# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**English** | [简体中文](CHANGELOG.md)

---

## [1.2.0] - 2026-02-04

### 🚀 Performance Optimizations

- **High Concurrency Backend** — Upgraded Gunicorn config to multi-process + multi-thread mode (`gthread`), boosting concurrency by 8-32x
- **Drastically Reduced Memory Usage** — Implemented **streaming file uploads**, reducing memory footprint for 30MB uploads from 30MB to just 8KB
- **Fast Frontend Loading** — Enabled **lazy loading** (`loading="lazy"`) and **async decoding** (`decoding="async"`) for all images
- **Request Cancellation** — Added support for canceling ongoing AI generation requests to prevent resource waste and memory leaks
- **Session Heartbeat** — Optimized heartbeat mechanism to reduce unnecessary network traffic and log noise

### ✨ New Features

- **Large File Support** — Increased maximum file upload size to **30MB**
- **Mobile Optimization** — Optimized file upload and browsing experience for mobile devices
- **Generation Cancellation** — Added an explicit "Cancel" button during generation
- **Image Sharing** — Added capability to share generated images
- **Access Control** — Enhanced session-based access control for image files

### 💅 UI/UX Improvements

- **New Upload Component** — Carousel-style design for upload preview
- **Interaction Polish** — Improved touch handling for mobile devices

---

---

## [1.1.0] - 2026-01-15

### Added

- **Image Carousel Component** — New interactive slideshow for viewing generated images
  - Navigation controls (previous/next)
  - Thumbnail strip for quick selection
  - Full-screen preview modal
  - Download actions directly from carousel
- **Image Preview Modal** — Click-to-zoom functionality for all images
  - Fixed positioning with proper z-index layering
  - Escape key to close
  - Download button in modal footer
- **Debug Logging** — Console logging for generation state monitoring
- **Warning Toast** — User feedback when AI processes but doesn't generate images

### Changed

- **Gemini API Configuration** — Added `response_modalities=['Text', 'Image']` to ensure image output
  - Fixed critical issue where API returned text-only responses
  - Applied to both `generate_text_to_image` and `generate_images_batch` functions
- **File Upload Handling** — Improved robustness with `secure_filename()` sanitization
  - Added directory existence check before saving
  - Better error handling for file operations
- **Frontend State Management** — Separated `currentSessionImages` from `generatedImages` history

### Fixed

- **`[Errno 2] No such file or directory`** — Backend now ensures upload directory exists
- **Modal not displaying** — Added proper CSS positioning (`position: fixed`, `z-index`)
- **Carousel not showing after generation** — Fixed API response parsing and state updates
- **Images not rendering** — Resolved `generated_files` array handling in frontend

### Removed

- Debug test button (used for development testing, no longer needed)

---

## [1.0.0] - 2026-01-14

### Added

- **Initial Release** — Full-stack AI image generation application
- **Text-to-Image Generation** — Generate images from natural language prompts
- **Image Editing** — Upload images and transform them with AI
- **File Storage Service** — Session-isolated file management
  - Secure upload with hash verification
  - Automatic cleanup after 3 minutes of inactivity
- **Frontend Interface** — Modern React-based UI
  - Drag-and-drop file upload
  - Mode toggle (Upload & Store / Generate Variations)
  - Responsive design with Warm & Organic theme
- **Service Management Scripts** — `start.sh`, `stop.sh`, `restart.sh`
- **Session Management** — Automatic session tracking and cleanup
- **API Endpoints** — RESTful API for both file storage and AI generation

### Technical Details

- Backend: Python Flask with Google GenAI SDK
- Frontend: React 18 + Vite + Lucide Icons
- AI Model: Gemini 2.5 Flash (Image Preview)
- Virtual environment activation in start scripts

---

## [0.1.0] - 2026-01-13

### Added

- Initial project scaffolding
- Basic Flask backend setup
- React frontend initialization with Vite
- Environment configuration structure

---

[1.1.0]: https://github.com/your-username/img-gen/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/your-username/img-gen/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/your-username/img-gen/releases/tag/v0.1.0
