from queue import Queue

# Central event bus (SIMULATES KAFKA STREAM)
event_queue = Queue()

def publish_event(event: dict):
    """
    Called by detection pipeline
    """
    event_queue.put(event)