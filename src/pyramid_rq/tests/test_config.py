import unittest


class get_setting_tests(unittest.TestCase):
    def get_setting(self, *a, **kw):
        from pyramid_rq import get_setting
        return get_setting(*a, **kw)

    def test_redis_key_fallback(self):
        from pyramid.config import Configurator
        config = Configurator()
        config.registry.settings = {'redis.key': 2}
        self.assertEqual(self.get_setting(config, 'key', 0), 2)

    def test_prefer_rq_key(self):
        from pyramid.config import Configurator
        config = Configurator()
        config.registry.settings = {'rq.redis.key': 1, 'redis.key': 2}
        self.assertEqual(self.get_setting(config, 'key', 0), 1)

    def test_default_value_if_nothing_found(self):
        from pyramid.config import Configurator
        config = Configurator()
        config.registry.settings = {}
        self.assertEqual(self.get_setting(config, 'key', 0), 0)

    def test_convert_to_default_type(self):
        from pyramid.config import Configurator
        config = Configurator()
        config.registry.settings = {'redis.key': '2'}
        self.assertEqual(self.get_setting(config, 'key', 0), 2)

    def test_conversion_not_possible(self):
        from pyramid.config import Configurator
        config = Configurator()
        config.registry.settings = {'redis.key': 'two'}
        self.assertRaises(ValueError, self.get_setting, config, 'key', 0)


class rq_tween_factory_tests(unittest.TestCase):
    def rq_tween_factory(self, *a, **kw):
        from pyramid_rq import rq_tween_factory
        return rq_tween_factory(*a, **kw)

    def test_return_callable(self):
        import collections
        import inspect
        tween = self.rq_tween_factory(None, None)
        self.assertTrue(isinstance(tween, collections.Callable))
        (args, varargs, keywords, defaults) = inspect.getargspec(tween)
        self.assertEqual(len(args), 1)

    def test_handler_invocation(self):
        import mock
        registry = mock.Mock()
        registry.settings = {'rq.redis': 'dummy-redis'}
        handler = mock.Mock(return_value='response')
        tween = self.rq_tween_factory(handler, registry)
        self.assertEqual(tween('request'), 'response')
        handler.assert_called_once_with('request')


class includeme_tests(unittest.TestCase):
    def includeme(self, *a, **kw):
        from pyramid_rq import includeme
        return includeme(*a, **kw)

    def test_configuration(self):
        import mock
        from pyramid.config import Configurator
        config = Configurator()
        config.add_tween = mock.Mock()
        with mock.patch('pyramid_rq.get_setting') as mock_get_setting:
            mock_get_setting.return_value = None
            self.includeme(config)
            self.assertTrue('rq.redis' in config.registry)
            config.add_tween.assert_called_once_with(
                    'pyramid_rq.rq_tween_factory')
