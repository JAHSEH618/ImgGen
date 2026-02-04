import React from 'react'
import { CheckCircle, XCircle, AlertCircle, Zap } from 'lucide-react'
import './Toast.css'

const Toast = ({ message, type, isVisible, onClose }) => {
  if (!isVisible) return null

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle size={20} />
      case 'error':
        return <XCircle size={20} />
      case 'warning':
        return <AlertCircle size={20} />
      default:
        return <Zap size={20} />
    }
  }

  return (
    <div className={`toast toast-${type} ${isVisible ? 'toast-visible' : ''}`}>
      <div className="toast-content">
        <div className="toast-icon">
          {getIcon()}
        </div>
        <div className="toast-message">
          {message}
        </div>
        <button className="toast-close" onClick={onClose}>
          ×
        </button>
      </div>
      <div className="toast-progress"></div>
    </div>
  )
}

export default Toast