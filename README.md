<div align="center">

# 🎨 Img Gen

**AI 智能图像生成与编辑工具**

基于 Google Gemini AI 的下一代图像创作平台

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Gemini](https://img.shields.io/badge/Gemini_AI-Flash_2.5-8E75B2?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**简体中文** | [English](README_EN.md)

</div>

---

## ✨ 功能特性

| 功能 | 描述 |
| :--- | :--- |
| 🎨 **文本生成图片** | 通过自然语言描述，让 AI 为你创作图像 |
| 🖌️ **图像智能编辑** | 上传图片 + 提示词，实现风格转换、内容修改 |
| 📂 **安全文件存储** | Session 隔离机制，自动清理临时文件 |
| 🎠 **图片走马灯** | 交互式轮播展示生成结果，支持预览与下载 |
| ⚡ **实时预览** | 上传与生成结果即时展示，所见即所得 |

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 |
| :--- | :--- |
| Python | 3.9+ |
| Node.js | 18+ |
| Gemini API Key | [点击获取](https://aistudio.google.com/apikey) |

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/img-gen.git
cd img-gen

# 2. 安装后端依赖
cd backend && pip install -r requirements-core.txt && cd ..

# 3. 安装前端依赖
cd frontend && npm install && cd ..
```

### 环境配置

在项目根目录创建 `.env` 文件：

```ini
GEMINI_API_KEY=你的API密钥
FLASK_ENV=development
```

### 启动服务

```bash
./start.sh      # 启动全部服务
./stop.sh       # 停止服务
./restart.sh    # 重启服务
```

**服务访问地址：**

| 服务 | 地址 |
| :--- | :--- |
| 🌐 前端界面 | <http://localhost:5173> |
| 📁 文件服务 | <http://localhost:10086> |
| 🤖 AI 服务 | <http://localhost:8088> |

---

## 📖 API 接口文档

### AI 图像生成服务 (端口 8088)

| 方法 | 端点 | 描述 |
| :--- | :--- | :--- |
| `POST` | `/generate` | 生成或编辑图像 |
| `GET` | `/image/<filename>` | 获取生成的图片 |
| `GET` | `/download/<filename>` | 下载图片文件 |
| `GET` | `/list_generated` | 列出所有生成的图片 |
| `POST` | `/heartbeat` | 保持会话活跃 |
| `GET` | `/test_api` | 测试 Gemini API 连接 |

### 文件存储服务 (端口 10086)

| 方法 | 端点 | 描述 |
| :--- | :--- | :--- |
| `POST` | `/upload` | 上传图片到图库 |
| `GET` | `/list` | 列出已上传的文件 |
| `GET` | `/image/<filename>` | 获取存储的图片 |
| `GET` | `/download/<filename>` | 下载文件 |
| `POST` | `/heartbeat` | 保持会话活跃 |

> **注意：** 所有请求需携带 `X-Session-ID` 请求头用于会话管理。

---

## 📁 项目结构

```text
img-gen/
├── start.sh / stop.sh / restart.sh   # 服务管理脚本
├── .env                               # 环境配置文件
├── frontend/                          # React 前端应用
│   ├── src/
│   │   ├── components/               # UI 组件 (走马灯、弹窗等)
│   │   ├── pages/                    # 页面组件
│   │   ├── config/                   # API 配置
│   │   └── utils/                    # 工具函数
│   └── package.json
├── backend/
│   ├── tools/
│   │   ├── img_gen/                  # AI 图像生成服务
│   │   │   └── routes.py             # Gemini API 集成
│   │   └── file_storage/             # 文件存储服务
│   │       └── app.py                # 上传/下载处理
│   ├── Dockerfile
│   └── docker-compose-fullstack.yml
├── CHANGELOG.md                       # 版本更新日志
└── README.md
```

---

## 🛠️ 技术栈

| 层级 | 技术 |
| :--- | :--- |
| **前端** | React 18, Vite, Axios, Lucide Icons, react-dropzone |
| **后端** | Python Flask, Google GenAI SDK, Werkzeug |
| **AI 模型** | Gemini 2.5 Flash (Image Preview) |
| **部署** | Docker, Nginx, Gunicorn |

---

## 🔒 安全特性

- **Session 隔离** — 用户只能访问自己的文件
- **自动清理** — 3 分钟无活动后自动删除临时文件
- **文件名安全** — 所有上传文件使用 `secure_filename()` 清理
- **完整性校验** — SHA256 哈希验证文件完整性

---

## 🤝 参与贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

---

## 📄 开源协议

本项目基于 MIT 协议开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<div align="center">

**使用 Gemini AI 用心打造 ❤️**

</div>
