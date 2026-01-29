"""
Agent Data Model
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    """Agent类型"""
    AI_AGENT = "ai_agent"
    EDITOR = "editor"
    ASSISTANT = "assistant"
    AUTOMATION = "automation"


class AgentStatus(str, Enum):
    """Agent状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"


class Skill(BaseModel):
    """技能模型"""
    id: str
    name: str
    category: str
    version: Optional[str] = "1.0.0"
    description: Optional[str] = None


class Agent(BaseModel):
    """Agent模型"""
    id: str = Field(..., description="Agent唯一标识")
    name: str = Field(..., description="Agent名称")
    type: AgentType = Field(default=AgentType.AI_AGENT, description="Agent类型")
    status: AgentStatus = Field(default=AgentStatus.ACTIVE, description="Agent状态")
    api_key: Optional[str] = Field(None, description="API密钥（加密存储）")
    skills: List[Skill] = Field(default_factory=list, description="关联的技能列表")
    last_active: Optional[datetime] = Field(default=None, description="最后活跃时间")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")


class AgentRegister(BaseModel):
    """Agent注册请求"""
    id: str
    name: str
    type: AgentType
    api_key: Optional[str] = None
    skill_ids: List[str] = Field(default_factory=list)


class AgentUpdate(BaseModel):
    """Agent更新请求"""
    name: Optional[str] = None
    status: Optional[AgentStatus] = None
    api_key: Optional[str] = None
    skill_ids: Optional[List[str]] = None


class AgentCall(BaseModel):
    """Agent调用请求"""
    task: str = Field(..., description="任务描述")
    context: Optional[dict] = Field(default_factory=dict, description="任务上下文")
    priority: Literal["low", "medium", "high"] = Field(default="medium", description="优先级")
