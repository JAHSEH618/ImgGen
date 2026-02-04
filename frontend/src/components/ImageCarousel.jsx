import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Download, ImageIcon, X, Share2 } from 'lucide-react';
import './FileUploader.css'; // Reusing styles and adding specific carousel styles

const ImageCarousel = ({ images, onDownload, onPreview, onShare, onClose }) => {
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        // Reset index when images array changes significantly
        if (currentIndex >= images.length) {
            setCurrentIndex(0);
        }
    }, [images.length]);

    const nextSlide = () => {
        setCurrentIndex((prev) => (prev + 1) % images.length);
    };

    const prevSlide = () => {
        setCurrentIndex((prev) => (prev - 1 + images.length) % images.length);
    };

    const currentImage = images[currentIndex];

    if (!currentImage) return null;

    return (
        <div className="carousel-container">
            <div className="carousel-header">
                <div className="carousel-counter">
                    Generated Results ({currentIndex + 1} / {images.length})
                </div>
                <button onClick={onClose} className="carousel-close-btn" title="Close Carousel">
                    <X size={20} />
                </button>
            </div>

            <div className="carousel-main">
                <button
                    onClick={prevSlide}
                    className="carousel-nav-btn prev"
                    disabled={images.length <= 1}
                >
                    <ChevronLeft size={32} />
                </button>

                <div className="carousel-image-wrapper">
                    <img
                        src={currentImage.url}
                        alt={currentImage.filename}
                        className="carousel-image"
                        onClick={() => onPreview(currentImage)}
                    />
                </div>

                <button
                    onClick={nextSlide}
                    className="carousel-nav-btn next"
                    disabled={images.length <= 1}
                >
                    <ChevronRight size={32} />
                </button>
            </div>

            <div className="carousel-actions" style={{ justifyContent: 'center' }}>
                <div className="carousel-buttons">
                    <button
                        onClick={() => onPreview(currentImage)}
                        className="action-btn secondary"
                        title="View Fullscreen"
                    >
                        <ImageIcon size={18} />
                        View
                    </button>
                    {onShare && (
                        <button
                            onClick={() => onShare(currentImage)}
                            className="action-btn secondary"
                            title="Share Image"
                        >
                            <Share2 size={18} />
                            Share
                        </button>
                    )}
                    <button
                        onClick={() => onDownload(currentImage)}
                        className="action-btn primary"
                        title="Download Image"
                    >
                        <Download size={18} />
                        Download
                    </button>
                </div>
            </div>

            {/* Thumbnails */}
            {images.length > 1 && (
                <div className="carousel-thumbnails">
                    {images.map((img, idx) => (
                        <div
                            key={img.id || idx}
                            className={`thumbnail-item ${idx === currentIndex ? 'active' : ''}`}
                            onClick={() => setCurrentIndex(idx)}
                        >
                            <img src={img.url} alt={`Thumbnail ${idx + 1}`} />
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ImageCarousel;
