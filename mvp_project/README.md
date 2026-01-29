# 🚀 野码AI - AI Agent协作平台 MVP

一个多AI Agent统一协作平台，支持Claude Code、Gemini CLI、OpenCode、CodeBuddy等31个agent，提供统一的API、任务调度、协作功能。

---

## 📊 项目概览

**项目名称**: 野码AI - AI Agent Collaboration Platform
**技术栈**: Python 3.12 + FastAPI 0.104 + Next.js 15 + TypeScript 5 + PostgreSQL 16 + Redis 7.4
**开发周期**: 4周
**目标用户**: 全栈开发者、AI驱动团队

---

## 🎯 核心功能

### 1. Agent注册与管理
- ✅ 支持Claude Code、Gemini CLI、OpenCode、CodeBuddy等
- ✅ API密钥管理
- ✅ Agent技能包管理（关联已安装的50个skills）
- ✅ Agent状态监控（在线/离线）

### 2. 统一API接口
- ✅ 标准化的Agent调用接口
- ✅ 跨Agent任务编排
- ✅ 结果聚合与缓存
- ✅ WebSocket实时通信

### 3. 协作工作空间
- ✅ 多人实时代码编辑
- ✅ 版本历史对比
- ✅ 评论和标注系统

### 4. 智能任务调度
- ✅ AI分析任务适合的Agent
- ✅ 自动负载均衡
- ✅ 任务优先级队列

---

## 🛠️ 技术架构

### 后端
```
backend/
├── main.py              # FastAPI入口
├── api/
│   ├── agents.py       # Agent管理API
│   ├── tasks.py       # 任务调度API
│   └── collaboration.py # 协作功能API
├── models/
│   ├── agent.py       # Agent模型
│   ├── skill.py       # 技能模型
│   └── task.py       # 任务模型
├── services/
│   ├── claude_code.py  # Claude Code集成
│   ├── gemini_cli.py  # Gemini CLI集成
│   ├── open_code.py   # OpenCode集成
│   └── codebuddy.py  # CodeBuddy集成
└── requirements.txt
```

### 前端
```
frontend/
├── app/
│   ├── layout.tsx       # 布局组件
│   └── page.tsx        # 主页面
├── components/
│   ├── AgentRegistry.tsx      # Agent注册界面
│   ├── AgentDashboard.tsx      # Agent仪表盘
│   └── TaskOrchestrator.tsx    # 任务编排器
└── lib/
    ├── integrations/
    │   ├── claude_code.tsx    # Claude Code集成
    │   ├── gemini_cli.tsx    # Gemini CLI集成
    │   ├── open_code.tsx      # OpenCode集成
    │   └── codebuddy.tsx    # CodeBuddy集成
```

### 数据库
- **PostgreSQL** - 主数据库
- **Redis** - 缓存和队列
- **SQLAlchemy** - ORM

### DevOps
- **Docker** - 容器化
- **GitHub Actions** - CI/CD
- **Nginx** - 反向代理

---

## 📋 开发计划

### Week 1: 基础架构 (当前)
- [x] 后端FastAPI项目初始化
- [x] 前端Next.js项目初始化
- [x] PostgreSQL数据库设计
- [x] Docker开发环境配置

### Week 2: 核心功能
- [ ] Agent注册API开发
- [ ] Claude Code集成测试
- [ ] 基础协作功能实现

### Week 3: 高级功能
- [ ] 智能任务调度系统
- [ ] 多Agent协作演示
- [ ] 性能优化

### Week 4: 上线准备
- [ ] 安全审计
- [ ] 压力测试
- [ ] 文档完善

---

## 🚀 快速开始

```bash
# 后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py

# 前端
cd frontend
npm install
npm run dev

# 访问
# 后端: http://localhost:8000
# 前端: http://localhost:3000
```

---

## 📝 API端点

### 核心API
- `GET /` - 平台信息
- `GET /health` - 健康检查
- `GET /agents` - 列出所有Agents
- `POST /agents/register` - 注册新Agent
- `GET /skills` - 列出所有Skills
- `GET /tasks` - 列出所有任务
- `POST /tasks/create` - 创建新任务

### Agent相关
- `POST /agents/{agent_id}/call` - 调用Agent
- `POST /agents/{agent_id}/skill/install` - 安装技能

### 协作
- `POST /collaboration/rooms` - 创建协作房间
- `GET /collaboration/rooms/{room_id}` - 获取房间信息
- `POST /collaboration/rooms/{room_id}/join` - 加入房间

---

## 💡 已集成的Skills (50个)

### AI辅助开发 (12个)
- Claude Code、Gemini CLI、OpenCode、CodeBuddy等

### GitHub自动化 (17个)
- github-action-gen、action-gen、github-kb、webhook-gen等

### 搜索工具 (6个)
- Tavily、Twitter、Reddit、Product Hunt等

### 设计工具 (4个)
- Logo-creator、Banner-creator、UI/UX-Pro-Max等

### 其他 (11个)
- ATXP付费API、find-skills、domain-hunter等

---

## 🎯 目标用户

- **全栈开发者** - 需要统一管理多个AI Agent
- **AI驱动团队** - 需要高效的AI工作流
- **DevOps团队** - 需要智能的CI/CD
- **内容创作者** - 需要智能搜索和内容工具

---

## 📊 市场分析

**市场规模**: 10亿美元 (AI开发工具市场)
**竞争强度**: 中高
**差异化**: 统一的多Agent协作平台
**市场缺口**: 大多数Agent工具各自为政，缺乏统一平台

---

## 🔐 安全考虑

- API密钥加密存储
- Agent权限验证
- 请求速率限制
- WebSocket认证

---

## 📞 资源链接

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Next.js文档](https://nextjs.org/)
- [Anthropic API](https://docs.anthropic.com/)
- [PostgreSQL文档](https://www.postgresql.org/docs/)

---

*最后更新: 2026-01-29 22:21*
