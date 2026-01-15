// API 配置文件
const API_CONFIG = {
  // 基础API URL - 在生产环境中会被Nginx代理
  baseURL: import.meta.env.VITE_API_BASE_URL || window.location.origin,

  // 开发环境直接访问后端服务，生产环境通过Nginx代理
  fileService: import.meta.env.DEV
    ? (import.meta.env.VITE_DEV_FILE_API || 'http://localhost:10086')
    : '/api/file',

  aiService: import.meta.env.DEV
    ? (import.meta.env.VITE_DEV_AI_API || 'http://localhost:8088')
    : '/api/ai'
}

// 在生产环境中，如果baseURL被设置，使用完整URL
const getFullServiceURL = (servicePath) => {
  if (import.meta.env.PROD && API_CONFIG.baseURL && API_CONFIG.baseURL !== window.location.origin) {
    return API_CONFIG.baseURL + servicePath
  }
  return servicePath
}

// API URLs
export const API_URLS = {
  // 文件服务
  fileUpload: getFullServiceURL(`${API_CONFIG.fileService}/upload`),
  fileList: getFullServiceURL(`${API_CONFIG.fileService}/list`),
  fileImage: (filename) => getFullServiceURL(`${API_CONFIG.fileService}/image/${filename}`),
  fileDownload: (filename) => getFullServiceURL(`${API_CONFIG.fileService}/download/${filename}`),
  fileHeartbeat: getFullServiceURL(`${API_CONFIG.fileService}/heartbeat`),
  fileCleanup: (sessionId) => getFullServiceURL(`${API_CONFIG.fileService}/cleanup/${sessionId}`),

  // AI服务  
  aiGenerate: getFullServiceURL(`${API_CONFIG.aiService}/generate`),
  aiImage: (filename) => getFullServiceURL(`${API_CONFIG.aiService}/image/${filename}`),
  aiDownload: (filename) => getFullServiceURL(`${API_CONFIG.aiService}/download/${filename}`),
  aiList: getFullServiceURL(`${API_CONFIG.aiService}/list_generated`),
  aiHeartbeat: getFullServiceURL(`${API_CONFIG.aiService}/heartbeat`),
  aiCleanup: (sessionId) => getFullServiceURL(`${API_CONFIG.aiService}/cleanup/${sessionId}`)
}

export default API_CONFIG