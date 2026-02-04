import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Sparkles, Image, X, Check, CheckSquare, Square } from 'lucide-react'
import axios from 'axios'
import Toast from './Toast'
import ImageCarousel from './ImageCarousel'
import { API_URLS } from '../config/api'
import sessionManager from '../utils/sessionManager'
import './FileUploader.css'

const ImageUploadForm = () => {
    const [uploadedImages, setUploadedImages] = useState([])
    const [selectedImages, setSelectedImages] = useState(new Set())
    const [generatedImages, setGeneratedImages] = useState([])
    const [prompt, setPrompt] = useState('')
    const [isUploading, setIsUploading] = useState(false)
    const [isGenerating, setIsGenerating] = useState(false)
    const [toast, setToast] = useState({ isVisible: false, message: '', type: '' })
    const [previewImage, setPreviewImage] = useState(null)

    const showToast = (message, type) => {
        setToast({ isVisible: true, message, type })
        setTimeout(() => {
            setToast(prev => ({ ...prev, isVisible: false }))
        }, 4000)
    }

    const onDrop = useCallback(async (acceptedFiles) => {
        if (acceptedFiles.length === 0) return

        setIsUploading(true)
        const formData = new FormData()
        acceptedFiles.forEach(file => {
            formData.append('files', file)
        })

        try {
            const response = await axios.post(API_URLS.fileUpload, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    ...sessionManager.getHeaders()
                },
                timeout: 30000
            })

            if (response.data.success) {
                const newImages = response.data.uploaded_files.map(file => ({
                    id: file.saved_name,
                    filename: file.saved_name,
                    originalName: file.original_name,
                    url: API_URLS.fileImage(file.saved_name),
                    size: file.size
                }))
                setUploadedImages(prev => [...prev, ...newImages])
                // Auto-select newly uploaded images
                setSelectedImages(prev => {
                    const newSet = new Set(prev)
                    newImages.forEach(img => newSet.add(img.id))
                    return newSet
                })
                showToast(`Uploaded ${acceptedFiles.length} image(s)`, 'success')
            }
        } catch (error) {
            console.error('Upload error:', error)
            showToast(error.response?.data?.error || 'Upload failed', 'error')
        } finally {
            setIsUploading(false)
        }
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'] },
        multiple: true
    })

    const toggleImageSelection = (id) => {
        setSelectedImages(prev => {
            const newSet = new Set(prev)
            if (newSet.has(id)) {
                newSet.delete(id)
            } else {
                newSet.add(id)
            }
            return newSet
        })
    }

    const selectAllImages = () => {
        setSelectedImages(new Set(uploadedImages.map(img => img.id)))
    }

    const deselectAllImages = () => {
        setSelectedImages(new Set())
    }

    const handleGenerate = async () => {
        if (!prompt.trim()) {
            showToast('Please enter a prompt', 'warning')
            return
        }

        // Get selected images for generation
        const imagesToUse = uploadedImages
            .filter(img => selectedImages.has(img.id))
            .map(img => img.filename)

        setIsGenerating(true)
        try {
            const requestData = {
                prompt: prompt.trim(),
                images: imagesToUse
            }

            const response = await axios.post(API_URLS.aiGenerate, requestData, {
                headers: sessionManager.getHeaders(),
                timeout: 300000
            })

            if (response.data.success && response.data.generated_images) {
                const newGenerated = response.data.generated_images.map((img, idx) => ({
                    id: `gen_${Date.now()}_${idx}`,
                    filename: img.filename,
                    url: API_URLS.aiImage(img.filename)
                }))
                setGeneratedImages(prev => [...prev, ...newGenerated])
                showToast('Image generated successfully!', 'success')
            } else if (response.data.text_response) {
                showToast(response.data.text_response.substring(0, 100), 'warning')
            }
        } catch (error) {
            console.error('Generation error:', error)
            showToast(error.response?.data?.error || 'Generation failed', 'error')
        } finally {
            setIsGenerating(false)
        }
    }

    const removeUploadedImage = (id, e) => {
        e.stopPropagation()
        setUploadedImages(prev => prev.filter(img => img.id !== id))
        setSelectedImages(prev => {
            const newSet = new Set(prev)
            newSet.delete(id)
            return newSet
        })
    }

    const handleDownload = async (image) => {
        try {
            const response = await axios.get(API_URLS.aiDownload(image.filename), {
                responseType: 'blob',
                headers: sessionManager.getHeaders()
            })
            const url = window.URL.createObjectURL(response.data)
            const link = document.createElement('a')
            link.href = url
            link.download = image.filename
            link.click()
            window.URL.revokeObjectURL(url)
        } catch (error) {
            showToast('Download failed', 'error')
        }
    }

    const handlePreview = (image) => {
        setPreviewImage(image)
    }

    const selectedCount = selectedImages.size
    const allSelected = uploadedImages.length > 0 && selectedCount === uploadedImages.length

    return (
        <div className="image-upload-form">
            {/* Main Grid Layout */}
            <div className="main-content-grid">
                {/* Left Column: Upload Input & List */}
                <div className="input-section">
                    {/* Upload Area */}
                    <div
                        {...getRootProps()}
                        className={`dropzone ${isDragActive ? 'active' : ''} ${isUploading ? 'uploading' : ''}`}
                    >
                        <input {...getInputProps()} />
                        <div className="dropzone-content">
                            {isUploading ? (
                                <>
                                    <div className="upload-spinner" />
                                    <p>Uploading...</p>
                                </>
                            ) : isDragActive ? (
                                <>
                                    <Upload size={48} />
                                    <p>Drop images here</p>
                                </>
                            ) : (
                                <>
                                    <Image size={48} />
                                    <p>Drag & drop images or click to browse</p>
                                    <span className="dropzone-hint">PNG, JPG, GIF, WEBP supported</span>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Uploaded Images Preview with Selection */}
                    <div className={`uploaded-preview ${uploadedImages.length === 0 ? 'empty' : ''}`}>
                        <div className="uploaded-header">
                            <h3>Uploaded ({uploadedImages.length})</h3>
                            {uploadedImages.length > 0 && (
                                <div className="selection-controls">
                                    <span className="selection-count">
                                        {selectedCount} selected
                                    </span>
                                    <button
                                        className="select-btn"
                                        onClick={allSelected ? deselectAllImages : selectAllImages}
                                    >
                                        {allSelected ? (
                                            <>
                                                <Square size={16} />
                                                Deselect
                                            </>
                                        ) : (
                                            <>
                                                <CheckSquare size={16} />
                                                Select All
                                            </>
                                        )}
                                    </button>
                                </div>
                            )}
                        </div>
                        {uploadedImages.length > 0 ? (
                            <div className="image-grid selectable">
                                {uploadedImages.map(img => (
                                    <div
                                        key={img.id}
                                        className={`image-thumb ${selectedImages.has(img.id) ? 'selected' : ''}`}
                                        onClick={() => toggleImageSelection(img.id)}
                                    >
                                        <img src={img.url} alt={img.originalName} />
                                        <div className="selection-checkbox">
                                            {selectedImages.has(img.id) ? (
                                                <Check size={14} />
                                            ) : null}
                                        </div>
                                        <button
                                            className="remove-btn"
                                            onClick={(e) => removeUploadedImage(img.id, e)}
                                        >
                                            <X size={14} />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="empty-state">
                                <Image size={32} />
                                <p>No images uploaded</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Column: Generated Output */}
                <div className="output-section">
                    {generatedImages.length > 0 ? (
                        <ImageCarousel
                            images={generatedImages}
                            onDownload={handleDownload}
                            onPreview={handlePreview}
                            onClose={() => setGeneratedImages([])}
                        />
                    ) : (
                        <div className="generated-preview empty">
                            <div className="empty-state">
                                <Sparkles size={32} />
                                <p>No images generated</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Prompt Input */}
            <div className="prompt-section">
                <div className="prompt-input-wrapper">
                    <input
                        type="text"
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder={selectedCount > 0
                            ? `Describe what you want to generate (${selectedCount} image${selectedCount > 1 ? 's' : ''} selected)...`
                            : "Describe what you want to generate..."
                        }
                        className="prompt-input"
                        onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
                    />
                    <button
                        className="generate-btn"
                        onClick={handleGenerate}
                        disabled={isGenerating}
                    >
                        {isGenerating ? (
                            <>
                                <div className="btn-spinner" />
                                Generating...
                            </>
                        ) : (
                            <>
                                <Sparkles size={20} />
                                Generate
                            </>
                        )}
                    </button>
                </div>
            </div>

            {/* Image Preview Modal */}
            {previewImage && (
                <div className="preview-modal" onClick={() => setPreviewImage(null)}>
                    <div className="preview-content" onClick={e => e.stopPropagation()}>
                        <button className="preview-close" onClick={() => setPreviewImage(null)}>
                            <X size={24} />
                        </button>
                        <img src={previewImage.url} alt={previewImage.filename} />
                        <div className="preview-actions">
                            <button onClick={() => handleDownload(previewImage)}>
                                Download
                            </button>
                        </div>
                    </div>
                </div>
            )}

            <Toast
                message={toast.message}
                type={toast.type}
                isVisible={toast.isVisible}
                onClose={() => setToast(prev => ({ ...prev, isVisible: false }))}
            />
        </div>
    )
}

export default ImageUploadForm
