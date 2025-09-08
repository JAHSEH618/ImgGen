# Demo Project

这是一个包含多个子项目的演示工程，主要包括：

## 1. IMG - AI图像生成工具

基于Gemini AI的智能图像生成和转换工具，具有以下特性：

### 功能特性
- **文件上传**：支持多种图片格式上传（PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF, SVG）
- **AI图像生成**：基于Gemini AI API的智能图像转换
- **Session管理**：3分钟超时自动清理机制，保护用户隐私
- **实时预览**：上传和生成图片的实时预览
- **响应式设计**：现代化的用户界面

### 技术栈
- **前端**：React + Vite + Lucide Icons
- **后端**：Python Flask + Gemini AI API
- **部署**：Docker + Nginx

### 安全特性
- Session隔离：每个用户session只能访问自己的文件
- 自动清理：3分钟无活动后自动删除所有文件
- 传输加密：HTTPS传输安全
- 文件完整性检查：SHA256哈希验证

## 2. Shopify - 应用爬虫工具

Shopify应用商店数据爬取工具

### 功能
- 爬取Shopify应用商店应用信息
- 支持批量处理和数据导出
- 可配置的爬取策略

## 项目结构

```
demoProj/
├── img/                    # AI图像生成工具
│   ├── frontend/          # React前端
│   └── backend/           # Python Flask后端
├── shopify/               # Shopify爬虫工具
└── README.md
```

## 开发环境设置

请参考各子项目的具体文档：
- [IMG项目文档](./img/README.md)
- [IMG后端部署文档](./img/backend/DEPLOYMENT.md)

## 注意事项

- 请确保设置正确的API密钥
- 生产环境请使用HTTPS
- 定期清理临时文件和日志