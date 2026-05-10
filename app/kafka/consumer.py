"""
Kafka Consumer — simulates a notification/audit service.

In a real microservices architecture:
  This would be a SEPARATE service entirely (different codebase, different deployment).
  It subscribes to the 'task-events' topic and reacts to events independently.

For this project:
  Run this as a separate process: python -m app.kafka.consumer
  It will continuously listen for task events and print notifications.

Producer-Consumer pattern:
  ┌──────────────┐    event     ┌─────────────┐    consume   ┌──────────────────┐
  │  Task API    │ ──────────► │  Kafka topic │ ──────────► │ Notification Svc  │
  │  (producer)  │             │  task-events │             │  (this consumer)  │
  └──────────────┘             └─────────────┘             └──────────────────┘

Interview talking point:
  "The consumer runs independently of the API. If the notification service
   goes down, Kafka holds the events. When it comes back up, it processes
   the backlog — no events are lost. This is the key benefit of event-driven
   architecture over direct service-to-service calls."
"""
import json
import logging
import signal
import sys
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def handle_event(event: dict) -> None:
    """
    Process a single event from Kafka.
    In production: send email, push notification, update dashboard, write to audit log.
    Here: print a human-readable notification to console.
    """
    event_type = event.get("event")
    task_id    = event.get("task_id")
    user       = event.get("user")
    timestamp  = event.get("timestamp")
    title      = event.get("title", "")
    new_status = event.get("new_status", "")

    # Map event types to notification messages
    messages = {
        "TASK_CREATED": f"✅ Notification: Task '{title}' created by {user} (ID: {task_id})",
        "TASK_UPDATED": f"🔄 Notification: Task {task_id} updated to '{new_status}' by {user}",
        "TASK_DELETED": f"🗑️  Notification: Task {task_id} deleted by {user}",
    }

    message = messages.get(event_type, f"📢 Unknown event: {event_type}")
    print(f"\n{message}")
    print(f"   Timestamp: {timestamp}")
    print(f"   Raw event: {json.dumps(event)}\n")

    # In production you'd also:
    # - Send email via SendGrid
    # - Push to Slack webhook
    # - Write to audit log database
    # - Update analytics dashboard


def run_consumer() -> None:
    """
    Start the Kafka consumer loop.
    Listens continuously on the task-events topic.
    Run this as: python -m app.kafka.consumer
    """
    try:
        from kafka import KafkaConsumer
    except ImportError:
        print("kafka-python not installed. Run: pip install kafka-python")
        sys.exit(1)

    print(f"Starting notification consumer...")
    print(f"Listening on topic: {settings.KAFKA_TOPIC}")
    print(f"Broker: {settings.KAFKA_BOOTSTRAP_SERVERS}")
    print("Press Ctrl+C to stop.\n")

    try:
        consumer = KafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            # Decode JSON bytes → Python dict automatically
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            # Consumer group — multiple consumers can share the load
            group_id="notification-service",
            # Start from earliest unread message on first run
            auto_offset_reset="earliest",
            # Commit offsets automatically after processing
            enable_auto_commit=True,
        )
    except Exception as exc:
        print(f"Cannot connect to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}: {exc}")
        print("Start Kafka with: docker-compose up -d")
        sys.exit(1)

    # Graceful shutdown on Ctrl+C
    def shutdown(sig, frame):
        print("\nShutting down consumer gracefully...")
        consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    # Main consumption loop
    print("Consumer ready. Waiting for events...")
    for message in consumer:
        try:
            event = message.value
            handle_event(event)
        except Exception as exc:
            logger.error(f"Error processing message: {exc}")
            # Don't crash the consumer on bad messages — log and continue


if __name__ == "__main__":
    run_consumer()
# Add this at the end of app/kafka/consumer.py

async def start_kafka_consumer():
    """
    Async wrapper to allow FastAPI to start the consumer in the background.
    If kafka-python is missing, it logs a warning instead of crashing.
    """
    try:
        from kafka import KafkaConsumer
        # Run the synchronous loop in a separate thread to avoid blocking FastAPI
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, run_consumer)
    except ImportError:
        logging.warning("Kafka Consumer: kafka-python not installed. Consumer is disabled.")
    except Exception as e:
        logging.error(f"Kafka Consumer failed to start: {e}")