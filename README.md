# Python Backend API Service

A universal Python backend API service based on the Flask framework, supporting deployment to the Vercel platform.

## Features

- 🚀 RESTful API based on Flask
- 🧩 Modular tool system with dynamic loading support
- 🌐 Built-in web crawler tool with GPT-4o content optimization
- 📦 Ready-to-use Vercel deployment configuration
- 🔧 Easily extensible architecture design

## Project Structure

```
python-backend-Vercel/
├── app.py                 # Flask application main file
├── vercel.json           # Vercel deployment configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── managers/            # Manager modules
│   └── tool_manager.py  # Tool manager
├── routes/              # API routes
│   └── tools.py        # Tool-related routes
└── tools/               # Tool modules
    ├── base_tool.py    # Tool base class
    └── web_crawler.py  # Web crawler tool
```

## Quick Start

### 1. Environment Configuration

```bash
# Copy environment variables template
cp .env.example .env

# Edit environment variables, set your OpenAI API key
# OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Local Development

```bash
python app.py
```

The service will start at http://localhost:5000

### 4. Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel deploy
```

## API Endpoints

### Basic Endpoints

- `GET /` - Service information
- `GET /api/health` - Health check

### Tool Endpoints

- `GET /api/tools` - Get all available tools
- `GET /api/tools/{tool_name}` - Get specific tool information
- `GET /api/crawler` - Web crawler interface
- `GET /api/execute` - Generic tool execution interface
- `GET /api/tools/{tool_name}/schema` - Get tool parameter schema

### Usage Examples

#### Get all tools
```bash
curl http://localhost:5000/api/tools
```

#### Execute web crawler
```bash
# Method 1: Using dedicated crawler interface
curl "http://localhost:5000/api/crawler?url=https://example.com"

# Method 2: Using generic execution interface
curl "http://localhost:5000/api/execute?tool=web_crawler&url=https://example.com"
```

#### Other tool execution examples
```bash
# Generic tool execution format
curl "http://localhost:5000/api/execute?tool=tool_name&param1=value1&param2=value2"
```

## Adding New Tools

1. Create a new tool file in the `tools/` directory
2. Inherit from the `Tool` base class and implement the `execute` method
3. The tool will be automatically discovered and registered

### Example Tool

```python
from .base_tool import Tool

class MyTool(Tool):
    name: str = "my_tool"
    description: str = "My custom tool"
    parameters: dict = {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter 1 description"
            }
        },
        "required": ["param1"]
    }
    
    def execute(self, **kwargs) -> str:
        param1 = kwargs.get("param1")
        return f"Execution result: {param1}"
```

## Technology Stack

- **Backend**: Flask 3.0
- **Tool Management**: Custom Tool system
- **Deployment**: Vercel Python Runtime
- **Web Scraping**: crawl4ai
- **AI**: OpenAI GPT-4o

## License

MIT License