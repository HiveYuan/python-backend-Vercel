from flask import Blueprint, request, jsonify, current_app
import logging

logger = logging.getLogger(__name__)

# Create blueprint for tool-related routes
tools_bp = Blueprint('tools', __name__)


@tools_bp.route('/tools', methods=['GET'])
def list_tools():
    """
    Get list of all available tools
    
    Returns:
        JSON response containing detailed information of all tools
    """
    try:
        tool_manager = current_app.tool_manager
        tools_info = tool_manager.list_available_tools()
        
        return jsonify({
            'status': 'success',
            'message': f'Found {len(tools_info)} available tools',
            'data': {
                'tools': tools_info,
                'count': len(tools_info)
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get tool list: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to get tool list',
            'code': 'LIST_TOOLS_ERROR'
        }), 500


@tools_bp.route('/tools/<tool_name>', methods=['GET'])
def get_tool_info(tool_name):
    """
    Get detailed information of a specific tool
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        JSON response containing detailed tool information
    """
    try:
        tool_manager = current_app.tool_manager
        tool_schema = tool_manager.get_tool_schema(tool_name)
        
        if not tool_schema:
            return jsonify({
                'status': 'error',
                'message': f'Tool {tool_name} does not exist',
                'code': 'TOOL_NOT_FOUND'
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully retrieved information for tool {tool_name}',
            'data': tool_schema
        })
        
    except Exception as e:
        logger.error(f"Failed to get tool information: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to get tool information',
            'code': 'GET_TOOL_ERROR'
        }), 500


@tools_bp.route('/crawler', methods=['GET'])
def web_crawler():
    """
    网页爬虫接口 - 获取网页内容
    
    Query Parameters:
        url: 要抓取的网页URL
        
    Returns:
        JSON响应包含网页内容
    """
    try:
        # 获取URL参数
        url = request.args.get('url')
        if not url:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: url',
                'code': 'MISSING_PARAMETER'
            }), 400
        
        # 记录执行请求
        logger.info(f"执行网页爬虫，URL: {url}")
        
        # Execute tool
        tool_manager = current_app.tool_manager
        result = tool_manager.execute_tool('web_crawler', url=url)
        
        # Return corresponding HTTP status codes based on execution result
        if result['status'] == 'success':
            return jsonify(result)
        elif result.get('code') == 'TOOL_NOT_FOUND':
            return jsonify(result), 404
        elif result.get('code') == 'INVALID_PARAMETERS':
            return jsonify(result), 400
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"执行网页爬虫时发生异常: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}',
            'code': 'INTERNAL_ERROR'
        }), 500


@tools_bp.route('/execute', methods=['GET'])
def execute_tool_generic():
    """
    通用工具执行接口
    
    Query Parameters:
        tool: 工具名称
        其他参数根据具体工具而定
        
    Returns:
        JSON响应包含工具执行结果
    """
    try:
        # 获取工具名称
        tool_name = request.args.get('tool')
        if not tool_name:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: tool',
                'code': 'MISSING_PARAMETER'
            }), 400
        
        # 获取其他参数
        params = {}
        for key, value in request.args.items():
            if key != 'tool':
                params[key] = value
        
        # 记录执行请求
        logger.info(f"执行工具 {tool_name}，参数: {params}")
        
        # Execute tool
        tool_manager = current_app.tool_manager
        result = tool_manager.execute_tool(tool_name, **params)
        
        # Return corresponding HTTP status codes based on execution result
        if result['status'] == 'success':
            return jsonify(result)
        elif result.get('code') == 'TOOL_NOT_FOUND':
            return jsonify(result), 404
        elif result.get('code') == 'INVALID_PARAMETERS':
            return jsonify(result), 400
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Exception occurred while executing tool {tool_name}: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}',
            'code': 'INTERNAL_ERROR',
            'tool': tool_name
        }), 500


@tools_bp.route('/tools/<tool_name>/schema', methods=['GET'])
def get_tool_schema(tool_name):
    """
    Get parameter Schema of a specific tool
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        JSON response containing the tool's parameter Schema
    """
    try:
        tool_manager = current_app.tool_manager
        tool = tool_manager.get_tool(tool_name)
        
        if not tool:
            return jsonify({
                'status': 'error',
                'message': f'Tool {tool_name} does not exist',
                'code': 'TOOL_NOT_FOUND'
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully retrieved parameter Schema for tool {tool_name}',
            'data': {
                'name': tool.name,
                'description': tool.description,
                'parameters': tool.parameters
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get tool Schema: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to get tool Schema',
            'code': 'GET_SCHEMA_ERROR'
        }), 500