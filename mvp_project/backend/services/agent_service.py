"""
Agent Service - Agent业务逻辑
"""
from typing import List, Optional
from datetime import datetime
from models.agent import Agent, AgentRegister, AgentUpdate, AgentStatus, AgentType, Skill


class AgentService:
    """Agent服务类"""

    def __init__(self):
        # 临时使用内存存储，后期迁移到数据库
        self.agents: dict[str, Agent] = {}
        self._init_default_agents()

    def _init_default_agents(self):
        """初始化默认Agents"""
        default_agents = [
            Agent(
                id="claude_code",
                name="Claude Code",
                type=AgentType.AI_AGENT,
                status=AgentStatus.ACTIVE,
                skills=[
                    Skill(id="claude_code", name="Claude Code", category="ai_development")
                ]
            ),
            Agent(
                id="gemini_cli",
                name="Gemini CLI",
                type=AgentType.AI_AGENT,
                status=AgentStatus.ACTIVE,
                skills=[
                    Skill(id="gemini_cli", name="Gemini CLI", category="ai_development")
                ]
            ),
            Agent(
                id="open_code",
                name="OpenCode",
                type=AgentType.EDITOR,
                status=AgentStatus.ACTIVE,
                skills=[
                    Skill(id="open_code", name="OpenCode", category="editor")
                ]
            ),
            Agent(
                id="codebuddy",
                name="CodeBuddy",
                type=AgentType.ASSISTANT,
                status=AgentStatus.ACTIVE,
                skills=[
                    Skill(id="codebuddy", name="CodeBuddy", category="assistant")
                ]
            )
        ]
        for agent in default_agents:
            self.agents[agent.id] = agent

    async def list_agents(self, status: Optional[AgentStatus] = None) -> List[Agent]:
        """列出所有Agents"""
        agents = list(self.agents.values())
        if status:
            agents = [a for a in agents if a.status == status]
        return agents

    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """获取指定Agent"""
        return self.agents.get(agent_id)

    async def register_agent(self, register_data: AgentRegister) -> Agent:
        """注册新Agent"""
        if register_data.id in self.agents:
            raise ValueError(f"Agent {register_data.id} already exists")

        agent = Agent(
            id=register_data.id,
            name=register_data.name,
            type=register_data.type,
            api_key=register_data.api_key
        )

        self.agents[agent.id] = agent
        return agent

    async def update_agent(self, agent_id: str, update_data: AgentUpdate) -> Optional[Agent]:
        """更新Agent信息"""
        agent = self.agents.get(agent_id)
        if not agent:
            return None

        if update_data.name:
            agent.name = update_data.name
        if update_data.status:
            agent.status = update_data.status
        if update_data.api_key:
            agent.api_key = update_data.api_key

        agent.last_active = datetime.utcnow()
        return agent

    async def delete_agent(self, agent_id: str) -> bool:
        """删除Agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False

    async def call_agent(self, agent_id: str, task: str, context: dict = None) -> dict:
        """调用Agent执行任务"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        if agent.status != AgentStatus.ACTIVE:
            raise ValueError(f"Agent {agent_id} is not active")

        # 更新最后活跃时间
        agent.last_active = datetime.utcnow()

        # TODO: 实现实际的Agent调用逻辑
        # 这里返回模拟结果
        return {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "task": task,
            "status": "completed",
            "result": f"Agent {agent.name} executed task successfully",
            "timestamp": datetime.utcnow().isoformat()
        }


# 全局Agent服务实例
agent_service = AgentService()
