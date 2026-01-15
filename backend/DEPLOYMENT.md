# Img Gen 部署指南

## 🚀 快速开始

### 本地开发（一键启动）
```bash
cd backend
./start-local.sh
```
访问: http://localhost:5173

### Docker部署（一键部署）
```bash
cd backend
echo "GEMINI_API_KEY=your_api_key" > .env
docker-compose -f docker-compose-fullstack.yml --env-file .env up -d --build
```
访问: http://localhost

---

## 💻 本地开发详细步骤

### 1. 配置API密钥
```bash
cd backend
./setup-api-key.sh  # 交互式配置
# 或手动创建
echo "GEMINI_API_KEY=your_api_key" > .env
```

### 2. 手动启动（可选）
```bash
# 后端 (终端1)
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-flexible.txt
export $(cat .env | xargs)
python file.py &      # 文件服务 (10086)
python gemini_api.py  # AI服务 (8088)

# 前端 (终端2)
cd frontend
npm install && npm run dev  # 前端服务 (5173)
```

### 3. 访问地址
- 前端界面: http://localhost:5173
- 文件API: http://localhost:10086
- AI API: http://localhost:8088

---

## 🐳 Docker部署

### 完整部署
```bash
cd backend

# 1. 配置API密钥
echo "GEMINI_API_KEY=your_actual_api_key" > .env

# 2. 启动所有服务
docker-compose -f docker-compose-fullstack.yml --env-file .env up -d --build

# 3. 检查状态
docker-compose -f docker-compose-fullstack.yml ps
```

### 服务说明
- **Frontend** (port 3000): React前端应用
- **Backend** (ports 8088, 10086): Flask API服务
- **Nginx** (port 80): 反向代理和静态文件服务

### 常用命令
```bash
# 查看日志
docker-compose -f docker-compose-fullstack.yml logs -f

# 重启服务
docker-compose -f docker-compose-fullstack.yml restart

# 停止服务
docker-compose -f docker-compose-fullstack.yml down
```

---

## 📦 生产部署

### 1. 构建部署包
```bash
cd backend
./build-fullstack.sh
```

### 2. 服务器部署
```bash
# 上传到服务器
scp img-gen-fullstack-*.tar.gz user@server:/opt/

# 服务器上执行
cd /opt && tar -xzf img-gen-fullstack-*.tar.gz
cd backend
echo "GEMINI_API_KEY=your_api_key" > .env
docker-compose -f docker-compose-fullstack.yml --env-file .env up -d --build
```

---

## 🔧 API端点

### 通过代理访问 (推荐)
- 文件上传: `POST /api/file/upload`
- 文件列表: `GET /api/file/list`
- AI生成: `POST /api/ai/generate`
- AI列表: `GET /api/ai/list_generated`

### 直接访问
- 文件服务: `http://localhost:10086/*`
- AI服务: `http://localhost:8088/*`

---

## ❗ 故障排查

### 1. 服务无法启动
```bash
# 检查API密钥
cat .env

# 检查端口占用
lsof -i :8088
lsof -i :10086
lsof -i :5173
```

### 2. Docker问题
```bash
# 查看容器状态
docker-compose -f docker-compose-fullstack.yml ps

# 查看日志
docker-compose -f docker-compose-fullstack.yml logs nginx
docker-compose -f docker-compose-fullstack.yml logs img-gen-backend

# 重新构建
docker-compose -f docker-compose-fullstack.yml build --no-cache
```

### 3. 常见错误
- **API密钥错误**: 检查`.env`文件中的`GEMINI_API_KEY`
- **端口占用**: 杀死占用进程或更换端口
- **依赖安装失败**: 使用`requirements-flexible.txt`

---

## 📋 项目文件结构

```
img/
├── README.md              # 项目总览
├── backend/               # 后端服务
│   ├── file.py           # 文件存储服务
│   ├── gemini_api.py     # AI生成服务
│   ├── start-local.sh    # 本地启动脚本
│   ├── setup-api-key.sh  # API密钥配置
│   ├── build-fullstack.sh # 构建脚本
│   ├── docker-compose-fullstack.yml # Docker编排
│   ├── nginx-proxy-fixed.conf # Nginx配置
│   └── requirements-*.txt # Python依赖
└── frontend/              # 前端应用
    ├── src/              # React源码
    ├── package.json      # Node依赖
    └── vite.config.js    # 构建配置
```