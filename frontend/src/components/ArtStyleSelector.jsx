import React, { useState } from 'react'
import { X } from 'lucide-react'
import './ArtStyleSelector.css'

import { ART_STYLES } from '../config/artStyles'

// Display only first 6 styles in the main view


const ArtStyleSelector = ({ selectedStyle, onSelectStyle }) => {
    const [isModalOpen, setIsModalOpen] = useState(false)

    const handleStyleClick = (styleId) => {
        onSelectStyle(styleId === selectedStyle ? null : styleId)
    }

    const handleModalStyleClick = (styleId) => {
        onSelectStyle(styleId === selectedStyle ? null : styleId)
        setIsModalOpen(false)
    }

    const renderStyleItem = (style, onClick, isModal = false) => (
        <div
            key={style.id}
            className={`style-item ${selectedStyle === style.id ? 'selected' : ''} ${isModal ? 'modal-item' : ''}`}
            onClick={() => onClick(style.id)}
        >
            <div className={`style-image-wrapper ${selectedStyle === style.id ? 'selected' : ''}`}>
                <img
                    src={style.image}
                    alt={`${style.name} Style`}
                    className="style-image"
                    loading="lazy"
                    decoding="async"
                />
                {selectedStyle === style.id && <div className="style-overlay"></div>}
            </div>
            <span className="style-label">{style.name}</span>
        </div>
    )

    return (
        <div className="art-style-selector">
            <div className="style-header">
                <h3 className="style-title">SELECT ART STYLE</h3>
                <button className="view-all-btn" onClick={() => setIsModalOpen(true)}>
                    View All
                </button>
            </div>
            <div className="style-list">
                {ART_STYLES.map((style) => renderStyleItem(style, handleStyleClick))}
            </div>

            {/* View All Modal */}
            {isModalOpen && (
                <div className="style-modal-overlay" onClick={() => setIsModalOpen(false)}>
                    <div className="style-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="style-modal-header">
                            <h2>All Art Styles</h2>
                            <button className="style-modal-close" onClick={() => setIsModalOpen(false)}>
                                <X size={24} />
                            </button>
                        </div>
                        <div className="style-modal-content">
                            <div className="style-modal-grid">
                                {ART_STYLES.map((style) => renderStyleItem(style, handleModalStyleClick, true))}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default ArtStyleSelector
