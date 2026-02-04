// Session Management Utility
import axios from 'axios'
import { API_URLS } from '../config/api'

class SessionManager {
  constructor() {
    this.sessionId = this.generateSessionId()
    this.heartbeatInterval = null
    this.isActive = true

    // Start heartbeat immediately
    this.startHeartbeat()

    // Listen for page visibility changes
    if (typeof document !== 'undefined') {
      document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this))
    }

    // Listen for beforeunload to cleanup
    if (typeof window !== 'undefined') {
      window.addEventListener('beforeunload', this.cleanup.bind(this))
    }
  }

  generateSessionId() {
    return 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
  }

  getSessionId() {
    return this.sessionId
  }

  startHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
    }

    // Send heartbeat every 2 minutes (less than 3 min timeout)
    this.heartbeatInterval = setInterval(() => {
      if (this.isActive) {
        this.sendHeartbeat()
      }
    }, 2 * 60 * 1000) // 2 minutes

    // Send initial heartbeat
    this.sendHeartbeat()
  }

  async sendHeartbeat() {
    try {
      // Send heartbeat to both services with short timeout
      const timeout = 5000 // 5 second timeout for heartbeats
      const promises = [
        axios.post(API_URLS.fileHeartbeat, {}, {
          headers: { 'X-Session-ID': this.sessionId },
          timeout
        }),
        axios.post(API_URLS.aiHeartbeat, {}, {
          headers: { 'X-Session-ID': this.sessionId },
          timeout
        })
      ]

      await Promise.allSettled(promises)
      // Only log in development
      if (import.meta.env.DEV) {
        console.debug(`Session heartbeat sent: ${this.sessionId}`)
      }

    } catch (error) {
      // Silent fail for heartbeats - they're expected to fail sometimes
      if (import.meta.env.DEV) {
        console.warn('Heartbeat failed:', error.message)
      }
    }
  }

  handleVisibilityChange() {
    if (document.hidden) {
      this.isActive = false
      console.debug('Page hidden, stopping heartbeat')
    } else {
      this.isActive = true
      console.debug('Page visible, resuming heartbeat')
      this.sendHeartbeat() // Send immediate heartbeat when page becomes visible
    }
  }

  async cleanup() {
    try {
      this.isActive = false

      if (this.heartbeatInterval) {
        clearInterval(this.heartbeatInterval)
        this.heartbeatInterval = null
      }

      // Send cleanup requests to both services using new API URLs
      const promises = [
        axios.post(API_URLS.fileCleanup(this.sessionId)),
        axios.post(API_URLS.aiCleanup(this.sessionId))
      ]

      await Promise.allSettled(promises)
      console.debug(`Session cleaned up: ${this.sessionId}`)

    } catch (error) {
      console.warn('Cleanup failed:', error.message)
    }
  }

  // Method to get headers with session ID
  getHeaders(additionalHeaders = {}) {
    return {
      'X-Session-ID': this.sessionId,
      ...additionalHeaders
    }
  }

  // Method to destroy session and create new one
  renewSession() {
    this.cleanup()
    this.sessionId = this.generateSessionId()
    this.isActive = true
    this.startHeartbeat()
    console.debug(`Session renewed: ${this.sessionId}`)
  }
}

// Create singleton instance
const sessionManager = new SessionManager()

export default sessionManager