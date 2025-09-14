// Portfolio Integration JavaScript for RAG PDF Chat Application
// This can be embedded directly into your existing portfolio website

class RAGPDFChat {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            apiUrl: options.apiUrl || 'http://localhost:8501',
            height: options.height || '600px',
            width: options.width || '100%',
            theme: options.theme || 'light',
            ...options
        };
        this.init();
    }

    init() {
        this.createContainer();
        this.loadApplication();
        this.setupEventListeners();
    }

    createContainer() {
        this.container.innerHTML = `
            <div class="rag-pdf-chat-container">
                <div class="rag-header">
                    <h3>🤖 AI PDF Chat</h3>
                    <p>Upload a PDF and ask questions about its content</p>
                </div>
                <div class="rag-iframe-wrapper">
                    <div class="rag-loading">
                        <div class="rag-spinner"></div>
                        <p>Loading RAG PDF Chat Application...</p>
                    </div>
                    <iframe 
                        src="${this.options.apiUrl}"
                        title="RAG PDF Chat Application"
                        class="rag-iframe"
                        style="width: ${this.options.width}; height: ${this.options.height};"
                        frameborder="0">
                    </iframe>
                </div>
                <div class="rag-status" id="rag-status">
                    <span class="rag-status-indicator"></span>
                    <span class="rag-status-text">Connecting...</span>
                </div>
            </div>
        `;

        this.addStyles();
    }

    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .rag-pdf-chat-container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                margin: 20px 0;
            }

            .rag-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }

            .rag-header h3 {
                margin: 0 0 5px 0;
                font-size: 1.5rem;
            }

            .rag-header p {
                margin: 0;
                opacity: 0.9;
                font-size: 0.9rem;
            }

            .rag-iframe-wrapper {
                position: relative;
                background: #f8f9fa;
            }

            .rag-loading {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                z-index: 10;
            }

            .rag-spinner {
                width: 40px;
                height: 40px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                animation: rag-spin 1s linear infinite;
                margin: 0 auto 10px;
            }

            @keyframes rag-spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .rag-loading p {
                color: #666;
                margin: 0;
            }

            .rag-iframe {
                border: none;
                display: block;
            }

            .rag-status {
                padding: 10px 20px;
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 0.9rem;
            }

            .rag-status-indicator {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #ffc107;
                animation: rag-pulse 2s infinite;
            }

            @keyframes rag-pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }

            .rag-status.connected .rag-status-indicator {
                background: #28a745;
                animation: none;
            }

            .rag-status.error .rag-status-indicator {
                background: #dc3545;
                animation: none;
            }

            .rag-status.connected .rag-status-text {
                color: #28a745;
            }

            .rag-status.error .rag-status-text {
                color: #dc3545;
            }
        `;
        document.head.appendChild(style);
    }

    loadApplication() {
        const iframe = this.container.querySelector('.rag-iframe');
        const loading = this.container.querySelector('.rag-loading');
        const status = this.container.querySelector('#rag-status');
        const statusText = status.querySelector('.rag-status-text');

        iframe.addEventListener('load', () => {
            loading.style.display = 'none';
            status.classList.add('connected');
            statusText.textContent = 'Connected';
            this.onConnected();
        });

        iframe.addEventListener('error', () => {
            loading.innerHTML = '<p style="color: #dc3545;">Error loading application</p>';
            status.classList.add('error');
            statusText.textContent = 'Connection Error';
            this.onError();
        });

        // Health check
        this.healthCheck();
    }

    healthCheck() {
        const checkInterval = setInterval(() => {
            fetch(`${this.options.apiUrl}/_stcore/health`)
                .then(response => {
                    if (response.ok) {
                        this.updateStatus('connected', 'Connected');
                    } else {
                        this.updateStatus('error', 'Service Unavailable');
                    }
                })
                .catch(() => {
                    this.updateStatus('error', 'Connection Lost');
                });
        }, 30000); // Check every 30 seconds

        // Store interval ID for cleanup
        this.healthCheckInterval = checkInterval;
    }

    updateStatus(type, text) {
        const status = this.container.querySelector('#rag-status');
        const statusText = status.querySelector('.rag-status-text');
        
        status.className = `rag-status ${type}`;
        statusText.textContent = text;
    }

    setupEventListeners() {
        // Add any custom event listeners here
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Pause health checks when tab is not visible
                if (this.healthCheckInterval) {
                    clearInterval(this.healthCheckInterval);
                }
            } else {
                // Resume health checks when tab becomes visible
                this.healthCheck();
            }
        });
    }

    onConnected() {
        console.log('RAG PDF Chat Application connected');
        // Emit custom event
        this.container.dispatchEvent(new CustomEvent('rag-connected', {
            detail: { timestamp: Date.now() }
        }));
    }

    onError() {
        console.error('RAG PDF Chat Application connection failed');
        // Emit custom event
        this.container.dispatchEvent(new CustomEvent('rag-error', {
            detail: { timestamp: Date.now() }
        }));
    }

    destroy() {
        if (this.healthCheckInterval) {
            clearInterval(this.healthCheckInterval);
        }
        this.container.innerHTML = '';
    }
}

// Usage example:
// const ragChat = new RAGPDFChat('rag-container', {
//     apiUrl: 'http://localhost:8501',
//     height: '600px'
// });

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RAGPDFChat;
}
