import React, { useState, useRef } from 'react'
import { Upload, Database, Zap } from 'lucide-react'
import axios from 'axios'
import Toast from './Toast'
import { API_URLS } from '../config/api'
import './FileUploader.css'

const FileUploader = () => {
  const [isUploading, setIsUploading] = useState(false)
  const [toast, setToast] = useState({ isVisible: false, message: '', type: '' })
  const fileInputRef = useRef(null)

  const showToast = (message, type) => {
    setToast({ isVisible: true, message, type })
    setTimeout(() => {
      setToast(prev => ({ ...prev, isVisible: false }))
    }, 4000)
  }

  const handleUpload = async (files) => {
    if (!files || files.length === 0) {
      showToast('Please select files to upload', 'warning')
      return
    }

    setIsUploading(true)

    try {
      const formData = new FormData()
      Array.from(files).forEach(file => {
        formData.append('files', file)
      })

      const response = await axios.post(API_URLS.fileUpload, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000
      })

      if (response.data.success) {
        showToast(
          `🚀 Successfully uploaded ${response.data.uploaded_files.length} file(s) to Neural Storage`,
          'success'
        )
      } else {
        showToast('Upload failed. Please try again.', 'error')
      }

      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }

    } catch (error) {
      console.error('Upload error:', error)
      showToast(
        `Upload failed: ${error.response?.data?.error || error.message}`,
        'error'
      )
    } finally {
      setIsUploading(false)
    }
  }

  const handleFileSelect = (event) => {
    const files = event.target.files
    handleUpload(files)
  }

  const handleButtonClick = () => {
    fileInputRef.current?.click()
  }

  const handleDrop = (event) => {
    event.preventDefault()
    const files = event.dataTransfer.files
    handleUpload(files)
  }

  const handleDragOver = (event) => {
    event.preventDefault()
  }

  return (
    <>
      <div className="file-uploader">
        <button
          className="upload-btn-neural"
          onClick={handleButtonClick}
          disabled={isUploading}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="btn-content">
            <div className="btn-icon">
              {isUploading ? (
                <div className="neural-spinner">
                  <Zap size={20} />
                </div>
              ) : (
                <Database size={20} />
              )}
            </div>
            <div className="btn-text">
              <span className="btn-main-text">
                {isUploading ? 'Neural Processing...' : 'Upload to Storage'}
              </span>
              <span className="btn-sub-text">
                {isUploading ? 'Transmitting data packets' : 'Click or drop files here'}
              </span>
            </div>
          </div>
          <div className="btn-circuits">
            <div className="circuit-line circuit-line-1"></div>
            <div className="circuit-line circuit-line-2"></div>
            <div className="circuit-line circuit-line-3"></div>
          </div>
        </button>
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        <div className="upload-info">
          <div className="info-item">
            <Upload size={14} />
            <span>Multi-file support enabled</span>
          </div>
          <div className="info-item">
            <Zap size={14} />
            <span>Secure transport protocol</span>
          </div>
        </div>
      </div>

      <Toast
        message={toast.message}
        type={toast.type}
        isVisible={toast.isVisible}
        onClose={() => setToast(prev => ({ ...prev, isVisible: false }))}
      />
    </>
  )
}

export default FileUploader