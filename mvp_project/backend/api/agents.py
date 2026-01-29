"""
Agent API Routes
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models.agent import Agent, AgentRegister, AgentUpdate, AgentStatus
from services.agent_service import agent_service

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("", response_model=List[Agent], summary="列出所有Agents")
async def list_agents(status: Optional[AgentStatus] = None):
    """
    列出所有已注册的Agents

    - **status**: 可选，按状态筛选
    """
    return await agent_service.list_agents(status)


@router.get("/{agent_id}", response_model=Agent, summary="获取Agent详情")
async def get_agent(agent_id: str):
    """
    获取指定Agent的详细信息
    """
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    return agent


@router.post("/register", response_model=Agent, status_code=status.HTTP_201_CREATED, summary="注册新Agent")
async def register_agent(register_data: AgentRegister):
    """
    注册新Agent到平台

    - **id**: Agent唯一标识
    - **name**: Agent名称
    - **type**: Agent类型
    - **api_key**: 可选，API密钥
    - **skill_ids**: 可选，关联的技能ID列表
    """
    try:
        return await agent_service.register_agent(register_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{agent_id}", response_model=Agent, summary="更新Agent信息")
async def update_agent(agent_id: str, update_data: AgentUpdate):
    """
    更新指定Agent的信息

    - **name**: 可选，新名称
    - **status**: 可选，新状态
    - **api_key**: 可选，新API密钥
    - **skill_ids**: 可选，新的技能ID列表
    """
    agent = await agent_service.update_agent(agent_id, update_data)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除Agent")
async def delete_agent(agent_id: str):
    """
    从平台删除指定Agent
    """
    success = await agent_service.delete_agent(agent_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    return None


@router.post("/{agent_id}/call", summary="调用Agent执行任务")
async def call_agent(agent_id: str, task: str, context: dict = None):
    """
    调用指定Agent执行任务

    - **task**: 任务描述
    - **context**: 可选，任务上下文
    """
    try:
        return await agent_service.call_agent(agent_id, task, context or {})
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
