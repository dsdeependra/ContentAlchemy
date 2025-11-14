# ContentAlchemy Deployment Guide

## Prerequisites

- Python 3.11+
- Docker (optional)
- OpenAI API Key
- SERP API Key (optional)

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/contentalchemy.git
cd contentalchemy
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 5. Run Application
```bash
streamlit run src/web_app/streamlit_app.py
```

Access at: http://localhost:8501

---

## Docker Deployment

### 1. Build Image
```bash
docker build -t contentalchemy:latest .
```

### 2. Run Container
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  -e SERP_API_KEY=your_key \
  contentalchemy:latest
```

### 3. Using Docker Compose
```bash
docker-compose up -d
```

---

## Cloud Deployment

### AWS Deployment

#### Using ECS

1. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name contentalchemy
```

2. **Push Image to ECR**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag contentalchemy:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/contentalchemy:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/contentalchemy:latest
```

3. **Create ECS Task Definition**
```json
{
  "family": "contentalchemy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "contentalchemy",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/contentalchemy:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your_key"
        }
      ]
    }
  ]
}
```

4. **Create ECS Service**
```bash
aws ecs create-service \
  --cluster your-cluster \
  --service-name contentalchemy \
  --task-definition contentalchemy \
  --desired-count 2 \
  --launch-type FARGATE
```

---

### Google Cloud Platform Deployment

#### Using Cloud Run

1. **Build and Push to GCR**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/contentalchemy
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy contentalchemy \
  --image gcr.io/PROJECT_ID/contentalchemy \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key
```

---

### Azure Deployment

#### Using Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name contentalchemy \
  --image youracr.azurecr.io/contentalchemy:latest \
  --dns-name-label contentalchemy \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=your_key
```

---

## Production Configuration

### 1. Environment Variables
```bash
# Production .env
OPENAI_API_KEY=sk-prod-...
SERP_API_KEY=prod-...
OPENAI_MODEL=gpt-4
DEBUG=false
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-prod-...
```

### 2. Monitoring Setup

#### LangSmith Integration
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your_key"
os.environ["LANGCHAIN_PROJECT"] = "contentalchemy-prod"
```

### 3. Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/production.log'),
        logging.StreamHandler()
    ]
)
```

---

## Scaling Configuration

### Horizontal Scaling

#### Docker Compose (Multiple Instances)
```yaml
version: '3.8'
services:
  contentalchemy:
    image: contentalchemy:latest
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
```

#### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contentalchemy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: contentalchemy
  template:
    metadata:
      labels:
        app: contentalchemy
    spec:
      containers:
      - name: contentalchemy
        image: contentalchemy:latest
        ports:
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: contentalchemy-secrets
              key: openai-api-key
```

---

## Load Balancing

### Nginx Configuration
```nginx
upstream contentalchemy {
    least_conn;
    server app1:8501;
    server app2:8501;
    server app3:8501;
}

server {
    listen 80;
    server_name contentalchemy.example.com;

    location / {
        proxy_pass http://contentalchemy;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # WebSocket support for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Database & Caching

### Redis Setup (Optional)
```yaml
# docker-compose.yml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
```

### Integration
```python
import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

# Cache example
def get_cached_content(key):
    cached = redis_client.get(key)
    if cached:
        return cached
    # Generate content...
    redis_client.setex(key, 3600, content)
    return content
```

---

## Security Hardening

### 1. API Key Management
```bash
# Use AWS Secrets Manager
aws secretsmanager create-secret \
  --name contentalchemy/openai-key \
  --secret-string "your_api_key"
```

### 2. HTTPS Configuration
```bash
# Using Let's Encrypt
certbot --nginx -d contentalchemy.example.com
```

### 3. Rate Limiting
```python
from functools import wraps
from time import time

def rate_limit(max_calls=10, period=60):
    def decorator(func):
        calls = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            calls[:] = [c for c in calls if c > now - period]
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## Monitoring & Observability

### 1. Health Checks
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### 2. Prometheus Metrics
```python
from prometheus_client import Counter, Histogram

request_count = Counter('contentalchemy_requests_total', 'Total requests')
request_duration = Histogram('contentalchemy_request_duration_seconds', 'Request duration')
```

### 3. Application Logs
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Content generated", extra={
    "content_type": "blog",
    "word_count": 1500,
    "user_id": user_id
})
```

---

## Backup & Recovery

### 1. Configuration Backup
```bash
# Backup .env and configs
tar -czf backup-$(date +%Y%m%d).tar.gz .env config/
```

### 2. Logs Backup
```bash
# Rotate and backup logs
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501
# Kill process
kill -9 PID
```

#### 2. API Rate Limits
- Implement exponential backoff
- Use caching
- Monitor usage

#### 3. Memory Issues
```bash
# Increase Docker memory
docker run -m 4g contentalchemy:latest
```

#### 4. Connection Timeouts
```python
# Increase timeout
response = requests.get(url, timeout=30)
```

---

## Performance Optimization

### 1. Caching Strategy
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_keywords(topic):
    # Expensive operation
    return keywords
```

### 2. Async Operations
```python
import asyncio

async def generate_multiple_contents(queries):
    tasks = [generate_content(q) for q in queries]
    return await asyncio.gather(*tasks)
```

### 3. Database Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

## Cost Optimization

### 1. Token Usage Monitoring
```python
def track_token_usage(response):
    tokens = response.usage.total_tokens
    cost = tokens * 0.00002  # GPT-4 pricing
    logger.info(f"Tokens used: {tokens}, Cost: ${cost:.4f}")
```

### 2. Model Selection
- Use GPT-3.5 for simple tasks
- Reserve GPT-4 for complex operations

### 3. Caching Results
- Cache frequently requested content
- Use Redis for distributed caching

---

## Maintenance

### Regular Tasks

#### Daily
- Check logs for errors
- Monitor API usage
- Review performance metrics

#### Weekly
- Update dependencies
- Review security alerts
- Backup configurations

#### Monthly
- Security audit
- Performance optimization
- Cost analysis
- Feature review

---

## Rollback Procedure

```bash
# Tag previous version
docker tag contentalchemy:latest contentalchemy:v1.0.0

# Deploy new version
docker build -t contentalchemy:latest .

# If issues occur, rollback
docker tag contentalchemy:v1.0.0 contentalchemy:latest
docker-compose up -d
```

---

## Support & Documentation

- GitHub Issues: https://github.com/yourusername/contentalchemy/issues
- Documentation: https://docs.contentalchemy.ai
- Email: support@contentalchemy.ai
