# 更新日志

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

[English](CHANGELOG_EN.md) | **简体中文**

---

## [未发布]

### 计划中

- Docker 部署优化
- 批量图像处理
- 图像历史持久化存储

---

## [1.1.0] - 2026-01-15

### 新增

- **图片走马灯组件** — 全新交互式轮播展示生成结果
  - 左右导航按钮
  - 缩略图快速选择
  - 全屏预览弹窗
  - 一键下载功能
- **图片预览弹窗** — 点击放大查看任意图片
  - 固定定位 + 正确的层级关系
  - ESC 键快速关闭
  - 弹窗内下载按钮
- **调试日志系统** — 控制台输出生成状态监控
- **警告提示** — 当 AI 处理成功但未生成图片时给出反馈

### 变更

- **Gemini API 配置优化** — 添加 `response_modalities=['Text', 'Image']` 确保返回图片
  - 修复了 API 只返回文本的关键问题
  - 同时应用于 `generate_text_to_image` 和 `generate_images_batch` 函数
- **文件上传处理增强** — 使用 `secure_filename()` 清理文件名
  - 保存前检查目录是否存在
  - 改进文件操作错误处理
- **前端状态管理优化** — 分离 `currentSessionImages` 与 `generatedImages` 历史记录

### 修复

- **`[Errno 2] No such file or directory`** — 后端现在确保上传目录存在
- **弹窗不显示** — 添加正确的 CSS 定位 (`position: fixed`, `z-index`)
- **生成后走马灯不显示** — 修复 API 响应解析和状态更新
- **图片不渲染** — 解决前端 `generated_files` 数组处理问题

### 移除

- 调试测试按钮（开发测试完成，不再需要）

---

## [1.0.0] - 2026-01-14

### 新增

- **首次正式发布** — 完整的 AI 图像生成全栈应用
- **文本生成图片** — 通过自然语言提示词生成图像
- **图像编辑** — 上传图片并使用 AI 进行转换
- **文件存储服务** — Session 隔离的文件管理
  - 安全上传与哈希验证
  - 3 分钟无活动后自动清理
- **前端界面** — 现代化 React UI
  - 拖拽上传
  - 模式切换（上传存储 / 生成变体）
  - 响应式设计 + Warm & Organic 主题
- **服务管理脚本** — `start.sh`, `stop.sh`, `restart.sh`
- **Session 管理** — 自动会话跟踪与清理
- **RESTful API** — 完整的文件存储和 AI 生成接口

### 技术细节

- 后端：Python Flask + Google GenAI SDK
- 前端：React 18 + Vite + Lucide Icons
- AI 模型：Gemini 2.5 Flash (Image Preview)
- 启动脚本支持虚拟环境自动激活

---

## [0.1.0] - 2026-01-13

### 新增

- 项目初始化
- 基础 Flask 后端框架
- Vite + React 前端初始化
- 环境配置结构

---

[未发布]: https://github.com/your-username/img-gen/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/your-username/img-gen/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/your-username/img-gen/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/your-username/img-gen/releases/tag/v0.1.0
