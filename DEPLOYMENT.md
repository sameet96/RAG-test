# 🚀 RAG PDF Chat - Deployment Guide

This guide will help you deploy your RAG PDF Chat application using Docker and integrate it into your portfolio website.

## 📋 Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Domain name (for production deployment)
- SSL certificate (for HTTPS)

## 🐳 Docker Deployment

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd RAG-test
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Deploy**:
   ```bash
   ./deploy.sh development  # For local testing
   ./deploy.sh production   # For production with nginx
   ```

### Manual Docker Commands

```bash
# Build the image
docker-compose build

# Run in development mode
docker-compose up -d rag-app

# Run in production mode with nginx
docker-compose --profile production up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🌐 Portfolio Integration

### Option 1: Standalone HTML Page

Use the provided `portfolio-integration.html` as a complete standalone page:

```html
<!-- Include in your portfolio -->
<iframe src="http://your-domain.com" 
        width="100%" 
        height="800px" 
        frameborder="0">
</iframe>
```

### Option 2: JavaScript Integration

Add to your existing portfolio:

```html
<!-- Include CSS -->
<link rel="stylesheet" href="portfolio-integration.css">

<!-- Include JavaScript -->
<script src="portfolio-integration.js"></script>

<!-- Add container -->
<div id="rag-container"></div>

<script>
// Initialize the RAG chat widget
const ragChat = new RAGPDFChat('rag-container', {
    apiUrl: 'http://your-domain.com',
    height: '600px',
    width: '100%'
});
</script>
```

### Option 3: React Component

```jsx
import React, { useEffect, useRef } from 'react';

const RAGPDFChat = ({ apiUrl = 'http://localhost:8501' }) => {
  const iframeRef = useRef(null);

  useEffect(() => {
    // Add any initialization logic here
  }, []);

  return (
    <div className="rag-iframe-container">
      <iframe
        ref={iframeRef}
        src={apiUrl}
        title="RAG PDF Chat Application"
        width="100%"
        height="800px"
        frameBorder="0"
      />
    </div>
  );
};

export default RAGPDFChat;
```

## 🔧 Production Deployment

### 1. Server Setup

**Requirements**:
- Ubuntu 20.04+ or CentOS 8+
- 2GB+ RAM
- 10GB+ storage
- Docker & Docker Compose

**Install Docker**:
```bash
# Ubuntu
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Domain Configuration

**DNS Setup**:
```
A    rag.yourdomain.com    -> YOUR_SERVER_IP
CNAME www.rag.yourdomain.com -> rag.yourdomain.com
```

**SSL Certificate** (using Let's Encrypt):
```bash
# Install certbot
sudo apt install certbot

# Generate certificate
sudo certbot certonly --standalone -d rag.yourdomain.com
```

### 3. Production Configuration

**Update nginx.conf**:
```nginx
server {
    listen 443 ssl;
    server_name rag.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/rag.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/rag.yourdomain.com/privkey.pem;
    
    # ... rest of configuration
}
```

**Update docker-compose.yml**:
```yaml
services:
  rag-app:
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    restart: unless-stopped
```

### 4. Deploy to Production

```bash
# Clone repository on server
git clone <your-repo>
cd RAG-test

# Configure environment
nano .env
# Add your OpenAI API key

# Deploy
./deploy.sh production

# Setup SSL (if using Let's Encrypt)
sudo certbot --nginx -d rag.yourdomain.com
```

## 🔒 Security Considerations

### Environment Variables
- Never commit `.env` files
- Use secrets management in production
- Rotate API keys regularly

### Network Security
```yaml
# In docker-compose.yml
services:
  rag-app:
    networks:
      - internal
    expose:
      - "8501"

  nginx:
    networks:
      - internal
      - external
    ports:
      - "80:80"
      - "443:443"

networks:
  internal:
    driver: bridge
  external:
    driver: bridge
```

### Firewall Configuration
```bash
# Ubuntu UFW
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check application status
curl -f http://your-domain.com/_stcore/health

# Check Docker containers
docker-compose ps

# View logs
docker-compose logs -f rag-app
```

### Backup Strategy
```bash
# Backup volumes
docker run --rm -v rag-test_uploads:/data -v $(pwd):/backup alpine tar czf /backup/uploads-backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v rag-test_uploads:/data -v $(pwd):/backup alpine tar xzf /backup/uploads-backup.tar.gz -C /data
```

### Updates
```bash
# Update application
git pull origin main
docker-compose build
docker-compose up -d

# Clean up old images
docker image prune -f
```

## 🚨 Troubleshooting

### Common Issues

**1. Container won't start**:
```bash
# Check logs
docker-compose logs rag-app

# Check environment variables
docker-compose config
```

**2. OpenAI API errors**:
```bash
# Verify API key
echo $OPENAI_API_KEY

# Test API connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

**3. Memory issues**:
```bash
# Increase Docker memory limits
# In docker-compose.yml:
services:
  rag-app:
    deploy:
      resources:
        limits:
          memory: 2G
```

**4. Port conflicts**:
```bash
# Check port usage
sudo netstat -tulpn | grep :8501

# Change port in docker-compose.yml
ports:
  - "8502:8501"
```

## 📈 Performance Optimization

### Docker Optimization
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# ... rest of Dockerfile
```

### Streamlit Optimization
```python
# In app.py
import streamlit as st

# Enable caching
@st.cache_data
def load_model():
    return your_model

# Optimize session state
if 'model' not in st.session_state:
    st.session_state.model = load_model()
```

## 🎯 Next Steps

1. **Deploy to your server** using the production guide
2. **Configure your domain** and SSL certificates
3. **Integrate into your portfolio** using the provided code
4. **Monitor performance** and optimize as needed
5. **Set up automated backups** and updates

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review Docker and Streamlit documentation
- Create an issue in the repository

---

**Happy Deploying! 🚀**
