# -*- coding: utf-8 -*-

import pytest

from builtins import str

from configmanager import Config, Item


def test_items_are_created_using_create_item_method():
    class CustomItem(Item):
        pass

    class CustomConfig(Config):
        def create_item(self, *args, **kwargs):
            return CustomItem(*args, **kwargs)

    config = CustomConfig({
        'a': {'b': {'c': {'d': 1, 'e': '2', 'f': True}}},
        'g': False,
    })

    assert isinstance(config, CustomConfig)
    assert isinstance(config.g, CustomItem)
    assert isinstance(config.a, CustomConfig)
    assert isinstance(config.a.b.c, CustomConfig)
    assert isinstance(config.a.b.c.d, CustomItem)


def test_reset_resets_values_to_defaults():
    config = Config({
        'x': Item(type=int),
        'y': Item(default='YES')
    })

    config.x.value = 23
    config.y.value = 'NO'

    assert config.x.value == 23
    assert config.y.value == 'NO'

    config.reset()

    assert config.x.is_default
    assert config.y.value == 'YES'


def test_repr_of_config():
    config = Config()
    assert repr(config).startswith('<Config at ')


def test_assigning_nameless_item_directly_to_config_should_set_its_name():
    config = Config()
    config.dummy = Config()
    config.dummy.x = Item(value=5)
    assert config.dummy.x.name == 'x'

    config.dummy['y'] = Item(default=True)
    assert config.dummy.y.name == 'y'

    assert config.to_dict() == {'dummy': {'x': 5, 'y': True}}


def test_assigning_item_with_name_directly_to_config_should_preserve_its_name():
    # This is debatable, but assuming that user wants to use
    # attribute access as much as possible, this should allow them to.

    config = Config()
    config.dummy = Config()

    config.dummy.a_b = Item(name='a.b', value='AB')
    assert config.dummy.a_b.name == 'a.b'
    assert config.dummy['a_b']
    assert 'a_b' in config.dummy
    assert 'a.b' in config.dummy

    config.dummy['w'] = Item(name='www', value=6)
    assert 'www' in config.dummy
    assert config.dummy.w.name == 'www'
    assert config.dummy.www.name == 'www'

    assert config.to_dict() == {'dummy': {'a.b': 'AB', 'www': 6}}

    all_dummies = list(config.dummy.iter_items())
    assert len(all_dummies) == 2

    items = dict(config.dummy.iter_items())
    assert ('a.b',) in items
    assert ('a_b',) not in items
    assert ('www',) in items
    assert ('w',) not in items


def test_item_name_and_alias_must_be_a_string():
    config = Config()

    with pytest.raises(TypeError):
        config.x = Item(name=5)

    with pytest.raises(TypeError):
        config[5] = Item()

    with pytest.raises(TypeError):
        config[5] = Item(name='x')


def test_section_name_must_be_a_string():
    config = Config()

    with pytest.raises(TypeError):
        config[5] = Config()


def test_to_dict_should_not_include_items_with_no_usable_value():
    config = Config()
    assert config.to_dict() == {}

    config.a = Item()
    config.b = Item()
    config.dummies = Config({'x': Item(), 'y': Item()})
    assert config.to_dict() == {}

    config.dummies.x.value = 'yes'
    assert config.to_dict() == {'dummies': {'x': 'yes'}}

    config.b.value = 'no'
    assert config.to_dict() == {'dummies': {'x': 'yes'}, 'b': 'no'}


def test_read_dict_recursively_loads_values_from_a_dictionary():
    config = Config({
        'a': {
            'x': 0,
            'y': True,
            'z': 0.0,
        },
        'b': {
            'c': {
                'd': {
                    'x': 'xxx',
                    'y': 'yyy',
                },
            },
        },
    })
    assert config.a.x.value == 0
    assert config.a.y.value is True

    config.read_dict({
        'a': {'x': '5', 'y': 'no'},
    })
    assert config.a.x.value == 5
    assert config.a.y.value is False

    config.b.c.read_dict({
        'e': 'haha',  # will be ignored
        'd': {'x': 'XXX'},
    })
    assert config.b.c.d.x.value == 'XXX'
    assert 'e' not in config.b.c


def test_read_dict_as_defaults_loads_default_values_from_a_dictionary():
    config = Config()

    # both will be ignored
    config.read_dict({
        'a': 5,
        'b': True,
    })

    assert 'a' not in config
    assert 'b' not in config

    # both will be added
    config.read_dict({
        'a': 5,
        'b': True,
    }, as_defaults=True)

    assert config.a.value == 5
    assert config.b.value is True


@pytest.fixture
def raw_logging_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'plain': {
                'format': '%(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }


@pytest.fixture
def raw_db_config():
    return {
        'host': 'localhost',
        'username': 'admin',
        'password': 'secret',
        'dbname': 'admindb',
    }


@pytest.fixture
def mixed_app_config(raw_logging_config, raw_db_config):
    """
     A config that contains a previously existing config
     as well as one generated on initialisation.
    """
    return Config({
        'logging': Config(raw_logging_config),
        'db': raw_db_config,
    })


def test_declaration_parser_does_not_modify_config(raw_logging_config):
    logging_config = Config(raw_logging_config)
    assert isinstance(logging_config, Config)

    assert logging_config['version']
    assert logging_config['formatters']

    config = Config({'logging': logging_config})
    assert isinstance(config, Config)

    assert config['logging']['version']
    assert config['logging']['formatters']

    assert config['logging']['formatters'] is logging_config['formatters']

    logging_config['version'].value = '2'
    assert config['logging']['version'].value == 2


def test_allows_iteration_over_all_items(mixed_app_config):
    config = mixed_app_config

    all_items = list(config.iter_items())
    assert len(all_items) == 14

    db_items = list(config['db'].iter_items())
    assert len(db_items) == 4

    formatters_items = list(config['logging']['formatters'].iter_items())
    assert len(formatters_items) == 2

    formatters = config['logging']['formatters'].to_dict()
    assert formatters['plain'] == {'format': '%(message)s'}


def test_forbids_accidental_item_overwrite_via_setitem(mixed_app_config):
    config = mixed_app_config

    assert config['db']['username'].value == 'admin'

    with pytest.raises(TypeError):
        config['db']['username'] = 'admin2'

    config['db']['username'].value = 'admin2'
    assert config['db']['username'].value == 'admin2'


def test_allows_iteration_over_sections(mixed_app_config):
    config = mixed_app_config

    sections = dict(config.iter_sections())
    assert len(sections) == 2

    assert len(dict(sections['db'].iter_sections())) == 0

    logging_sections = dict(sections['logging'].iter_sections())
    assert len(logging_sections) == 3


def test_attribute_read_access(mixed_app_config):
    config = mixed_app_config

    assert isinstance(config.db, Config)
    assert isinstance(config.db.username, Item)
    assert isinstance(config.logging.handlers, Config)
    assert isinstance(config.logging.handlers.default, Config)
    assert isinstance(config.logging.loggers[''].handlers, Item)
    assert isinstance(config.logging.loggers[''].level, Item)


def test_attribute_write_access(mixed_app_config):
    config = mixed_app_config

    assert config.db.username.value == 'admin'
    config.db.username.value = 'ADMIN'
    assert config.db.username.value == 'ADMIN'

    config.logging.loggers[''].propagate.value = 'no'
    assert config.logging.loggers[''].propagate.value is False


def test_forbids_accidental_item_overwrite_via_setattr(mixed_app_config):
    config = mixed_app_config

    with pytest.raises(TypeError):
        config.db.username = 'ADMIN'

    assert config.db.username.value == 'admin'

    with pytest.raises(TypeError):
        config.logging.loggers[''].propagate = False

    assert config.logging.loggers[''].propagate.value is True


def test_to_dict(mixed_app_config, raw_db_config, raw_logging_config):
    config = mixed_app_config

    config_dict = config.to_dict()

    assert isinstance(config_dict, dict)

    assert config_dict['db'] is not raw_db_config
    assert config_dict['db'] == raw_db_config
    assert config_dict['logging'] == raw_logging_config


def test_can_inspect_config_contents(mixed_app_config):
    config = mixed_app_config

    assert 'db' in config
    assert 'dbe' not in config

    assert 'logging' in config

    assert 'handlers' in config.logging
    assert '' in config.logging.loggers
    assert 'haha' not in config.logging.loggers


def test_can_have_a_dict_as_a_config_value_if_wrapped_inside_item():
    # You may want to have a dictionary as a config value if you only
    # change it all together or you only pass it all in one piece.

    config = Config({
        'db': {
            'user': 'admin',
            'password': 'secret',
        },
        'aws': Item(default={
            'access_key': '123',
            'secret_key': 'secret',
        })
    })

    assert isinstance(config.aws, Item)
    assert config.aws.name == 'aws'

    with pytest.raises(AttributeError):
        assert config.aws.access_key.value == '123'

    assert config.aws.value['access_key'] == '123'

    # This should have no effect because it is working on a copy of the default
    # value, not the real thing.
    config.aws.value['secret_key'] = 'NEW_SECRET'

    assert config.to_dict()['aws'] == {'access_key': '123', 'secret_key': 'secret'}


def test_len_of_config_returns_number_of_items_in_it():
    assert len(Config()) == 0

    assert len(Config({'enabled': True})) == 1

    assert len(Config({'uploads': Config()})) == 0
    assert len(Config({'uploads': {}})) == 0

    assert len(Config({'uploads': {'enabled': False}})) == 1
    assert len(Config({'uploads': {'enabled': False, 'threads': 1}})) == 2

    assert len(Config({'uploads': {'enabled': False, 'threads': 0}, 'greeting': 'Hi'})) == 3


def test__getitem__handles_paths_to_sections_and_items_and_so_does__contains__():
    config = Config()
    with pytest.raises(KeyError):
        assert not config['uploads', 'enabled']
    assert ('uploads',) not in config
    assert ('uploads', 'enabled') not in config

    config.uploads = Config({'enabled': True, 'db': {'user': 'root'}})
    assert config['uploads', 'enabled'] is config.uploads.enabled
    assert config['uploads', 'db'] is config.uploads.db

    assert 'uploads' in config
    assert ('uploads',) in config
    assert ('uploads', 'enabled') in config
    assert ('uploads', 'db') in config
    assert ('uploads', 'db', 'user') in config

    assert config.uploads.db.user.value == 'root'

    config['uploads', 'db', 'user'].set('admin')
    assert config.uploads.db.user.value == 'admin'


def test_can_use__setitem__to_create_new_deep_paths():
    config = Config()
    config['uploads'] = Config({'enabled': True})

    with pytest.raises(TypeError):
        config['uploads', 'threads'] = 5

    config['uploads', 'threads'] = Item(value=5)
    assert config.uploads.threads.type is int

    config['uploads', 'db'] = Config({'user': 'root'})
    assert config.uploads.db


def test_section_knows_its_alias():
    config = Config()
    config.uploads = Config({
        'enabled': True
    })
    assert config.uploads.alias == 'uploads'

    config.uploads.db = Config({'connection': {'user': 'root'}})
    assert config.uploads.db.alias == 'db'
    assert config.uploads.db.connection.alias == 'connection'


def test_config_item_value_can_be_unicode_str(tmpdir):
    config1 = Config({'greeting': u'Hello, {name}', 'name': u'Anonymous'})
    config1.name.value = u'Jānis Bērziņš'
    assert config1.name.type is str

    path = tmpdir.join('config.ini').strpath
    config1.configparser.dump(path, with_defaults=True)

    config2 = Config({'greeting': '', 'name': ''})
    config2.configparser.load(path)
    assert config2.name.value == u'Jānis Bērziņš'
    assert config1.to_dict(with_defaults=True) == config2.to_dict(with_defaults=True)


def test_config_of_config_is_a_deep_copy_of_original_config():
    config1 = Config({'uploads': {'enabled': True, 'db': {'user': 'root'}}})
    config1.uploads.enabled.value = False

    config2 = Config(config1)
    assert config1 is not config2
    assert config1.to_dict() == config2.to_dict()
    assert config1.to_dict(with_defaults=True) == config2.to_dict(with_defaults=True)

    config1.uploads.enabled.value = True
    config1.uploads.db.read_dict({'user': 'admin'})

    assert config2.to_dict(with_defaults=True) == {'uploads': {'enabled': False, 'db': {'user': 'root'}}}

    config2.uploads.db.user.default = 'default-user'
    assert config1.uploads.db.user.default == 'root'
