import collections
import configparser
import copy

import six

from .persistence import ConfigPersistenceAdapter, YamlReaderWriter, JsonReaderWriter, ConfigParserReaderWriter
from .base import BaseSection, is_config_item, is_config_section
from .items import Item
from .parsers import ConfigDeclarationParser
from .utils import not_set
from .exceptions import NotFound


class Config(BaseSection):
    """
    Represents a section consisting of items (instances of :class:`.Item`) and other sections
    (instances of :class:`.Config`).
    
    .. attribute:: Config(config_declaration=None, **kwargs)
        
        Creates a section from a declaration.

        Args:
            ``config_declaration``: can be a dictionary, a list, a simple class, a module, another :class:`.Config`
            instance, and a combination of these.

        Keyword Args:

            ``item_cls``:

            ``config_parser_factory``:

        Examples::

            config = Config([
                ('greeting', 'Hello!'),
                ('uploads', Config({
                    'enabled': True,
                    'tmp_dir': '/tmp',
                })),
                ('db', {
                    'host': 'localhost',
                    'user': 'root',
                    'password': 'secret',
                    'name': 'test',
                }),
                ('api', Config([
                    'host',
                    'port',
                    'default_user',
                    ('enabled', Item(type=bool)),
                ])),
            ])
    
    .. attribute:: <config>[<name_or_path>]
    
        Access item by its name, section by its alias, or either by its path.

        Args:
            ``name`` (str): name of an item or alias of a section

        Args:
            ``path`` (tuple): path of an item or a section
        
        Returns:
            :class:`.Item` or :class:`.Config`

        Examples::

            >>> config['greeting']
            <Item greeting 'Hello!'>

            >>> config['uploads']
            <Config uploads at 4436269600>

            >>> config['uploads', 'enabled'].value
            True
    
    .. attribute:: <config>.<name>
    
        Access an item by its name or a section by its alias.

        For names and aliases that break Python grammar rules, use ``config[name]`` notation instead.
        
        Returns:
            :class:`.Item` or :class:`.Config`

    .. attribute:: <name_or_path> in <Config>

        Returns ``True`` if an item or section with the specified name or path is to be found in this section.

    .. attribute:: len(<Config>)

        Returns the number of items and sections in this section (does not include sections and items in
        sub-sections).

    .. attribute:: __iter__()

        Returns an iterator over all item names and section aliases in this section.

    """

    cm__item_cls = Item
    cm__configparser_factory = configparser.ConfigParser

    def __new__(cls, config_declaration=None, item_cls=None, configparser_factory=None):
        if config_declaration and isinstance(config_declaration, cls):
            return copy.deepcopy(config_declaration)

        instance = super(Config, cls).__new__(cls)
        instance._cm__section = None
        instance._cm__section_alias = None
        instance._cm__configs = collections.OrderedDict()
        instance._cm__configparser_adapter = None
        instance._cm__json_adapter = None
        instance._cm__yaml_adapter = None
        instance._cm__click_extension = None

        if item_cls:
            instance.cm__item_cls = item_cls
        if configparser_factory:
            instance.cm__configparser_factory = configparser_factory

        instance._cm__process_config_declaration = ConfigDeclarationParser(section=instance)

        if config_declaration:
            instance._cm__process_config_declaration(config_declaration)

        return instance

    def __repr__(self):
        return '<{cls} {alias} at {id}>'.format(cls=self.__class__.__name__, alias=self.alias, id=id(self))

    def _resolve_config_key(self, key):
        if isinstance(key, six.string_types):
            if key in self._cm__configs:
                return self._cm__configs[key]
            else:
                raise NotFound(key, section=self)

        if isinstance(key, (tuple, list)) and len(key) > 0:
            if len(key) == 1:
                return self._resolve_config_key(key[0])
            else:
                return self._resolve_config_key(key[0])[key[1:]]
        else:
            raise TypeError('Expected either a string or a tuple as key, got {!r}'.format(key))

    def __contains__(self, key):
        try:
            _ = self._resolve_config_key(key)
            return True
        except NotFound:
            return False

    def __setitem__(self, key, value):
        if isinstance(key, six.string_types):
            name = key
            rest = None
        elif isinstance(key, (tuple, list)) and len(key) > 0:
            name = key[0]
            if len(key) == 1:
                rest = None
            else:
                rest = key[1:]
        else:
            raise TypeError('Expected either a string or a tuple as key, got {!r}'.format(key))

        if rest:
            self[name][rest] = value
            return

        if is_config_item(value):
            self.add_item(name, value)
        elif isinstance(value, self.__class__):
            self.add_section(name, value)
        else:
            raise TypeError(
                'Config sections/items can only be replaced with sections/items, '
                'got {type}. To set value use ..[{name}].value = <new_value>'.format(
                    type=type(value),
                    name=name,
                )
            )

    def __getitem__(self, key):
        return self._resolve_config_key(key)

    def __getattr__(self, name):
        if not isinstance(name, six.string_types):
            raise TypeError('Expected a string, got a {!r}'.format(type(name)))

        if name.startswith('_'):
            raise AttributeError(name)

        return self._resolve_config_key(name)

    def __setattr__(self, name, value):
        if name.startswith('cm__') or name.startswith('_cm__'):
            return super(Config, self).__setattr__(name, value)
        elif is_config_item(value):
            self.add_item(name, value)
        elif isinstance(value, self.__class__):
            self.add_section(name, value)
        else:
            raise TypeError(
                'Config sections/items can only be replaced with sections/items, '
                'got {type}. To set value use {name}.value = <new_value> notation.'.format(
                    type=type(value),
                    name=name,
                )
            )

    def __len__(self):
        return len(self._cm__configs)

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True

    def __iter__(self):
        for name in self._cm__configs.keys():
            yield name

    def _parse_path(self, path=None, separator='.'):
        if not path:
            return ()

        clean_path = tuple(path.split(separator))
        if clean_path not in self:
            # TODO Use custom exceptions
            raise AttributeError(path)

        return clean_path

    def _get_recursive_iterator(self, recursive=False):
        """
        Basic recursive iterator whose only purpose is to yield all items
        and sections in order, with their full paths as keys.

        Main challenge is to de-duplicate items and sections which
        have aliases.

        Do not add any new features to this iterator, instead
        build others that extend this one.
        """

        names_yielded = set()

        for obj_alias, obj in self._cm__configs.items():
            if obj.is_section:
                if obj.alias in names_yielded:
                    continue
                names_yielded.add(obj.alias)

                yield (obj.alias,), obj

                if not recursive:
                    continue

                for sub_item_path, sub_item in obj._get_recursive_iterator(recursive=recursive):
                    yield (obj_alias,) + sub_item_path, sub_item

            else:
                # _cm__configs contains duplicates so that we can have multiple aliases point
                # to the same item. We have to de-duplicate here.
                if obj.name in names_yielded:
                    continue
                names_yielded.add(obj.name)

                yield (obj.name,), obj

    def _get_path_iterator(self, path=None, separator='.', recursive=False):
        clean_path = self._parse_path(path=path, separator=separator)

        config = self[clean_path] if clean_path else self

        if clean_path:
            yield clean_path, config

        if config.is_section:
            for path, obj in config._get_recursive_iterator(recursive=recursive):
                yield (clean_path + path), obj

    def iter_items(self, recursive=False, path=None, key='path', separator='.'):
        """

        Args:
            recursive: if ``True``, recurse into sub-sections.

            path (tuple or string): optional path to limit iteration over.

            key: ``path`` (default), ``str_path``, ``name``, or ``None``.

            separator (string): used both to interpret ``path=`` kwarg when it is a string,
                and to generate ``str_path`` as the returned key.

        Returns:
            iterator: iterator over ``(key, item)`` pairs of all items
                in this section (and sub-sections if ``recursive=True``).

        """
        for x in self.iter_all(recursive=recursive, path=path, key=key, separator=separator):
            if key is None:
                if x.is_item:
                    yield x
            elif x[1].is_item:
                yield x

    def iter_sections(self, recursive=False, path=None, key='path', separator='.'):
        """
        Args:
            recursive: if ``True``, recurse into sub-sections.

            path (tuple or string): optional path to limit iteration over.

            key: ``path`` (default), ``str_path``, ``alias``, or ``None``.

            separator (string): used both to interpret ``path=`` kwarg when it is a string,
                and to generate ``str_path`` as the returned key.

        Returns:
            iterator: iterator over ``(key, section)`` pairs of all sections
                in this section (and sub-sections if ``recursive=True``).

        """
        for x in self.iter_all(recursive=recursive, path=path, key=key, separator=separator):
            if key is None:
                if x.is_section:
                    yield x
            elif x[1].is_section:
                yield x

    def iter_all(self, recursive=False, path=None, key='path', separator='.'):
        """
        Args:
            recursive: if ``True``, recurse into sub-sections

            path (tuple or string): optional path to limit iteration over.

            key: ``path`` (default), ``str_path``, ``name``, or ``None``.

            separator (string): used both to interpret ``path=`` kwarg when it is a string,
                and to generate ``str_path`` as the returned key.

        Returns:
            iterator: iterator over ``(path, obj)`` pairs of all items and
            sections contained in this section.
        """
        for path, obj in self._get_path_iterator(recursive=recursive, path=path, separator=separator):
            if key is None:
                yield obj
            elif key == 'path':
                yield path, obj
            elif key == 'name' or key == 'alias':
                if obj.is_section:
                    yield obj.alias, obj
                else:
                    yield obj.name, obj
            elif key == 'str_path':
                yield separator.join(path), obj
            else:
                raise ValueError('Invalid key {!r}'.format(key))

    def iter_paths(self, recursive=False, path=None, key='path', separator='.'):
        """

        Args:
            recursive: if ``True``, recurse into sub-sections

            path (tuple or string): optional path to limit iteration over.

            key: ``path`` (default), ``str_path``, or ``name``.

            separator (string): used both to interpret ``path=`` kwarg when it is a string,
                and to generate ``str_path`` as the returned key.

        Returns:
            iterator: iterator over paths of all items and sections
            contained in this section.

        """
        assert key is not None
        for path, _ in self.iter_all(recursive=recursive, path=path, key=key, separator=separator):
            yield path

    def dump_values(self, with_defaults=True, dict_cls=dict):
        """
        Export values of all items contained in this section to a dictionary.

        Items with no values set (and no defaults set if ``with_defaults=True``) will be excluded.
        
        Returns:
            dict: A dictionary of key-value pairs, where for sections values are dictionaries
            of their contents.
        
        """
        values = dict_cls()
        for item_name, item in self._cm__configs.items():
            if is_config_section(item):
                section_values = item.dump_values(with_defaults=with_defaults, dict_cls=dict_cls)
                if section_values:
                    values[item_name] = section_values
            else:
                if item.has_value:
                    if with_defaults or not item.is_default:
                        values[item.name] = item.value
        return values

    def load_values(self, dictionary, as_defaults=False):
        """
        Import config values from a dictionary.
        
        When ``as_defaults`` is set to ``True``, the values
        imported will be set as defaults. This can be used to
        declare the sections and items of configuration.
        Values of sections and items in ``dictionary`` can be
        dictionaries as well as instances of :class:`.Item` and
        :class:`.Config`.
        
        Args:
            dictionary: 
            as_defaults: if ``True``, the imported values will be set as defaults.
        """
        for name, value in dictionary.items():
            if name not in self:
                if as_defaults:
                    if isinstance(value, dict):
                        self[name] = self.create_section()
                        self[name].load_values(value, as_defaults=as_defaults)
                    else:
                        self[name] = self.create_item(name, default=value)
                else:
                    # Skip unknown names if not interpreting dictionary as defaults
                    continue
            elif is_config_item(self[name]):
                if as_defaults:
                    self[name].default = value
                else:
                    self[name].value = value
            else:
                self[name].load_values(value, as_defaults=as_defaults)

    def reset(self):
        """
        Recursively resets values of all items contained in this section
        and its subsections to their default values.
        """
        for _, item in self.iter_items(recursive=True):
            item.reset()

    @property
    def is_default(self):
        """
        ``True`` if values of all config items in this section and its subsections
        have their values equal to defaults or have no value set.
        """
        for _, item in self.iter_items(recursive=True):
            if not item.is_default:
                return False
        return True

    @property
    def section(self):
        """
        Returns:
            (:class:`.Config`): section to which this section belongs or ``None`` if this
            hasn't been added to any section.
        """
        return self._cm__section

    @property
    def alias(self):
        """
        Returns alias with which this section was added to another or ``None`` if it hasn't been added
        to any.
        
        Returns:
            (str)
        """
        return self._cm__section_alias

    def added_to_section(self, alias, section):
        """
        A hook that is called when this section is added to another.
        This should only be called when extending functionality of :class:`.Config`.
        
        Args:
            alias (str): alias with which the section as added as a sub-section to another 
            section (:class:`.Config`): section to which this section has been added
        """
        self._cm__section = section
        self._cm__section_alias = alias

    @property
    def configparser(self):
        """
        Adapter to dump/load INI format strings and files using standard library's
        ``ConfigParser`` (or the backported configparser module in Python 2).
        
        Returns:
            :class:`.ConfigPersistenceAdapter`
        """
        if self._cm__configparser_adapter is None:
            self._cm__configparser_adapter = ConfigPersistenceAdapter(
                config=self,
                reader_writer=ConfigParserReaderWriter(
                    config_parser_factory=self.cm__configparser_factory,
                ),
            )
        return self._cm__configparser_adapter

    @property
    def json(self):
        """
        Adapter to dump/load JSON format strings and files.
        
        Returns:
            :class:`.ConfigPersistenceAdapter`
        """
        if self._cm__json_adapter is None:
            self._cm__json_adapter = ConfigPersistenceAdapter(
                config=self,
                reader_writer=JsonReaderWriter(),
            )
        return self._cm__json_adapter

    @property
    def yaml(self):
        """
        Adapter to dump/load YAML format strings and files.
        
        Returns:
            :class:`.ConfigPersistenceAdapter`
        """
        if self._cm__yaml_adapter is None:
            self._cm__yaml_adapter = ConfigPersistenceAdapter(
                config=self,
                reader_writer=YamlReaderWriter(),
            )
        return self._cm__yaml_adapter

    @property
    def click(self):
        if self._cm__click_extension is None:
            from .click_ext import ClickExtension
            self._cm__click_extension = ClickExtension(
                config=self
            )
        return self._cm__click_extension

    def add_item(self, alias, item):
        """
        Add a config item to this section.
        """
        if not isinstance(alias, six.string_types):
            raise TypeError('Item name must be a string, got a {!r}'.format(type(alias)))
        item = copy.deepcopy(item)
        if item.name is not_set:
            item.name = alias
        self._cm__configs[item.name] = item
        self._cm__configs[alias] = item
        item.added_to_section(alias, self)

    def add_section(self, alias, section):
        """
        Add a sub-section to this section.
        """
        if not isinstance(alias, six.string_types):
            raise TypeError('Section name must be a string, got a {!r}'.format(type(alias)))
        self._cm__configs[alias] = section
        section.added_to_section(alias, self)
