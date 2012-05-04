import redis
import rq


def get_setting(config, key, default):
    settings = config.registry.settings
    for prefix in ['rq.redis', 'redis']:
        value = settings.get('%s.%s' % (prefix, key))
        if value is not None:
            return type(default)(value)
    else:
        return default


def rq_tween_factory(handler, registry):
    def rq_tween(request):
        with rq.Connection(registry.settings['rq.redis']):
            return handler(request)
    return rq_tween


def includeme(config):
    try:
        host = get_setting(config, 'host', 'localhost')
        port = get_setting(config, 'port', 6379)
        db = get_setting(config, 'db', 1)
    except ValueError:
        raise ValueError('Invalid rq/redis configuration')
    connection = redis.Redis(host=host, port=port, db=db)
    config.registry.settings['rq.redis'] = connection
    config.add_tween('pyramid_rq.rq_tween_factory')


__all__ = ['includeme']
