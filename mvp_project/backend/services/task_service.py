"""
Task Service - 任务调度和执行逻辑
"""
from typing import List, Optional
from datetime import datetime
from models.task import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority, TaskExecutionResult
from models.agent import Agent, AgentStatus
import uuid


class TaskScheduler:
    """智能任务调度器"""

    def __init__(self):
        self.agents_available = {}  # agent_id -> Agent

    def update_agent_status(self, agent: Agent):
        """更新Agent状态"""
        self.agents_available[agent.id] = agent

    def find_best_agent(self, task: Task, agents: List[Agent]) -> Optional[Agent]:
        """
        为任务找到最合适的Agent

        策略:
        1. 优先级匹配任务技能要求
        2. 检查Agent状态（必须是active）
        3. 如果有指定preferred_agent_id，优先使用
        4. 选择负载最低的Agent
        """
        # 如果有首选Agent，优先使用
        if task.skill_requirements:
            for agent in agents:
                if agent.id == task.skill_requirements[0] and agent.status == AgentStatus.ACTIVE:
                    return agent

        # 找到所有active的agents
        active_agents = [a for a in agents if a.status == AgentStatus.ACTIVE]
        if not active_agents:
            return None

        # 简单策略：随机选择一个active agent
        # TODO: 实现更智能的调度策略（负载均衡、技能匹配等）
        return active_agents[0]


class TaskService:
    """任务服务类"""

    def __init__(self):
        # 临时使用内存存储
        self.tasks: dict[str, Task] = {}
        self.scheduler = TaskScheduler()

    async def list_tasks(self, status: Optional[TaskStatus] = None, 
                        agent_id: Optional[str] = None) -> List[Task]:
        """列出所有任务"""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        if agent_id:
            tasks = [t for t in tasks if t.agent_id == agent_id]
        
        # 按创建时间倒序排序
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks

    async def get_task(self, task_id: str) -> Optional[Task]:
        """获取指定任务"""
        return self.tasks.get(task_id)

    async def create_task(self, task_data: TaskCreate, agents: List[Agent]) -> Task:
        """创建新任务"""
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            skill_requirements=task_data.skill_requirements,
            context=task_data.context
        )

        # 智能分配Agent
        best_agent = self.scheduler.find_best_agent(task, agents)
        if best_agent:
            task.agent_id = best_agent.id
            task.assigned_agent = best_agent.name

        self.tasks[task_id] = task
        return task

    async def update_task(self, task_id: str, update_data: TaskUpdate) -> Optional[Task]:
        """更新任务信息"""
        task = self.tasks.get(task_id)
        if not task:
            return None

        if update_data.title:
            task.title = update_data.title
        if update_data.description:
            task.description = update_data.description
        if update_data.status:
            # 更新时间戳
            if update_data.status == TaskStatus.RUNNING and task.started_at is None:
                task.started_at = datetime.utcnow()
            if update_data.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                if task.completed_at is None:
                    task.completed_at = datetime.utcnow()
                    if task.started_at:
                        task.duration_seconds = (task.completed_at - task.started_at).total_seconds()
            
            task.status = update_data.status
        if update_data.priority:
            task.priority = update_data.priority
        if update_data.agent_id:
            task.agent_id = update_data.agent_id
        if update_data.result:
            task.result = update_data.result
        if update_data.error:
            task.error = update_data.error

        return task

    async def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    async def execute_task(self, task_id: str, agents: List[Agent]) -> TaskExecutionResult:
        """执行任务"""
        task = await self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # 更新任务状态为运行中
        await self.update_task(task_id, TaskUpdate(status=TaskStatus.RUNNING))

        # 获取Agent
        agent = next((a for a in agents if a.id == task.agent_id), None)
        if not agent or agent.status != AgentStatus.ACTIVE:
            await self.update_task(
                task_id, 
                TaskUpdate(status=TaskStatus.FAILED, error="Agent not available")
            )
            return TaskExecutionResult(
                task_id=task_id,
                agent_id=task.agent_id or "unknown",
                status=TaskStatus.FAILED,
                error="Agent not available",
                duration_seconds=0.0,
                timestamp=datetime.utcnow()
            )

        # TODO: 实现实际的任务执行逻辑
        # 这里模拟执行
        start_time = datetime.utcnow()

        # 模拟任务执行
        result = {
            "task": task.title,
            "agent": agent.name,
            "output": f"Task '{task.title}' executed successfully by {agent.name}",
            "context": task.context
        }

        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()

        # 更新任务状态为完成
        await self.update_task(
            task_id,
            TaskUpdate(status=TaskStatus.COMPLETED, result=result)
        )

        return TaskExecutionResult(
            task_id=task_id,
            agent_id=agent.id,
            status=TaskStatus.COMPLETED,
            result=result,
            duration_seconds=duration,
            timestamp=end_time
        )


# 全局任务服务实例
task_service = TaskService()
