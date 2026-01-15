import React from 'react'
import ImageUploadForm from './components/ImageUploadForm'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">🤖</div>
            <h1>Img Gen</h1>
          </div>
          <p className="subtitle">AI-Powered Image Generation & Transformation</p>
          <div className="tech-lines">
            <div className="tech-line"></div>
            <div className="tech-line"></div>
            <div className="tech-line"></div>
          </div>
        </div>
      </header>

      <main className="main-content">
        <ImageUploadForm />
      </main>

      <footer className="app-footer">
        <div className="footer-grid">
          <span>⚡ NEURAL PROCESSING</span>
          <span>🎨 AI CREATIVITY</span>
          <span>🚀 NEXT-GEN TECH</span>
        </div>
      </footer>
    </div>
  )
}

export default App