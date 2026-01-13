from .logger import logger

class BasePlugin:
    def __init__(self, driver_instance):
        self.driver_instance = driver_instance
    
    def on_setup(self):
        pass
    
    def on_teardown(self):
        pass

class PluginManager:
    def __init__(self, driver_instance):
        self.driver_instance = driver_instance
        self.plugins = []

    def register(self, plugin_class):
        try:
            plugin = plugin_class(self.driver_instance)
            self.plugins.append(plugin)
            logger.info(f"Plugin: Registered {plugin_class.__name__}")
        except Exception as e:
            logger.error(f"Plugin: Failed to register {plugin_class.__name__}: {e}")

    def notify_setup(self):
        for plugin in self.plugins:
            plugin.on_setup()

    def notify_teardown(self):
        for plugin in self.plugins:
            plugin.on_teardown()
