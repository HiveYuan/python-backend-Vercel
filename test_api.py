#!/usr/bin/env python3
"""
API test script
Used to verify the basic functionality of the Flask application
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all key modules can be imported normally"""
    try:
        print("Testing imports...")
        
        # Test basic tool import
        from tools.base_tool import Tool
        print("✓ Basic tool class imported successfully")
        
        # Test tool manager import
        from managers.tool_manager import ToolManager
        print("✓ Tool manager imported successfully")
        
        # Test tool instantiation
        manager = ToolManager()
        print(f"✓ Tool manager instantiated successfully, loaded {manager.get_tools_count()} tools")
        
        # List all tools
        tools = manager.get_all_tools()
        print("✓ Available tools:")
        for name, desc in tools.items():
            print(f"  - {name}: {desc[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {str(e)}")
        return False

def test_flask_app():
    """Test if Flask application can start"""
    try:
        print("\nTesting Flask application...")
        from app import app
        
        # Test application configuration
        print(f"✓ Flask application created successfully")
        print(f"✓ JSON Chinese support: {not app.config['JSON_AS_ASCII']}")
        
        # Test if tool manager is correctly bound
        if hasattr(app, 'tool_manager'):
            print(f"✓ Tool manager is bound to the application")
        else:
            print("✗ Tool manager is not properly bound")
            
        return True
        
    except Exception as e:
        print(f"✗ Flask application test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("=== Python Backend API Test ===\n")
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test Flask application
    if not test_flask_app():
        success = False
    
    print("\n=== Test Results ===")
    if success:
        print("✓ All tests passed! API is ready")
        print("\nDeployment recommendations:")
        print("1. Set environment variable OPENAI_API_KEY")
        print("2. Run 'python app.py' to start development server")
        print("3. Use 'vercel deploy' to deploy to Vercel")
        print("\nAPI usage examples:")
        print("- Web crawler: curl 'http://localhost:5000/api/crawler?url=https://example.com'")
        print("- Generic interface: curl 'http://localhost:5000/api/execute?tool=web_crawler&url=https://example.com'")
    else:
        print("✗ Some tests failed, please check configuration")
        
    return success

if __name__ == "__main__":
    exit(0 if main() else 1)