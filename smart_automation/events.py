from .logger import logger

class EventObserver:
    """Base class for event observers."""
    def on_event(self, event_name, data):
        pass

class LoggingObserver(EventObserver):
    """Observer that logs every event."""
    def on_event(self, event_name, data):
        logger.debug(f"Event Observed: {event_name} with data: {data}")

class EventDispatcher:
    """Dispatches events to registered observers."""
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def dispatch(self, event_name, data):
        for observer in self._observers:
            try:
                observer.on_event(event_name, data)
            except Exception as e:
                logger.error(f"Error in observer {type(observer).__name__}: {e}")

# Global dispatcher
dispatcher = EventDispatcher()
dispatcher.register(LoggingObserver())
