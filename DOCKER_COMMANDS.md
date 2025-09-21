# FloatChat Docker Commands Guide
# Complete setup and management commands for containerized deployment

## 🚀 QUICK START COMMANDS

### 1. Build and Start Everything (First Time)
```powershell
# Clone or navigate to FloatChat directory
cd "C:\Users\swapn\OneDrive\Documents\Floatchat_SIH"

# Create environment file (add your Cerebras API key)
copy .env.docker .env

# Build and start all services
docker-compose up --build -d
```

### 2. Check if Everything is Running
```powershell
# Check all containers status
docker-compose ps

# Check logs
docker-compose logs floatchat-api
docker-compose logs floatchat-db
```

### 3. Test the API
```powershell
# Test health endpoint
curl http://localhost:5000/api/health

# Test query endpoint
curl -X POST http://localhost:5000/api/query -H "Content-Type: application/json" -d "{\"query\": \"show temperature data near mumbai\"}"
```

## 📋 DETAILED DOCKER COMMANDS

### Building the FloatChat Container

```powershell
# Build just the FloatChat image
docker build -t floatchat:latest .

# Build with specific tag
docker build -t floatchat:v1.0 .

# Build without cache (clean build)
docker build --no-cache -t floatchat:latest .
```

### Running Single Container (Development)

```powershell
# Run FloatChat container only (requires external database)
docker run -d \
  --name floatchat-dev \
  -p 5000:5000 \
  -e CEREBRAS_API_KEY=your_api_key_here \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  floatchat:latest

# Run with volume mounts for development
docker run -d \
  --name floatchat-dev \
  -p 5000:5000 \
  -v ${PWD}:/app \
  -e CEREBRAS_API_KEY=your_api_key_here \
  floatchat:latest
```

### Docker Compose Operations

```powershell
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d floatchat-api

# Stop all services
docker-compose down

# Stop and remove volumes (CAREFUL: deletes data!)
docker-compose down -v

# Restart specific service
docker-compose restart floatchat-api

# View logs
docker-compose logs -f floatchat-api
docker-compose logs -f floatchat-db

# Scale services (if needed)
docker-compose up -d --scale floatchat-api=3
```

### Debugging and Maintenance

```powershell
# Enter container shell
docker exec -it floatchat-backend bash

# Check container resources
docker stats floatchat-backend

# Inspect container configuration
docker inspect floatchat-backend

# View container filesystem
docker exec floatchat-backend ls -la /app

# Copy files from container
docker cp floatchat-backend:/app/logs ./local-logs

# View database data
docker exec -it floatchat-postgres psql -U floatchat_user -d floatchat_ocean_data
```

### Database Operations

```powershell
# Connect to PostgreSQL
docker exec -it floatchat-postgres psql -U floatchat_user -d floatchat_ocean_data

# Backup database
docker exec floatchat-postgres pg_dump -U floatchat_user floatchat_ocean_data > backup.sql

# Restore database
docker exec -i floatchat-postgres psql -U floatchat_user -d floatchat_ocean_data < backup.sql

# Check database size
docker exec floatchat-postgres psql -U floatchat_user -d floatchat_ocean_data -c "\l+"
```

## 🔧 CONFIGURATION COMMANDS

### Environment Setup

```powershell
# Create production environment file
@"
# FloatChat Docker Environment Configuration
CEREBRAS_API_KEY=your_cerebras_api_key_here
DATABASE_URL=postgresql://floatchat_user:floatchat_secure_password_2024@floatchat-db:5432/floatchat_ocean_data
FLASK_ENV=production
FLASK_DEBUG=false
"@ | Out-File -FilePath .env -Encoding utf8

# View current environment
docker exec floatchat-backend env | grep -E "(CEREBRAS|DATABASE|FLASK)"
```

### Network Configuration

```powershell
# List Docker networks
docker network ls

# Inspect FloatChat network
docker network inspect floatchat-network

# Connect external container to network
docker network connect floatchat-network your-other-container
```

## 📊 MONITORING COMMANDS

### Health Checks

```powershell
# Check all service health
docker-compose ps

# Manual health check
curl http://localhost:5000/api/health
curl http://localhost:5000/api/examples

# Database connection test
docker exec floatchat-postgres pg_isready -U floatchat_user
```

### Performance Monitoring

```powershell
# Monitor resource usage
docker stats

# Monitor specific container
docker stats floatchat-backend

# Check disk usage
docker system df

# Check container logs size
docker exec floatchat-backend du -sh /app/logs
```

## 🧹 CLEANUP COMMANDS

### Removing Containers

```powershell
# Stop and remove all FloatChat containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove specific container
docker rm -f floatchat-backend
```

### Cleaning Docker System

```powershell
# Remove unused containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Complete system cleanup (CAREFUL!)
docker system prune -a -f
```

## 🚢 DEPLOYMENT COMMANDS

### Production Deployment

```powershell
# Build for production
docker-compose -f docker-compose.yml up --build -d

# Update specific service
docker-compose pull floatchat-api
docker-compose up -d floatchat-api

# Zero-downtime deployment
docker-compose up -d --scale floatchat-api=2 floatchat-api
docker-compose up -d --scale floatchat-api=1 floatchat-api
```

### Container Registry Operations

```powershell
# Tag for registry
docker tag floatchat:latest your-registry.com/floatchat:v1.0

# Push to registry
docker push your-registry.com/floatchat:v1.0

# Pull and run from registry
docker pull your-registry.com/floatchat:v1.0
docker run -d --name floatchat -p 5000:5000 your-registry.com/floatchat:v1.0
```

## 🔍 TROUBLESHOOTING

### Common Issues

```powershell
# Container won't start - check logs
docker-compose logs floatchat-api

# Database connection issues
docker exec floatchat-postgres pg_isready -U floatchat_user

# API not responding
curl -v http://localhost:5000/api/health

# Port conflicts
netstat -an | findstr :5000

# Disk space issues
docker system df
docker system prune -f
```

### Reset Everything

```powershell
# Complete reset (CAREFUL: deletes all data!)
docker-compose down -v
docker rmi floatchat:latest
docker-compose up --build -d
```

## 📋 USEFUL ALIASES (Add to PowerShell Profile)

```powershell
# Add these to your PowerShell profile for convenience
function fcup { docker-compose up -d }
function fcdown { docker-compose down }
function fclogs { docker-compose logs -f floatchat-api }
function fcshell { docker exec -it floatchat-backend bash }
function fchealth { curl http://localhost:5000/api/health }
function fcstats { docker stats floatchat-backend }
```

## 🌐 SHARING WITH TEAM

To share with other team members:

1. **Share the repository** with all Docker files
2. **Provide Cerebras API key** separately  
3. **Run these commands** on any machine with Docker:

```powershell
git clone https://github.com/Swapnil565/FloatChat.git
cd FloatChat
echo "CEREBRAS_API_KEY=your_key_here" > .env
docker-compose up --build -d
```

The application will be available at `http://localhost:5000` on any machine!