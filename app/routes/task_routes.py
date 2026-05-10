from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.auth.dependencies import get_current_user
from app.schemas.task_schemas import CreateTaskRequest, UpdateTaskRequest, TaskResponse, TaskListResponse
from app.services.task_service import TaskService
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: CreateTaskRequest, current_user: dict = Depends(get_current_user)):
    # Pass both ID and Username to the service
    return await TaskService.create_task(payload, current_user["id"], current_user["username"])

@router.get("/", response_model=TaskListResponse)
async def get_tasks(current_user: User = Depends(get_current_user)):
    tasks = await TaskService.get_user_tasks(current_user.id)
    return {"total": len(tasks), "tasks": tasks}

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    # Change .id to ["id"]
    task = await TaskService.get_task_by_id(task_id, current_user["id"])
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str, 
    payload: UpdateTaskRequest, 
    current_user: dict = Depends(get_current_user)
):
    # Change current_user.id -> current_user["id"]
    # Also add current_user["username"] if your service needs it for Kafka
    task = await TaskService.update_task(
        task_id, 
        payload, 
        current_user["id"], 
        current_user["username"]
    )
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user: User = Depends(get_current_user)):
    success = await TaskService.delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None