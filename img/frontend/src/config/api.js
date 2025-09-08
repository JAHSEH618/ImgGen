// API 配置文件
const API_CONFIG = {
  // 基础API URL - 在生产环境中会被Nginx代理
  baseURL: import.meta.env.VITE_API_BASE_URL || window.location.origin,
  
  // 开发环境直接访问后端服务
  fileService: import.meta.env.DEV 
    ? (import.meta.env.VITE_DEV_FILE_API || 'http://localhost:10086')
    : '/api/file',
    
  aiService: import.meta.env.DEV 
    ? (import.meta.env.VITE_DEV_AI_API || 'http://localhost:8088')
    : '/api/ai'
}

// API URLs
export const API_URLS = {
  // 文件服务
  fileUpload: `${API_CONFIG.fileService}/upload`,
  fileList: `${API_CONFIG.fileService}/list`,
  fileImage: (filename) => `${API_CONFIG.fileService}/image/${filename}`,
  fileDownload: (filename) => `${API_CONFIG.fileService}/download/${filename}`,
  fileHeartbeat: `${API_CONFIG.fileService}/heartbeat`,
  
  // AI服务  
  aiGenerate: `${API_CONFIG.aiService}/generate`,
  aiImage: (filename) => `${API_CONFIG.aiService}/image/${filename}`,
  aiDownload: (filename) => `${API_CONFIG.aiService}/download/${filename}`,
  aiList: `${API_CONFIG.aiService}/list_generated`,
  aiHeartbeat: `${API_CONFIG.aiService}/heartbeat`
}

export default API_CONFIG