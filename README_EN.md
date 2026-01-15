<div align="center">

# 🎨 Img Gen

**AI-Powered Image Generation & Editing Tool**

Next-generation image creation platform powered by Google Gemini AI

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Gemini](https://img.shields.io/badge/Gemini_AI-Flash_2.5-8E75B2?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[简体中文](README.md) | **English**

</div>

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🎨 **Text-to-Image** | Generate AI images from natural language descriptions |
| 🖌️ **Image Editing** | Transform uploaded images with AI-powered prompts |
| 📂 **Secure Storage** | Session-isolated file management with auto-cleanup |
| 🎠 **Image Carousel** | Interactive slideshow for viewing generated results |
| ⚡ **Real-time Preview** | Instant display of uploads and generation results |

---

## 🚀 Quick Start

### Prerequisites

| Dependency | Version |
| :--- | :--- |
| Python | 3.9+ |
| Node.js | 18+ |
| Gemini API Key | [Get it here](https://aistudio.google.com/apikey) |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/img-gen.git
cd img-gen

# 2. Install backend dependencies
cd backend && pip install -r requirements-core.txt && cd ..

# 3. Install frontend dependencies
cd frontend && npm install && cd ..
```

### Configuration

Create a `.env` file in the project root:

```ini
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
```

### Running the Application

```bash
./start.sh      # Start all services
./stop.sh       # Stop all services
./restart.sh    # Restart all services
```

**Access Points:**

| Service | URL |
| :--- | :--- |
| 🌐 Frontend | <http://localhost:5173> |
| 📁 File Service | <http://localhost:10086> |
| 🤖 AI Service | <http://localhost:8088> |

---

## 📖 API Reference

### AI Image Generation (Port 8088)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/generate` | Generate or edit images |
| `GET` | `/image/<filename>` | Retrieve generated image |
| `GET` | `/download/<filename>` | Download image file |
| `GET` | `/list_generated` | List all generated images |
| `POST` | `/heartbeat` | Keep session alive |
| `GET` | `/test_api` | Test Gemini API connection |

### File Storage (Port 10086)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/upload` | Upload images to library |
| `GET` | `/list` | List uploaded files |
| `GET` | `/image/<filename>` | Retrieve stored image |
| `GET` | `/download/<filename>` | Download file |
| `POST` | `/heartbeat` | Keep session alive |

> **Note:** All requests require `X-Session-ID` header for session management.

---

## 📁 Project Structure

```text
img-gen/
├── start.sh / stop.sh / restart.sh   # Service management scripts
├── .env                               # Environment configuration
├── frontend/                          # React frontend application
│   ├── src/
│   │   ├── components/               # UI components (Carousel, Modal, etc.)
│   │   ├── pages/                    # Page components
│   │   ├── config/                   # API configuration
│   │   └── utils/                    # Utility functions
│   └── package.json
├── backend/
│   ├── tools/
│   │   ├── img_gen/                  # AI image generation service
│   │   │   └── routes.py             # Gemini API integration
│   │   └── file_storage/             # File storage service
│   │       └── app.py                # Upload/download handlers
│   ├── Dockerfile
│   └── docker-compose-fullstack.yml
├── CHANGELOG.md                       # Version history
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Axios, Lucide Icons, react-dropzone |
| **Backend** | Python Flask, Google GenAI SDK, Werkzeug |
| **AI Model** | Gemini 2.5 Flash (Image Preview) |
| **Deployment** | Docker, Nginx, Gunicorn |

---

## 🔒 Security Features

- **Session Isolation** — Users can only access their own files
- **Auto Cleanup** — Temporary files deleted after 3 minutes of inactivity
- **Secure Filenames** — All uploads sanitized with `secure_filename()`
- **Integrity Check** — SHA256 hash verification for file integrity

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ using Gemini AI**

</div>
