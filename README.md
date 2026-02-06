# 🌍 AI Travel Itinerary Planner

An intelligent travel planning assistant powered by AI, LangChain, and conversational interfaces. This system generates personalized day-trip itineraries based on your destination and interests using advanced language models.

## 🌟 Features

- **AI-Powered Itinerary Generation**: Uses GROQ LLM (Llama 3.3) or local Ollama models for intelligent, personalized travel recommendations.
- **Conversational Interface**: Clean Streamlit-based web UI for natural language interaction.
- **Flexible LLM Backend**: Switch seamlessly between cloud-based GROQ API and local Ollama deployment.
- **Context-Aware Planning**: Generates detailed day-trip itineraries tailored to user interests.
- **Production-Ready**: Fully containerized with Docker and Kubernetes support.
- **Structured Logging**: Comprehensive logging and custom exception handling for debugging.
- **ELK Stack Integration**: Complete logging and monitoring solution with Elasticsearch, Logstash, Kibana, and Filebeat.

## 🛠️ Tech Stack

- **LLM**: GROQ API (Llama 3.3) / Ollama (Qwen3-VL)
- **Framework**: LangChain (LCEL)
- **Frontend**: Streamlit
- **Logging & Monitoring**: ELK Stack (Elasticsearch, Logstash, Kibana, Filebeat)
- **Containerization**: Docker
- **Orchestration**: Kubernetes (K8s)
- **Language**: Python 3.11

## 📁 Project Structure

```
AI Travel Agent/
├── app.py                      # Streamlit application entry point
├── src/
│   ├── core/
│   │   └── planner.py         # Travel planner core logic
│   ├── chains/
│   │   └── itinerary_chain.py # LangChain pipeline
│   ├── config/
│   │   └── config.py          # Configuration & Environment setup
│   └── utils/
│       ├── logger.py          # Logging utilities
│       └── custom_exception.py # Exception handling
├── Dockerfile                  # Container configuration
├── k8s-deployment.yaml        # Kubernetes deployment manifest
├── elasticsearch.yaml         # Elasticsearch deployment
├── logstash.yaml              # Logstash deployment
├── kibana.yaml                # Kibana deployment
├── filebeat.yaml              # Filebeat DaemonSet
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
└── .env                       # Environment variables
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher (managed via `uv`)
- [GROQ API Key](https://console.groq.com) (for cloud deployment)
- [Ollama](https://ollama.ai) (optional, for local deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/deep1305/AI_Travel_Itinerary_Planner-.git
   cd "AI Travel Agent"
   ```

2. **Install dependencies**
   
   Using `uv` (recommended):
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # GROQ Configuration (for cloud deployment)
   GROQ_API_KEY=your_groq_api_key
   
   # Ollama Configuration (for local deployment)
   USE_OLLAMA=false  # Set to 'true' for local Ollama
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build the Docker image
docker build -t ai-travel-agent:latest .

# Run the container
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_groq_api_key \
  -e USE_OLLAMA=false \
  ai-travel-agent:latest
```

Access the app at `http://localhost:8501`

### Docker Compose (Optional)

Create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - USE_OLLAMA=false
```

Run with:
```bash
docker-compose up --build
```

## ☸️ Kubernetes Deployment

Deploy to a Kubernetes cluster (GKE, Minikube, etc.):

### 1. Create Secrets

```bash
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY=your_groq_api_key \
  --from-literal=USE_OLLAMA=false
```

### 2. Build and Tag Image

For GCP Artifact Registry:
```bash
# Build image
docker build -t ai-travel-agent:latest .

# Tag for Artifact Registry
docker tag ai-travel-agent:latest \
  <region>-docker.pkg.dev/<project-id>/<repo-name>/ai-travel-agent:latest

# Push to registry
docker push <region>-docker.pkg.dev/<project-id>/<repo-name>/ai-travel-agent:latest
```

### 3. Update Deployment Manifest

Edit `k8s-deployment.yaml` to use your image:
```yaml
image: <region>-docker.pkg.dev/<project-id>/<repo-name>/ai-travel-agent:latest
imagePullPolicy: Always  # Change to 'Always' for production
```

### 4. Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f k8s-deployment.yaml

# Check status
kubectl get pods
kubectl get svc streamlit-service

# View logs
kubectl logs -f <pod-name>
```

### 5. Access the Application

For LoadBalancer service:
```bash
# Get external IP
kubectl get svc streamlit-service

# Access at: http://<EXTERNAL-IP>
```

For local testing (Minikube):
```bash
minikube service streamlit-service
```

## 📊 ELK Stack Deployment (Logging & Monitoring)

The project includes a complete ELK (Elasticsearch, Logstash, Kibana) stack for centralized logging and monitoring.

### Architecture

```
Streamlit App (Logs) 
    ↓
Filebeat (Collects logs from all pods)
    ↓
Logstash (Processes & transforms logs)
    ↓
Elasticsearch (Stores & indexes logs)
    ↓
Kibana (Visualizes & searches logs)
```

### Deploy ELK Stack

**1. Create logging namespace:**
```bash
kubectl create namespace logging
```

**2. Deploy Elasticsearch (storage for logs):**
```bash
kubectl apply -f elasticsearch.yaml

# Verify
kubectl get pods -n logging
kubectl get pvc -n logging
kubectl get pv
```

**3. Deploy Logstash (log processing):**
```bash
kubectl apply -f logstash.yaml

# Verify
kubectl get pods -n logging
```

**4. Deploy Kibana (visualization dashboard):**
```bash
kubectl apply -f kibana.yaml

# Verify
kubectl get svc -n logging
```

**5. Deploy Filebeat (log collection):**
```bash
kubectl apply -f filebeat.yaml

# Verify - should run on each node
kubectl get daemonset -n logging
kubectl get pods -n logging -l k8s-app=filebeat
```

### Access Kibana Dashboard

**For Minikube:**
```bash
minikube service kibana -n logging
```

**For GKE/Cloud:**
```bash
# Get NodePort
kubectl get svc kibana -n logging

# Access at: http://<NODE-IP>:30601
```

### View Logs in Kibana

1. Open Kibana in browser
2. Go to **Management → Stack Management → Index Patterns**
3. Create index pattern: `filebeat-*`
4. Set time field: `@timestamp`
5. Go to **Discover** to view logs
6. Filter by namespace, pod, container, etc.

### ELK Stack Components

| Component | Purpose | Port | Storage |
|-----------|---------|------|---------|
| **Elasticsearch** | Log storage & indexing | 9200 | 2Gi PVC |
| **Logstash** | Log processing & transformation | 5044 (input), 9600 (monitoring) | - |
| **Kibana** | Log visualization & search UI | 5601 (NodePort: 30601) | - |
| **Filebeat** | Log collection from containers | - | Registry data on each node |

### Troubleshooting ELK Stack

**Elasticsearch CrashLoopBackOff on Minikube (Java cgroup NPE):**
- If you see an error like `CgroupInfo.getMountPoint() ... anyController is null`, use the `7.17.28` images in this repo (older `7.17.0` can crash in some cgroup environments).

**Check Elasticsearch health:**
```bash
kubectl exec -n logging <elasticsearch-pod> -- curl -X GET "localhost:9200/_cluster/health?pretty"
```

**Check logs are flowing:**
```bash
# Check Filebeat is collecting
kubectl logs -n logging -l k8s-app=filebeat

# Check Logstash is processing
kubectl logs -n logging -l app=logstash

# Check Elasticsearch indices
kubectl exec -n logging <elasticsearch-pod> -- curl -X GET "localhost:9200/_cat/indices?v"
```

**View pod logs:**
```bash
kubectl logs -n logging <pod-name>
```

### Cleanup ELK Stack

```bash
kubectl delete -f filebeat.yaml
kubectl delete -f kibana.yaml
kubectl delete -f logstash.yaml
kubectl delete -f elasticsearch.yaml
kubectl delete namespace logging
```

## 📊 How It Works

1. **User Input**: User enters a destination city and interests (e.g., "museums, food, history").
2. **LangChain Processing**: The input is formatted into a prompt template and sent to the LLM.
3. **AI Generation**: 
   - **Cloud Mode**: GROQ API (Llama 3.3) generates the itinerary.
   - **Local Mode**: Ollama (Qwen3-VL) processes the request locally.
4. **Response Display**: The generated itinerary is displayed in a clean, formatted layout in Streamlit.
5. **Conversation History**: Messages are tracked for potential future enhancements.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | GROQ API key for cloud LLM | - | Yes (if not using Ollama) |
| `USE_OLLAMA` | Use local Ollama instead of GROQ | `false` | No |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` | No |

### Model Configuration

Edit `src/config/config.py` to change models:
```python
# Ollama Model
OLLAMA_MODEL = "qwen3-vl:30b-a3b-instruct"

# Groq Model
GROQ_MODEL = "llama-3.3-70b-versatile"
```

## 🧪 Development

### Local Development with Ollama

1. Install and start Ollama:
   ```bash
   ollama pull qwen3-vl:30b-a3b-instruct
   ollama serve
   ```

2. Set environment variable:
   ```bash
   USE_OLLAMA=true
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

### Testing Different LLMs

Switch between models by updating `config.py` or setting environment variables:
- **For GROQ**: Set `USE_OLLAMA=false`
- **For Ollama**: Set `USE_OLLAMA=true`

## 📝 Example Usage

1. Open the app in your browser
2. Enter a city: `Paris`
3. Enter interests: `art, cafes, architecture`
4. Click "Generate Itinerary"
5. Receive a personalized day-trip plan with recommended activities, timing, and tips

## 🚀 Deployment Options

### GCP Cloud Run (Serverless)

```bash
gcloud run deploy ai-travel-agent \
  --image <region>-docker.pkg.dev/<project-id>/<repo>/ai-travel-agent:latest \
  --platform managed \
  --region <region> \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=<your-key>,USE_OLLAMA=false
```

### GCP GKE (Kubernetes)

Follow the Kubernetes deployment steps above with GKE-specific configurations.

### AWS ECS / Azure Container Instances

Similar Docker-based deployment using respective cloud container services.

## 🛡️ Best Practices

- ✅ Always use environment variables for API keys (never hardcode)
- ✅ Use Python 3.11 for consistency across local and production
- ✅ Enable structured logging for debugging in production
- ✅ Use `imagePullPolicy: Always` for production Kubernetes deployments
- ✅ Set resource limits in Kubernetes manifests for production workloads

## 📦 Dependencies

Key packages:
- `langchain` - LLM orchestration
- `langchain-groq` - GROQ API integration
- `langchain-ollama` - Ollama local integration
- `streamlit` - Web interface
- `python-dotenv` - Environment variable management

Full list in `requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) for LLM orchestration
- [GROQ](https://groq.com) for lightning-fast inference
- [Ollama](https://ollama.ai) for local LLM deployment
- [Streamlit](https://streamlit.io) for the elegant UI framework

---

**Made with ❤️ for Travel Enthusiasts and AI Explorers**
