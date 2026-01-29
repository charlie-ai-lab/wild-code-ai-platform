"""
Task Data Model
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """任务优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(BaseModel):
    """任务模型"""
    id: str = Field(..., description="任务唯一标识")
    title: str = Field(..., description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="任务优先级")
    agent_id: Optional[str] = Field(None, description="分配的Agent ID")
    assigned_agent: Optional[str] = Field(None, description="分配的Agent名称")
    skill_requirements: List[str] = Field(default_factory=list, description="需要的技能列表")
    context: dict = Field(default_factory=dict, description="任务上下文")
    result: Optional[dict] = Field(None, description="执行结果")
    error: Optional[str] = Field(None, description="错误信息")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    started_at: Optional[datetime] = Field(None, description="开始时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    duration_seconds: Optional[float] = Field(None, description="执行时长（秒）")


class TaskCreate(BaseModel):
    """创建任务请求"""
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    skill_requirements: List[str] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)
    preferred_agent_id: Optional[str] = None


class TaskUpdate(BaseModel):
    """更新任务请求"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    agent_id: Optional[str] = None
    result: Optional[dict] = None
    error: Optional[str] = None


class TaskExecutionResult(BaseModel):
    """任务执行结果"""
    task_id: str
    agent_id: str
    status: TaskStatus
    result: Optional[dict] = None
    error: Optional[str] = None
    duration_seconds: float
    timestamp: datetime
