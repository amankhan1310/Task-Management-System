"""
Kafka Producer — publishes task events to the 'task-events' topic.

Event-driven architecture pattern:
  When a task is created or updated, we publish an event to Kafka.
  Other services (notification service, analytics service, audit log)
  can independently consume and react to these events WITHOUT being
  directly coupled to the task service.

This is the Producer-Consumer pattern:
  Producer (this file) → Kafka topic → Consumer (kafka/consumer.py)

Graceful fallback:
  If Kafka is not running (e.g. local dev without Docker),
  events are logged to console instead of failing the API call.
  This keeps the project runnable without Kafka for interview demos.

Interview talking point:
  "I used Kafka to decouple task creation from notification delivery.
   When a task is created, the API publishes an event and returns immediately.
   The notification service consumes the event asynchronously — no waiting."
"""
import json
import logging
from datetime import datetime, timezone
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

# Try to import KafkaProducer — gracefully handle missing Kafka
try:
    from kafka import KafkaProducer as _KafkaProducer
    _KAFKA_AVAILABLE = True
except ImportError:
    _KAFKA_AVAILABLE = False


class TaskEventProducer:
    """
    Kafka producer for task lifecycle events.
    Publishes JSON messages to the configured Kafka topic.
    """

    def __init__(self):
        self._producer: Optional[object] = None
        self._connected = False
        self._try_connect()

    def _try_connect(self) -> None:
        """Attempt to connect to Kafka. Fail silently if unavailable."""
        if not _KAFKA_AVAILABLE:
            logger.warning("kafka-python not installed. Events will be logged only.")
            return

        try:
            self._producer = _KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                # Serialize Python dict → JSON bytes for Kafka
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                # Retry up to 3 times on transient failures
                retries=3,
                # Wait up to 1 second for broker acknowledgement
                request_timeout_ms=1000,
            )
            self._connected = True
            logger.info(f"Kafka producer connected to {settings.KAFKA_BOOTSTRAP_SERVERS}")
        except Exception as exc:
            logger.warning(
                f"Kafka unavailable ({exc}). Events will be logged to console only. "
                f"Start Kafka with: docker-compose up -d"
            )

    def _build_event(self, event_type: str, task_id: str, username: str, extra: dict = None) -> dict:
        """Build a standardised event payload."""
        event = {
            "event": event_type,                           # e.g. TASK_CREATED
            "task_id": task_id,
            "user": username,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if extra:
            event.update(extra)
        return event

    def publish(self, event_type: str, task_id: str, username: str, extra: dict = None) -> None:
        """
        Publish an event to the Kafka topic.
        Falls back to console logging if Kafka is unavailable.

        Args:
            event_type: e.g. "TASK_CREATED", "TASK_UPDATED", "TASK_DELETED"
            task_id:    The ID of the task that triggered the event.
            username:   The user who performed the action.
            extra:      Any additional fields to include in the event payload.
        """
        event = self._build_event(event_type, task_id, username, extra)

        if self._connected and self._producer:
            try:
                self._producer.send(settings.KAFKA_TOPIC, value=event)
                self._producer.flush()  # ensure message is sent before returning
                logger.info(f"[Kafka] Published: {event}")
            except Exception as exc:
                # Don't fail the API call if Kafka has issues
                logger.error(f"[Kafka] Failed to publish event: {exc}")
                self._log_fallback(event)
        else:
            self._log_fallback(event)

    def _log_fallback(self, event: dict) -> None:
        """Log event to console when Kafka is unavailable."""
        print(f"\n[KAFKA EVENT - console fallback]\n{json.dumps(event, indent=2)}\n")

    def close(self) -> None:
        """Clean up the producer connection."""
        if self._producer and self._connected:
            self._producer.close()


# ── Singleton producer instance ───────────────────────────────────────────────
# Created once at module import — reused across all requests
# Avoids the overhead of creating a new producer per API call
producer = TaskEventProducer()


# ── Convenience functions ─────────────────────────────────────────────────────

def publish_task_created(task_id: str, username: str, title: str) -> None:
    """Publish a TASK_CREATED event."""
    producer.publish(
        event_type="TASK_CREATED",
        task_id=task_id,
        username=username,
        extra={"title": title}
    )


def publish_task_updated(task_id: str, username: str, new_status: str) -> None:
    """Publish a TASK_UPDATED event."""
    producer.publish(
        event_type="TASK_UPDATED",
        task_id=task_id,
        username=username,
        extra={"new_status": new_status}
    )


def publish_task_deleted(task_id: str, username: str) -> None:
    """Publish a TASK_DELETED event."""
    producer.publish(
        event_type="TASK_DELETED",
        task_id=task_id,
        username=username,
    )
