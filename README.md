# 🚀 野码AI - Agent性能基准测试平台

> 统一的多AI Agent协作平台 + Agent性能基准测试

一个开源的Agent性能监控和基准测试平台，支持对比Claude、Gemini、GPT等多种Agent的性能。

---

## ✨ 核心功能

### 🤖 Agent管理
- 支持多Agent注册和管理
- Agent状态监控
- Agent技能包管理
- API密钥安全存储

### 📊 性能基准测试
- **标准化测试用例** - 代码生成、问答、推理等
- **Agent性能排名** - 类似3DMark的跑分系统
- **多Agent对比** - 横向对比不同Agent性能
- **性能退化检测** - 自动检测性能下降并告警
- **智能性能报告** - AI驱动的优化建议

### 🎯 智能任务调度
- 自动分配最适合的Agent
- 任务优先级管理
- 异步后台任务执行
- 任务状态实时跟踪

### 🔥 热点扫描
- Hacker News热门追踪
- NewsNow实时热点
- 自动识别商业机会
- 相关性分析

### 📈 财经分析
- A股实时行情
- 港股通扫描
- 板块热点分析
- 投资建议生成

---

## 🛠️ 技术栈

### 后端
```
Python 3.12
FastAPI 0.104
Pydantic 2.0
SQLAlchemy 2.0
PostgreSQL 16
Redis 7.4
```

### 前端
```
Next.js 15
TypeScript 5
Tailwind CSS 3.4
React 18
Recharts (图表)
```

### 数据分析
```
Python statistics
NumPy
Pandas
```

---

## 🚀 快速开始

### 前置要求
- Python 3.12+
- Node.js 18+
- PostgreSQL 16
- Redis 7.4

### 安装

#### 后端

```bash
cd mvp_project/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务器
python main.py
```

后端将在 http://localhost:8000 启动

#### 前端（开发中）

```bash
cd mvp_project/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 启动

---

## 📚 API文档

启动后端后，访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 核心API端点

#### Agents
```
GET    /agents              - 列出所有Agents
GET    /agents/{id}         - 获取Agent详情
POST   /agents/register     - 注册新Agent
PUT    /agents/{id}         - 更新Agent信息
DELETE /agents/{id}         - 删除Agent
POST   /agents/{id}/call    - 调用Agent执行任务
```

#### Tasks
```
GET    /tasks               - 列出所有任务
GET    /tasks/{id}          - 获取任务详情
POST   /tasks/create        - 创建新任务
PUT    /tasks/{id}          - 更新任务信息
DELETE /tasks/{id}          - 删除任务
POST   /tasks/{id}/execute  - 执行任务
POST   /tasks/{id}/cancel   - 取消任务
```

#### Benchmarks
```
GET    /benchmarks/tests             - 列出所有测试用例
POST   /benchmarks/run              - 运行基准测试
GET    /benchmarks/rankings          - 获取Agent性能排名
GET    /benchmarks/reports/latest    - 获取测试报告
GET    /benchmarks/alerts/degradation - 获取退化告警
GET    /benchmarks/stats/summary    - 获取统计摘要
POST   /benchmarks/compare          - 对比Agent性能
```

---

## 📊 快速示例

### 运行Agent基准测试

```bash
curl -X POST http://localhost:8000/benchmarks/run \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "claude_code",
    "categories": ["code_generation", "qa"]
  }'
```

### 获取Agent性能排名

```bash
curl http://localhost:8000/benchmarks/rankings?limit=5
```

### 创建新任务

```bash
curl -X POST http://localhost:8000/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "代码审查任务",
    "priority": "high",
    "skill_requirements": ["claude_code"]
  }'
```

---

## 🎯 MVP路线图

### Phase 1: 核心功能 ✅ (完成)
- [x] Agent管理API
- [x] 智能任务调度
- [x] Agent性能基准测试
- [x] 热点扫描工具
- [x] 财经分析脚本

### Phase 2: 前端和集成 (开发中)
- [ ] Next.js用户界面
- [ ] 性能仪表盘
- [ ] 实时排名展示
- [ ] 性能图表可视化

### Phase 3: 高级功能
- [ ] 真实Agent API集成 (Claude, Gemini, OpenAI)
- [ ] 数据库持久化 (PostgreSQL + Redis)
- [ ] 用户认证和授权
- [ ] 多租户支持

### Phase 4: 企业版
- [ ] 私有部署支持
- [ ] 自定义指标
- [ ] A/B测试支持
- [ ] SLA监控

---

## 📈 项目进度

```
后端API:       ████████████████████ 100% ✅
Agent管理:     ████████████████████ 100% ✅
任务调度:      ████████████████████ 100% ✅
基准测试:      ████████████████████ 100% ✅
前端开发:      ░░░░░░░░░░░░░░░░░░░░   0%
真实Agent集成: ░░░░░░░░░░░░░░░░░░░░   0%
数据库持久化:  ░░░░░░░░░░░░░░░░░░░░   0%
文档完善:      ████████████████░░░░  70%
```

---

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 📧 联系方式

- GitHub: [@charlie-ai-lab](https://github.com/charlie-ai-lab)
- 邮箱: charlie901030@gmail.com

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [Next.js](https://nextjs.org/) - React全栈框架
- [Hacker News](https://news.ycombinator.com/) - 热点数据源
- [MarginLab](https://marginlab.ai/) - Claude Code性能追踪灵感

---

## 🌟 Star History

如果这个项目对你有帮助，请给它一个⭐️

---

**[野码AI](https://github.com/charlie-ai-lab/wild-code-ai-platform)** - 用我的野码爪子debug一切！⚡
