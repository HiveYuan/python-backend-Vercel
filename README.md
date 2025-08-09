# Python Backend API Service

A minimal Python backend API service based on Flask framework, optimized for Vercel deployment.

## Features

- 🚀 Simple RESTful API based on Flask
- ⚡ Lightweight with minimal dependencies
- 📦 Optimized for Vercel deployment
- 🔍 Health check endpoint for monitoring

## Project Structure

```
python-backend-Vercel/
├── app.py              # Flask application main file
├── requirements.txt    # Python dependencies (minimal)
├── vercel.json        # Vercel deployment configuration  
└── README.md          # Project documentation
```

## Quick Start

### 1. Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd python-backend-Vercel

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

The service will start at http://localhost:5000

### 2. Deploy to Vercel

#### Method 1: Via GitHub (Recommended)
1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Vercel will automatically deploy

#### Method 2: Via Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel deploy --prod
```

## API Endpoints

### Available Endpoints

- `GET /` - Service information
- `GET /api/health` - Health check

### Usage Examples

#### Service Information
```bash
curl https://your-app.vercel.app/
```

Response:
```json
{
  "name": "Python Backend API Service",
  "description": "Universal Python backend API service",
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/health"
  }
}
```

#### Health Check
```bash
curl https://your-app.vercel.app/api/health
```

Response:
```json
{
  "status": "success",
  "message": "API service is running normally",
  "version": "1.0.0"
}
```

## Dependencies

- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing support

## Deployment Notes

- **Package Size**: Optimized to stay under Vercel's 250MB limit
- **Runtime**: Python 3.9+ (automatically detected by Vercel)
- **Cold Start**: Fast startup due to minimal dependencies

## Extending the API

To add new endpoints, simply add new routes to `app.py`:

```python
@app.route('/api/new-endpoint', methods=['GET'])
def new_endpoint():
    return jsonify({
        'message': 'New endpoint working!'
    })
```

## Error Handling

The API includes built-in error handling for:
- 404 - Endpoint not found
- 500 - Internal server error

## License

MIT License