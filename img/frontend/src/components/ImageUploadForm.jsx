import React, { useState, useCallback, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, Image as ImageIcon, Sparkles, Send, Database, Archive, Download } from 'lucide-react'
import axios from 'axios'
import Toast from './Toast'
import { API_URLS } from '../config/api'
import sessionManager from '../utils/sessionManager'
import './ImageUploadForm.css'

const ImageUploadForm = () => {
  const [prompt, setPrompt] = useState('将上传的照片转换成高分辨率的黑白肖像艺术作品，采用编辑类和艺术摄影风格。背景呈现柔和渐变效果，从中灰过渡到近乎纯白，营造出层次感与寂静氛围。')
  const [mode, setMode] = useState('upload') // 'upload' or 'generate'
  const [files, setFiles] = useState([])
  const [storedImages, setStoredImages] = useState([])
  const [selectedStoredImages, setSelectedStoredImages] = useState([])
  const [generatedImages, setGeneratedImages] = useState([])
  const [uploadedImages, setUploadedImages] = useState([])
  const [processing, setProcessing] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)
  const [toast, setToast] = useState({ isVisible: false, message: '', type: '' })
  const [previewModal, setPreviewModal] = useState({ isOpen: false, image: null })
  const [generationCounter, setGenerationCounter] = useState(0) // Add counter to force re-renders

  const showToast = (message, type) => {
    setToast({ isVisible: true, message, type })
    setTimeout(() => {
      setToast({ isVisible: false, message: '', type: '' })
    }, 4000)
  }

  const openImagePreview = (imageObj) => {
    setPreviewModal({ isOpen: true, image: imageObj })
  }

  const closeImagePreview = () => {
    setPreviewModal({ isOpen: false, image: null })
  }

  // Keyboard navigation for modal
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (previewModal.isOpen && e.key === 'Escape') {
        closeImagePreview()
      }
    }

    document.addEventListener('keydown', handleKeyPress)
    return () => document.removeEventListener('keydown', handleKeyPress)
  }, [previewModal.isOpen])

  // Debug: Monitor generated images changes
  useEffect(() => {
    console.log('Generated images state changed:', generatedImages.length, generatedImages)
  }, [generatedImages])

  const downloadSingleImage = async (imageObj) => {
    try {
      const response = await fetch(imageObj.downloadUrl, {
        headers: sessionManager.getHeaders()
      })
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = imageObj.filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      showToast('Image downloaded successfully', 'success')
    } catch (error) {
      console.error('Download failed:', error)
      showToast('Download failed', 'error')
    }
  }

  const downloadAllImages = async (images) => {
    if (images.length === 0) return

    showToast(`Starting download of ${images.length} images...`, 'info')

    try {
      for (let i = 0; i < images.length; i++) {
        const imageObj = images[i]
        const response = await fetch(imageObj.downloadUrl, {
          headers: sessionManager.getHeaders()
        })
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${i + 1}_${imageObj.filename}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)

        // Small delay between downloads to prevent browser blocking
        if (i < images.length - 1) {
          await new Promise(resolve => setTimeout(resolve, 500))
        }
      }
      showToast(`Successfully downloaded ${images.length} images`, 'success')
    } catch (error) {
      console.error('Batch download failed:', error)
      showToast('Some downloads failed', 'error')
    }
  }

  const handleModeSwitch = (newMode) => {
    setMode(newMode)
    
    // Clear generated images when switching to upload mode
    if (newMode === 'upload') {
      setGeneratedImages([])
      setUploadStatus(null)
    }
    
    // Clear uploaded images when switching to generate mode
    if (newMode === 'generate') {
      setUploadedImages([])
      loadStoredImages()
    }
  }

  const loadStoredImages = async () => {
    try {
      const response = await axios.get(API_URLS.fileList, {
        headers: sessionManager.getHeaders()
      })
      if (response.data.files) {
        setStoredImages(response.data.files)
      }
    } catch (error) {
      console.error('Failed to load stored images:', error)
      showToast('Failed to load stored images', 'error')
    }
  }

  const toggleStoredImageSelection = (filename) => {
    setSelectedStoredImages(prev => 
      prev.includes(filename)
        ? prev.filter(f => f !== filename)
        : [...prev, filename]
    )
  }

  const onDrop = useCallback((acceptedFiles) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      preview: URL.createObjectURL(file)
    }))
    setFiles(prev => [...prev, ...newFiles])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.svg']
    },
    multiple: true
  })

  const removeFile = (id) => {
    setFiles(prev => {
      const updated = prev.filter(f => f.id !== id)
      // Cleanup object URLs
      const removed = prev.find(f => f.id === id)
      if (removed) {
        URL.revokeObjectURL(removed.preview)
      }
      return updated
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (mode === 'upload') {
      return handleUploadToStorage()
    } else {
      return handleGenerateFromStorage()
    }
  }

  const handleUploadToStorage = async () => {
    if (files.length === 0) {
      setUploadStatus({ type: 'error', message: 'Please select at least one image' })
      return
    }

    setProcessing(true)
    setUploadStatus(null)

    try {
      const formData = new FormData()
      files.forEach(({ file }) => {
        formData.append('files', file)
      })
      
      const response = await axios.post(API_URLS.fileUpload, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          ...sessionManager.getHeaders()
        },
        timeout: 30000
      })

      console.log('Upload response:', response.data) // Debug log

      if (response.data.success) {
        console.log('Upload success branch triggered') // Debug log
        
        showToast(
          `🚀 Successfully uploaded ${response.data.uploaded_files.length} file(s) to Neural Storage`,
          'success'
        )
        
        // Show uploaded images instead of clearing files
        const uploadedImageObjects = response.data.uploaded_files.map(fileInfo => ({
          filename: fileInfo.saved_name,
          originalName: fileInfo.original_name,
          url: API_URLS.fileImage(fileInfo.saved_name),
          downloadUrl: API_URLS.fileDownload(fileInfo.saved_name)
        }))
        setUploadedImages(uploadedImageObjects)
        
        // Clear the upload files
        setFiles([])
        
        // Auto switch to generate mode after a brief delay
        setTimeout(() => {
          console.log('Auto switching to generate mode') // Debug log
          handleModeSwitch('generate')
        }, 2000) // 2 second delay to let user see the uploaded images
        
        setUploadStatus({ 
          type: 'success', 
          message: `✅ Uploaded ${response.data.uploaded_files.length} file(s) successfully! Switching to Generate mode...` 
        })
      } else {
        setUploadStatus({ type: 'error', message: 'Upload failed. Please try again.' })
      }
      
    } catch (error) {
      console.error('Upload error:', error)
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.error || error.message || 'Upload failed. Please try again.'
      })
    } finally {
      setProcessing(false)
    }
  }

  const handleGenerateFromStorage = async () => {
    if (!prompt.trim()) {
      setUploadStatus({ type: 'error', message: 'Please enter a prompt' })
      return
    }
    
    if (selectedStoredImages.length === 0) {
      setUploadStatus({ type: 'error', message: 'Please select at least one stored image' })
      return
    }

    setProcessing(true)
    setUploadStatus(null)
    // Don't clear existing generated images - append new ones instead

    try {
      const formData = new FormData()
      
      // Download selected images and add to form data
      for (const filename of selectedStoredImages) {
        const imageResponse = await axios.get(API_URLS.fileImage(filename), {
          responseType: 'blob',
          headers: sessionManager.getHeaders()
        })
        formData.append('images', imageResponse.data, filename)
      }
      
      formData.append('prompt', prompt)
      
      const response = await axios.post(API_URLS.aiGenerate, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          ...sessionManager.getHeaders()
        },
        timeout: 300000 // 5 minutes timeout for processing
      })

      if (response.data.success) {
        setUploadStatus({
          type: 'success',
          message: `Successfully processed ${response.data.processed_count} image(s)! ${response.data.text_response}`
        })

        console.log('Generation response:', response.data) // Debug log

        if (response.data.generated_files && response.data.generated_files.length > 0) {
          // Transform filenames to full objects with URLs
          const baseTimestamp = Date.now()
          const generatedImageObjects = response.data.generated_files.map((filename, idx) => ({
            id: `${baseTimestamp}-${Math.random().toString(36).substr(2, 9)}-${idx}-${generationCounter}`, // More unique ID with counter
            filename: filename,
            url: API_URLS.aiImage(filename),
            downloadUrl: API_URLS.aiDownload(filename)
          }))

          console.log('New generated images:', generatedImageObjects) // Debug log

          // Append new images to existing ones instead of replacing
          setGeneratedImages(prev => {
            console.log('Previous images:', prev) // Debug log
            const combined = [...prev, ...generatedImageObjects]
            console.log('Combined images:', combined) // Debug log
            console.log('Total images after combination:', combined.length) // Debug log

            // Check for duplicate IDs
            const ids = combined.map(img => img.id)
            const uniqueIds = new Set(ids)
            if (ids.length !== uniqueIds.size) {
              console.warn('Warning: Duplicate IDs detected!', ids)
            }

            // Force re-render by creating a completely new array
            return combined.slice()
          })

          // Increment generation counter to ensure unique IDs next time
          setGenerationCounter(prev => prev + 1)
        }
      } else {
        setUploadStatus({
          type: 'error',
          message: response.data.error || 'Generation failed'
        })
      }
      
      // Clear selection
      setSelectedStoredImages([])
      
    } catch (error) {
      console.error('Generation error:', error)
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.error || error.message || 'Generation failed. Please try again.'
      })
    } finally {
      setProcessing(false)
    }
  }

  return (
    <>
      <div className="upload-form-container">
        <div className="upload-card">
          <div className="card-header">
            <Sparkles className="header-icon" size={24} />
            <h2>Create with AI</h2>
            <p>{mode === 'upload' ? 'Upload images to neural storage' : 'Generate from stored images'}</p>
            
            {/* Mode Toggle */}
            <div className="mode-toggle">
              <button
                type="button"
                className={`mode-btn ${mode === 'upload' ? 'active' : ''}`}
                onClick={() => handleModeSwitch('upload')}
              >
                <Database size={16} />
                Upload & Store
              </button>
              <button
                type="button"
                className={`mode-btn ${mode === 'generate' ? 'active' : ''}`}
                onClick={() => handleModeSwitch('generate')}
              >
                <Sparkles size={16} />
                Generate AI Art
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="upload-form">
            {/* Uploaded Images - Show in upload mode after successful upload */}
            {mode === 'upload' && uploadedImages.length > 0 && (
              <div className="uploaded-section">
                <div className="uploaded-header">
                  <h3 className="uploaded-title">Successfully Uploaded ({uploadedImages.length})</h3>
                  <button
                    type="button"
                    className="download-all-btn"
                    onClick={() => downloadAllImages(uploadedImages)}
                    title="Download all uploaded images"
                  >
                    <Download size={16} />
                    Download All
                  </button>
                </div>
                <div className="uploaded-grid">
                  {uploadedImages.map((imageObj, index) => (
                    <div key={index} className="uploaded-item">
                      <div className="uploaded-image-container">
                        <img
                          src={imageObj.url}
                          alt={`Uploaded ${imageObj.filename}`}
                          className="uploaded-image"
                          loading="lazy"
                          onClick={() => openImagePreview(imageObj)}
                        />
                        <div className="uploaded-image-overlay">
                          <button
                            type="button"
                            className="preview-btn"
                            onClick={() => openImagePreview(imageObj)}
                            title="Preview image"
                          >
                            <ImageIcon size={16} />
                          </button>
                          <button
                            type="button"
                            className="download-btn"
                            onClick={() => downloadSingleImage(imageObj)}
                            title="Download image"
                          >
                            <Download size={16} />
                          </button>
                        </div>
                      </div>
                      <div className="uploaded-image-info">
                        <p className="uploaded-filename" title={imageObj.filename}>
                          {imageObj.originalName && imageObj.originalName.length > 25 ? `${imageObj.originalName.substring(0, 25)}...` : imageObj.originalName || imageObj.filename}
                        </p>
                        <small>Successfully Uploaded</small>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Show prompt input only in generate mode */}
            {mode === 'generate' && (
              <div className="form-group">
                <label htmlFor="prompt" className="form-label">
                  <Sparkles size={16} />
                  Your Creative Prompt
                </label>
                <textarea
                  id="prompt"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe how you want to transform your images... 

Examples:
• Convert to a vintage black and white portrait
• Transform into a watercolor painting
• Create a futuristic cyberpunk version"
                  className="prompt-textarea"
                  rows={6}
                />
                <div className="char-count">
                  {prompt.length} characters
                </div>
              </div>
            )}

            {/* Upload Mode */}
            {mode === 'upload' && (
              <>
                <div className="form-group">
                  <label className="form-label">
                    <Upload size={16} />
                    Upload to Neural Storage
                  </label>
                  
                  <div
                    {...getRootProps()}
                    className={`dropzone ${isDragActive ? 'dropzone-active' : ''}`}
                  >
                    <input {...getInputProps()} />
                    <div className="dropzone-content">
                      <Database size={48} className="dropzone-icon" />
                      <h3>
                        {isDragActive
                          ? 'Drop your images here...'
                          : 'Drag & drop images or click to browse'
                        }
                      </h3>
                      <p>Supports PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF, SVG</p>
                      <p className="file-limit">Max 16MB per file</p>
                    </div>
                  </div>
                </div>

                {/* File Preview for Upload */}
                {files.length > 0 && (
                  <div className="file-preview-section">
                    <h3 className="preview-title">Selected Images ({files.length})</h3>
                    <div className="file-preview-grid">
                      {files.map(({ id, file, preview }) => (
                        <div key={id} className="file-preview-item">
                          <div className="preview-image-container">
                            <img src={preview} alt={file.name} className="preview-image" />
                            <button
                              type="button"
                              onClick={() => removeFile(id)}
                              className="remove-file-btn"
                              aria-label="Remove file"
                            >
                              <X size={16} />
                            </button>
                          </div>
                          <div className="file-info">
                            <p className="file-name" title={file.name}>
                              {file.name.length > 20 ? `${file.name.substring(0, 20)}...` : file.name}
                            </p>
                            <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Generate Mode - Show Stored Images */}
            {mode === 'generate' && (
              <div className="form-group">
                <label className="form-label">
                  <Archive size={16} />
                  Select from Neural Storage ({storedImages.length} available)
                </label>
                
                {storedImages.length === 0 ? (
                  <div className="empty-storage">
                    <Database size={48} className="empty-icon" />
                    <h3>No images in storage</h3>
                    <p>Upload some images first to generate AI art</p>
                    <button 
                      type="button" 
                      className="switch-mode-btn"
                      onClick={() => handleModeSwitch('upload')}
                    >
                      <Upload size={16} />
                      Upload Images
                    </button>
                  </div>
                ) : (
                  <div className="stored-images-grid">
                    {storedImages.map((image) => (
                      <div 
                        key={image.filename}
                        className={`stored-image-item ${
                          selectedStoredImages.includes(image.filename) ? 'selected' : ''
                        }`}
                        onClick={() => toggleStoredImageSelection(image.filename)}
                      >
                        <img 
                          src={API_URLS.fileImage(image.filename)} 
                          alt={image.original_name} 
                          className="stored-image"
                        />
                        <div className="stored-image-info">
                          <p className="stored-name">{image.original_name}</p>
                          <p className="stored-size">{(image.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                        {selectedStoredImages.includes(image.filename) && (
                          <div className="selection-indicator">
                            <Sparkles size={16} />
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Generated Images - Only show in generate mode */}
            {mode === 'generate' && generatedImages.length > 0 && (
              <div className="generated-section">
                {/* Debug info - remove in production */}
                {console.log('Rendering generated images, count:', generatedImages.length)}
                {console.log('Generated images array:', generatedImages)}

                <div className="generated-header">
                  <h3 className="generated-title">Generated Images ({generatedImages.length})</h3>
                  <div className="generated-header-actions">
                    <button
                      type="button"
                      className="clear-all-btn"
                      onClick={() => setGeneratedImages([])}
                      title="Clear all generated images"
                    >
                      <X size={16} />
                      Clear All
                    </button>
                    <button
                      type="button"
                      className="download-all-btn"
                      onClick={() => downloadAllImages(generatedImages)}
                      title="Download all generated images"
                    >
                      <Download size={16} />
                      Download All
                    </button>
                  </div>
                </div>
                <div className="generated-grid" key={`generated-grid-${generationCounter}`}>
                  {generatedImages.map((imageObj) => (
                    <div key={imageObj.id} className="generated-item">
                      <div className="generated-image-container">
                        <img
                          src={imageObj.url}
                          alt={`Generated ${imageObj.filename}`}
                          className="generated-image"
                          loading="lazy"
                          onClick={() => openImagePreview(imageObj)}
                        />
                        <div className="generated-image-overlay">
                          <button
                            type="button"
                            className="preview-btn"
                            onClick={() => openImagePreview(imageObj)}
                            title="Preview image"
                          >
                            <ImageIcon size={16} />
                          </button>
                          <button
                            type="button"
                            className="download-btn"
                            onClick={() => downloadSingleImage(imageObj)}
                            title="Download image"
                          >
                            <Download size={16} />
                          </button>
                        </div>
                      </div>
                      <div className="generated-image-info">
                        <p className="generated-filename" title={imageObj.filename}>
                          {imageObj.filename.length > 25 ? `${imageObj.filename.substring(0, 25)}...` : imageObj.filename}
                        </p>
                        <small>AI Generated Image</small>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Status Messages */}
            {uploadStatus && (
              <div className={`status-message ${uploadStatus.type}`}>
                {uploadStatus.message}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={processing || (mode === 'upload' && files.length === 0) || (mode === 'generate' && (selectedStoredImages.length === 0 || !prompt.trim()))}
              className="submit-btn"
            >
              {processing ? (
                <>
                  <div className="spinner" />
                  {mode === 'upload' ? 'Uploading to Storage...' : 'Generating with AI...'}
                </>
              ) : (
                <>
                  <Send size={20} />
                  {mode === 'upload' ? 'Upload to Storage' : 'Generate with AI'}
                </>
              )}
            </button>
          </form>
        </div>
      </div>

      <Toast
        message={toast.message}
        type={toast.type}
        isVisible={toast.isVisible}
        onClose={() => setToast({ isVisible: false, message: '', type: '' })}
      />

      {/* Image Preview Modal */}
      {previewModal.isOpen && previewModal.image && (
        <div className="modal-overlay" onClick={closeImagePreview}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{previewModal.image.originalName || previewModal.image.filename}</h3>
              <button
                className="modal-close-btn"
                onClick={closeImagePreview}
                title="Close preview"
              >
                <X size={24} />
              </button>
            </div>
            <div className="modal-body">
              <img
                src={previewModal.image.url}
                alt={previewModal.image.filename}
                className="modal-image"
              />
            </div>
            <div className="modal-footer">
              <button
                className="modal-download-btn"
                onClick={() => {
                  downloadSingleImage(previewModal.image)
                  closeImagePreview()
                }}
              >
                <Download size={16} />
                Download Image
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default ImageUploadForm