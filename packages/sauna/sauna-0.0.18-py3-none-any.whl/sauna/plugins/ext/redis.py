from sauna.plugins import Plugin, human_to_bytes, bytes_to_human,\
    PluginRegister

my_plugin = PluginRegister('Redis')


@my_plugin.plugin()
class Redis(Plugin):

    def __init__(self, config):
        super().__init__(config)
        try:
            import redis
            self.redis = redis
        except ImportError:
            from ... import DependencyError
            raise DependencyError(self.__class__.__name__, 'redis-py',
                                  'redis', 'python3-redis')
        self._redis_info = None

    @my_plugin.check()
    def used_memory(self, check_config):
        status = self._value_to_status_less(
            self.redis_info['used_memory'], check_config, human_to_bytes
        )
        output = 'Used memory: {}'.format(self.redis_info['used_memory_human'])
        return status, output

    @my_plugin.check()
    def used_memory_rss(self, check_config):
        status = self._value_to_status_less(
            self.redis_info['used_memory_rss'], check_config, human_to_bytes
        )
        output = 'Used memory RSS: {}'.format(
            bytes_to_human(self.redis_info['used_memory_rss'])
        )
        return status, output

    @property
    def redis_info(self):
        if not self._redis_info:
            r = self.redis.StrictRedis(**self.config)
            self._redis_info = r.info()
        return self._redis_info

    @my_plugin.check()
    def llen(self, check_config):
        r = self.redis.StrictRedis(**self.config)
        num_items = r.llen(check_config['key'])
        status = self._value_to_status_less(num_items, check_config)
        output = '{} items in key {}'.format(num_items, check_config['key'])
        return status, output

    @staticmethod
    def config_sample():
        return '''
        # Redis
        - type: Redis
          checks:
            - type: used_memory
              warn: 128M
              crit: 1024M
            - type: used_memory_rss
              warn: 128M
              crit: 1024M
            # Check the size of a list
            - type: llen
              key: celery
              warn: 10
              crit: 20
          config:
            host: localhost
            port: 6379
        '''
