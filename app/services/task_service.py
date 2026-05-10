import uuid
from typing import List, Optional
from app.database import get_db
from app.schemas.task_schemas import CreateTaskRequest, UpdateTaskRequest
from app.kafka.producer import publish_task_created, publish_task_updated

class TaskService:
    @staticmethod
    async def create_task(payload: CreateTaskRequest, user_id: str, username: str) -> dict:
        """Create a task in SQLite and publish a Kafka event."""
        task_id = str(uuid.uuid4())
        
        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (id, title, description, status, user_id) VALUES (?, ?, ?, ?, ?)",
            (task_id, payload.title, payload.description, payload.status, user_id)
        )
        conn.commit()
        conn.close()
        
        task_data = {
            "id": task_id, 
            "title": payload.title, 
            "description": payload.description,
            "status": payload.status,
            "user_id": user_id
        }
        
        # Fire and forget Kafka event
        publish_task_created(task_id=task_id, username=username, title=payload.title)
        
        return task_data

    @staticmethod
    async def get_user_tasks(user_id: str) -> List[dict]:
        """Fetch all tasks for a specific user."""
        conn = get_db()
        rows = conn.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    async def get_task_by_id(task_id: str, user_id: str) -> Optional[dict]:
        """Fetch a single task by ID."""
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?", 
            (task_id, user_id)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    async def update_task(task_id: str, payload: UpdateTaskRequest, user_id: str, username: str) -> Optional[dict]:
        """Update task status/details and publish update event."""
        task = await TaskService.get_task_by_id(task_id, user_id)
        if not task:
            return None

        # Build dynamic update query based on provided fields
        update_data = payload.dict(exclude_unset=True)
        if not update_data:
            return task

        set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
        params = list(update_data.values()) + [task_id, user_id]

        conn = get_db()
        conn.execute(f"UPDATE tasks SET {set_clause}, updated_at = datetime('now') WHERE id = ? AND user_id = ?", params)
        conn.commit()
        conn.close()

        # Notify Kafka of the update
        if "status" in update_data:
            publish_task_updated(task_id=task_id, username=username, new_status=update_data["status"])

        return await TaskService.get_task_by_id(task_id, user_id)