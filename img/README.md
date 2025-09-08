# Img Gen 项目构建和部署指南

## 📂 项目结构
```
img/
├── backend/              # 后端服务
│   ├── file.py          # 文件存储服务
│   ├── gemini_api.py    # AI生成服务
│   ├── __init__.py      # 服务管理器
│   └── ...配置文件
└── frontend/            # 前端React应用
    ├── src/             # 源代码
    ├── package.json     # 依赖配置
    └── ...配置文件
```

## 🚀 快速开始

### 1. 本地开发（一键启动）
```bash
cd backend
./start-local.sh    # 一键启动前后端
```
- 前端: http://localhost:5173
- 后端: http://localhost:8088, http://localhost:10086

### 2. Docker部署（一键部署）
```bash
cd backend
echo "GEMINI_API_KEY=your_api_key" > .env
docker-compose -f docker-compose-fullstack.yml --env-file .env up -d --build
```
- 访问: http://localhost

---

## 💻 本地开发环境

### 前置条件
- Python 3.11+
- Node.js 18+
- Gemini API Key

### 手动启动
```bash
# 1. 配置API密钥
cd backend
echo "GEMINI_API_KEY=your_api_key" > .env

# 2. 启动后端
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-flexible.txt
export $(cat .env | xargs)
python file.py &      # 文件服务
python gemini_api.py  # AI服务

# 3. 启动前端 (新终端)
cd frontend
npm install
npm run dev
```

### 停止服务
```bash
./stop-local.sh  # 或按 Ctrl+C
```

---

## 🐳 Docker部署

### 完整部署（前端+后端+代理）
```bash
cd backend

# 1. 配置API密钥
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 2. 启动服务
docker-compose -f docker-compose-fullstack.yml --env-file .env up -d --build

# 3. 检查状态
docker-compose -f docker-compose-fullstack.yml ps

# 4. 查看日志
docker-compose -f docker-compose-fullstack.yml logs -f
```

### 服务架构
- `img-gen-frontend` (port 3000): React前端
- `img-gen-backend` (ports 8088, 10086): Python后端服务
- `nginx` (port 80): 反向代理

### 停止和清理
```bash
# 停止服务
docker-compose -f docker-compose-fullstack.yml down

# 清理数据
docker-compose -f docker-compose-fullstack.yml down -v
```

---

## 📦 生产构建

### 构建部署包
```bash
cd backend
./build-fullstack.sh
```
生成: `img-gen-fullstack-YYYYMMDD_HHMMSS.tar.gz`

### 服务器部署
```bash
# 1. 上传部署包
scp img-gen-fullstack-*.tar.gz user@server:/opt/

# 2. 服务器解压
cd /opt && tar -xzf img-gen-fullstack-*.tar.gz

# 3. 启动服务
cd backend
echo "GEMINI_API_KEY=your_api_key" > .env
docker-compose -f docker-compose-fullstack.yml --env-file .env up -d --build
```

---

## 🔧 API端点

### 文件服务 (端口 10086)
- `POST /upload` - 上传文件
- `GET /list` - 文件列表
- `GET /image/<filename>` - 图片访问
- `GET /download/<filename>` - 文件下载

### AI服务 (端口 8088)
- `POST /generate` - AI图片生成
- `GET /list_generated` - 生成图片列表
- `GET /image/<filename>` - AI图片访问
- `GET /download/<filename>` - AI图片下载

### 代理访问 (端口 80)
- 文件服务: `/api/file/*`
- AI服务: `/api/ai/*`

---

## ❗ 故障排查

### 检查服务状态
```bash
# Docker模式
docker-compose -f docker-compose-fullstack.yml ps
docker-compose -f docker-compose-fullstack.yml logs

# 本地开发
curl http://localhost:10086/list
curl http://localhost:8088/list_generated
```

### 重启服务
```bash
# Docker模式
docker-compose -f docker-compose-fullstack.yml restart

# 本地开发
./start-local.sh
```

### 常见问题
1. **API密钥错误**: 检查 `.env` 文件中的 `GEMINI_API_KEY`
2. **端口占用**: `lsof -i :8088` 查看占用进程
3. **依赖安装失败**: 使用 `requirements-flexible.txt`

---

## 📋 核心文件说明

### 后端核心文件
- `file.py` - 文件存储服务
- `gemini_api.py` - AI生成服务  
- `__init__.py` - 服务管理器
- `docker-compose-fullstack.yml` - Docker编排文件
- `nginx-proxy-fixed.conf` - Nginx代理配置

### 前端核心文件
- `src/components/ImageUploadForm.jsx` - 主界面组件
- `src/config/api.js` - API配置
- `package.json` - 依赖配置
- `vite.config.js` - 构建配置

### 工具脚本
- `start-local.sh` - 本地开发启动
- `build-fullstack.sh` - 构建部署包
- `setup-api-key.sh` - API密钥配置