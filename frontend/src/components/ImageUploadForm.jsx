import React, { useState, useCallback, useRef, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Sparkles, Image, X, Check, CheckSquare, Square, Share2 } from 'lucide-react'
import axios from 'axios'
import Toast from './Toast'
import ImageCarousel from './ImageCarousel'
import { API_URLS } from '../config/api'
import sessionManager from '../utils/sessionManager'
import './FileUploader.css'

const ImageUploadForm = () => {
    const [uploadedImages, setUploadedImages] = useState([])
    const [selectedImages, setSelectedImages] = useState(new Set())
    const [activeUploadId, setActiveUploadId] = useState(null)
    const [generatedImages, setGeneratedImages] = useState([])
    const [prompt, setPrompt] = useState('')
    const [isUploading, setIsUploading] = useState(false)
    const [isGenerating, setIsGenerating] = useState(false)
    const [toast, setToast] = useState({ isVisible: false, message: '', type: '' })
    const [previewImage, setPreviewImage] = useState(null)

    // Refs for cleanup
    const toastTimeoutRef = useRef(null)
    const abortControllerRef = useRef(null)

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (toastTimeoutRef.current) clearTimeout(toastTimeoutRef.current)
            if (abortControllerRef.current) abortControllerRef.current.abort()
        }
    }, [])

    const showToast = (message, type) => {
        if (toastTimeoutRef.current) clearTimeout(toastTimeoutRef.current)
        setToast({ isVisible: true, message, type })
        toastTimeoutRef.current = setTimeout(() => {
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
                const sessionId = sessionManager.getSessionId()
                const newImages = response.data.uploaded_files.map(file => ({
                    id: file.saved_name,
                    filename: file.saved_name,
                    originalName: file.original_name,
                    url: API_URLS.fileImage(file.saved_name, sessionId),
                    size: file.size
                }))
                setUploadedImages(prev => [...prev, ...newImages])
                // Auto-select newly uploaded images
                setSelectedImages(prev => {
                    const newSet = new Set(prev)
                    newImages.forEach(img => newSet.add(img.id))
                    return newSet
                })
                // Set the last uploaded image as active
                if (newImages.length > 0) {
                    setActiveUploadId(newImages[newImages.length - 1].id)
                }
                showToast(`Uploaded ${acceptedFiles.length} image(s)`, 'success')
            }
        } catch (error) {
            console.error('Upload error:', error)
            showToast(error.response?.data?.error || 'Upload failed', 'error')
        } finally {
            setIsUploading(false)
        }
    }, [])

    const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
        onDrop,
        accept: { 'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'] },
        multiple: true,
        noClick: true // We will handle clicks manually to avoid conflicts
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
        if (selectedImages.size === 0) {
            showToast('Please select at least one image to generate', 'warning')
            return
        }

        if (!prompt.trim()) {
            showToast('Please enter a prompt', 'warning')
            return
        }

        // Get selected images for generation
        const imagesToUse = uploadedImages
            .filter(img => selectedImages.has(img.id))
            .map(img => img.filename)

        // Create abort controller for this request
        abortControllerRef.current = new AbortController()

        setIsGenerating(true)
        try {
            const requestData = {
                prompt: prompt.trim(),
                images: imagesToUse
            }

            const response = await axios.post(API_URLS.aiGenerate, requestData, {
                headers: sessionManager.getHeaders(),
                timeout: 300000,
                signal: abortControllerRef.current.signal
            })

            if (response.data.success && response.data.generated_images) {
                const sessionId = sessionManager.getSessionId()
                const newGenerated = response.data.generated_images.map((img, idx) => ({
                    id: `gen_${Date.now()}_${idx}`,
                    filename: img.filename,
                    url: API_URLS.aiImage(img.filename, sessionId)
                }))
                setGeneratedImages(prev => [...prev, ...newGenerated])
                showToast('Image generated successfully!', 'success')
            } else {
                // Handle cases where success is false (e.g. safety filters, no images returned)
                const errorMsg = response.data.message || response.data.text_response || 'Generation produced no images'
                showToast(errorMsg, 'warning')
            }
        } catch (error) {
            // Don't show error for aborted requests
            if (axios.isCancel(error) || error.name === 'CanceledError') {
                console.log('Request was cancelled')
                return
            }
            console.error('Generation error:', error)
            showToast(error.response?.data?.error || 'Generation failed', 'error')
        } finally {
            setIsGenerating(false)
            abortControllerRef.current = null
        }
    }

    const removeUploadedImage = (id, e) => {
        if (e) e.stopPropagation()
        setUploadedImages(prev => {
            const filtered = prev.filter(img => img.id !== id)
            // If we removed the active image, set new active
            if (id === activeUploadId) {
                if (filtered.length > 0) {
                    setActiveUploadId(filtered[filtered.length - 1].id)
                } else {
                    setActiveUploadId(null)
                }
            }
            return filtered
        })
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

    const handleShare = async (image) => {
        if (!image) return

        try {
            if (navigator.share) {
                await navigator.share({
                    title: 'Generated Image',
                    text: 'Check out this AI generated image!',
                    url: image.url
                })
            } else {
                await navigator.clipboard.writeText(image.url)
                showToast('Link copied to clipboard', 'success')
            }
        } catch (error) {
            console.error('Share failed:', error)
            // Fallback for user cancellation or other errors
            if (error.name !== 'AbortError') {
                showToast('Share failed', 'error')
            }
        }
    }

    const handlePreview = (image) => {
        setPreviewImage(image)
    }

    const selectedCount = selectedImages.size
    const allSelected = uploadedImages.length > 0 && selectedCount === uploadedImages.length
    const activeImg = uploadedImages.find(img => img.id === activeUploadId) || uploadedImages[uploadedImages.length - 1]

    return (
        <div className="image-upload-form">
            {/* Main Grid Layout */}
            <div className="main-content-grid">
                {/* Left Column: Upload Input & List */}
                <div className="input-section">
                    <div
                        {...getRootProps()}
                        className="uploaded-carousel-container"
                        onClick={(e) => e.stopPropagation()} // Prevent bubble up
                    >
                        <input {...getInputProps()} />

                        {/* 1. Main Preview Area */}
                        <div className="uploaded-main-preview">
                            {uploadedImages.length > 0 ? (
                                (() => {
                                    const activeImg = uploadedImages.find(img => img.id === activeUploadId) || uploadedImages[uploadedImages.length - 1]
                                    return (
                                        <div className="main-preview-wrapper">
                                            <img src={activeImg.url} alt={activeImg.originalName} className="main-preview-image" decoding="async" />
                                            <div className="main-preview-info">
                                                <button
                                                    className="remove-active-btn"
                                                    onClick={(e) => {
                                                        e.stopPropagation()
                                                        removeUploadedImage(activeImg.id, e)
                                                    }}
                                                    title="Remove image"
                                                >
                                                    <X size={16} />
                                                </button>
                                                <div className="info-badges">
                                                    <button
                                                        className={`select-badge-btn ${selectedImages.has(activeImg.id) ? 'selected' : ''}`}
                                                        onClick={(e) => {
                                                            e.stopPropagation()
                                                            toggleImageSelection(activeImg.id)
                                                        }}
                                                    >
                                                        {selectedImages.has(activeImg.id) ? <CheckSquare size={16} /> : <Square size={16} />}
                                                        {selectedImages.has(activeImg.id) ? 'Selected' : 'Use'}
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    )
                                })()
                            ) : (
                                <div
                                    className="upload-placeholder"
                                    onClick={open}
                                >
                                    <div className="placeholder-content">
                                        <Image size={64} />
                                        <p>Drag & drop images here</p>
                                        <p className="sub-text">or click to browse</p>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* 2. Thumbnail Strip & Mini Dropzone */}
                        <div className="uploaded-thumbnails-strip">
                            {uploadedImages.map(img => (
                                <div
                                    key={img.id}
                                    className={`strip-thumb ${activeUploadId === img.id ? 'active' : ''} ${selectedImages.has(img.id) ? 'selected' : ''}`}
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        setActiveUploadId(img.id)
                                    }}
                                >
                                    <img src={img.url} alt={img.originalName} loading="lazy" decoding="async" />
                                    <div
                                        className={`thumb-checkbox ${selectedImages.has(img.id) ? 'checked' : ''}`}
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            toggleImageSelection(img.id)
                                        }}
                                        title={selectedImages.has(img.id) ? "Unselect" : "Select"}
                                    >
                                        {selectedImages.has(img.id) && <Check size={10} />}
                                    </div>
                                </div>
                            ))}

                            {/* Mini Dropzone at the end */}
                            <div
                                className={`mini-dropzone ${isDragActive ? 'active' : ''}`}
                                title="Add more images"
                                onClick={open}
                            >
                                <Upload size={20} />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Generated Output */}
                <div className="output-section">
                    {generatedImages.length > 0 ? (
                        <ImageCarousel
                            images={generatedImages}
                            onDownload={handleDownload}
                            onPreview={handlePreview}
                            onShare={handleShare}
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
                        onClick={isGenerating ? () => abortControllerRef.current?.abort() : handleGenerate}
                        style={isGenerating ? { background: 'var(--text-tertiary)' } : {}}
                    >
                        {isGenerating ? (
                            <>
                                <X size={20} />
                                Cancel
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
                            <button onClick={() => handleShare(previewImage)} className="secondary">
                                <Share2 size={16} /> Share
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
