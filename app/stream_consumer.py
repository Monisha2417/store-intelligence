import threading
import time

from pipeline.event_bus import event_queue
from app.ingestion import ingest_single_event


def start_event_consumer():

    def consume():
        print("[STREAM] Consumer started...")

        while True:

            if not event_queue.empty():

                event = event_queue.get()

                print(f"[STREAM] Consuming event: {event['event_type']} | visitor={event['visitor_id']}")

                try:
                    ingest_single_event(event)
                except Exception as e:
                    print("[STREAM ERROR]", e)

            time.sleep(0.05)

    thread = threading.Thread(target=consume, daemon=True)
    thread.start()