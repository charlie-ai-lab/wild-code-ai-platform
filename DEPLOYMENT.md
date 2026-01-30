# 🚀 野码AI Agent协作平台 - 外网部署指南

## 📋 当前部署状态

### 服务状态
- **后端API**: ✅ 运行中
  - 本地地址: http://localhost:8000
  - 外网地址: https://small-signs-stick.loca.lt

- **前端UI**: ✅ 运行中
  - 本地地址: http://localhost:3000
  - 外网地址: https://wildcodeai-frontend.loca.lt

---

## 🛠️ 快速启动

### 启动后端
```bash
cd /root/clawd/mvp_project/backend
source venv/bin/activate
python main.py
```

### 启动前端
```bash
cd /root/clawd/mvp_project/frontend
python3 -m http.server 3000
```

### 创建外网隧道
```bash
npm install -g localtunnel
lt --port 8000 &
lt --port 3000 --subdomain wildcodeai-frontend &
```

---

## 🌐 访问地址

- 后端API: https://small-signs-stick.loca.lt
- 前端UI: https://wildcodeai-frontend.loca.lt
- API文档: https://small-signs-stick.loca.lt/docs

---

**状态**: ✅ 已部署，可外网访问
**GitHub**: https://github.com/charlie-ai-lab/wild-code-ai-platform
