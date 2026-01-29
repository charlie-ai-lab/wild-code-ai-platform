"""
Task API Routes
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List, Optional
from models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from services.task_service import task_service
from services.agent_service import agent_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=List[Task], summary="列出所有任务")
async def list_tasks(
    status: Optional[TaskStatus] = None,
    agent_id: Optional[str] = None
):
    """
    列出所有任务

    - **status**: 可选，按状态筛选
    - **agent_id**: 可选，按Agent筛选
    """
    return await task_service.list_tasks(status, agent_id)


@router.get("/{task_id}", response_model=Task, summary="获取任务详情")
async def get_task(task_id: str):
    """
    获取指定任务的详细信息
    """
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task


@router.post("/create", response_model=Task, status_code=status.HTTP_201_CREATED, summary="创建新任务")
async def create_task(task_data: TaskCreate):
    """
    创建新任务

    - **title**: 任务标题
    - **description**: 可选，任务描述
    - **priority**: 优先级（low/medium/high/urgent）
    - **skill_requirements**: 可选，需要的技能列表
    - **context**: 可选，任务上下文
    - **preferred_agent_id**: 可选，首选Agent ID
    """
    # 获取所有可用Agents
    agents = await agent_service.list_agents(status=None)
    
    task = await task_service.create_task(task_data, agents)
    return task


@router.put("/{task_id}", response_model=Task, summary="更新任务信息")
async def update_task(task_id: str, update_data: TaskUpdate):
    """
    更新指定任务的信息

    - **title**: 可选，新标题
    - **description**: 可选，新描述
    - **status**: 可选，新状态
    - **priority**: 可选，新优先级
    - **agent_id**: 可选，新Agent ID
    - **result**: 可选，执行结果
    - **error**: 可选，错误信息
    """
    task = await task_service.update_task(task_id, update_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除任务")
async def delete_task(task_id: str):
    """
    删除指定任务
    """
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return None


@router.post("/{task_id}/execute", summary="执行任务")
async def execute_task(task_id: str, background_tasks: BackgroundTasks):
    """
    执行指定任务

    系统会自动分配最合适的Agent并执行任务
    """
    try:
        # 获取所有可用Agents
        agents = await agent_service.list_agents(status=None)
        
        # 异步执行任务
        background_tasks.add_task(task_service.execute_task, task_id, agents)
        
        return {
            "task_id": task_id,
            "status": "executing",
            "message": "Task execution started"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{task_id}/cancel", response_model=Task, summary="取消任务")
async def cancel_task(task_id: str):
    """
    取消指定任务
    """
    task = await task_service.update_task(task_id, TaskUpdate(status=TaskStatus.CANCELLED))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task
