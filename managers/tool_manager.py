import importlib
import pkgutil
import inspect
import logging
from typing import Dict, List, Optional, Any
from tools.base_tool import Tool

logger = logging.getLogger(__name__)


class ToolManager:
    """
    Tool manager class
    
    Responsible for automatically discovering, registering and managing all tool instances
    Supports dynamic loading of all Tool subclasses from the tools package
    """
    
    def __init__(self):
        """Initialize tool manager and automatically load all available tools"""
        self.tools: Dict[str, Tool] = {}
        self._load_all_tools()
    
    def _load_all_tools(self):
        """Automatically load all tools from the tools package"""
        try:
            # Import tools package
            tools_package = importlib.import_module('tools')
            
            # Iterate through all modules in the tools package
            for _, modname, _ in pkgutil.iter_modules(tools_package.__path__, 'tools.'):
                if modname.endswith('.__init__') or modname.endswith('.base_tool'):
                    continue
                    
                try:
                    # Dynamically import module
                    module = importlib.import_module(modname)
                    
                    # Find all Tool subclasses in the module
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, Tool) and 
                            obj != Tool and 
                            not inspect.isabstract(obj)):
                            
                            # Instantiate tool and register
                            try:
                                tool_instance = obj()
                                self.register_tool(tool_instance)
                                logger.info(f"Successfully loaded tool: {tool_instance.name}")
                            except Exception as e:
                                logger.error(f"Failed to instantiate tool {name}: {str(e)}")
                                
                except Exception as e:
                    logger.error(f"Failed to load module {modname}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Failed to load tools package: {str(e)}")
    
    def register_tool(self, tool: Tool):
        """
        Register a tool instance
        
        Args:
            tool: The tool instance to register
        """
        if not isinstance(tool, Tool):
            raise ValueError(f"Registered object must be an instance of Tool, current type: {type(tool)}")
        
        self.tools[tool.name] = tool
        logger.info(f"Tool {tool.name} registered successfully")
    
    def unregister_tool(self, tool_name: str):
        """
        Unregister a tool
        
        Args:
            tool_name: The name of the tool to unregister
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            logger.info(f"Tool {tool_name} has been unregistered")
        else:
            logger.warning(f"Attempting to unregister non-existent tool: {tool_name}")
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """
        Get a tool instance by name
        
        Args:
            tool_name: The name of the tool
            
        Returns:
            Tool instance, or None if it doesn't exist
        """
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> Dict[str, str]:
        """
        Get names and descriptions of all registered tools
        
        Returns:
            Dictionary containing tool names and descriptions
        """
        return {name: tool.description for name, tool in self.tools.items()}
    
    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the JSON Schema of a specific tool
        
        Args:
            tool_name: The name of the tool
            
        Returns:
            Tool schema information, or None if the tool doesn't exist
        """
        tool = self.get_tool(tool_name)
        return tool.get_schema() if tool else None
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a specific tool
        
        Args:
            tool_name: The name of the tool
            **kwargs: Tool execution parameters
            
        Returns:
            Execution result dictionary
        """
        tool = self.get_tool(tool_name)
        
        if not tool:
            return {
                'status': 'error',
                'message': f'Tool {tool_name} does not exist',
                'code': 'TOOL_NOT_FOUND'
            }
        
        # Validate parameters
        if not tool.validate_parameters(**kwargs):
            required_params = tool.parameters.get("required", [])
            return {
                'status': 'error',
                'message': f'Parameter validation failed, required parameters: {required_params}',
                'code': 'INVALID_PARAMETERS',
                'required_parameters': required_params
            }
        
        try:
            # Execute tool
            result = tool.execute(**kwargs)
            
            return {
                'status': 'success',
                'data': result,
                'tool': tool_name
            }
            
        except Exception as e:
            logger.error(f"Error occurred while executing tool {tool_name}: {str(e)}")
            return {
                'status': 'error',
                'message': f'Tool execution failed: {str(e)}',
                'code': 'EXECUTION_ERROR',
                'tool': tool_name
            }
    
    def list_available_tools(self) -> List[Dict[str, Any]]:
        """
        List detailed information of all available tools
        
        Returns:
            List containing information of all tools
        """
        tools_info = []
        
        for name, tool in self.tools.items():
            tool_info = {
                'name': name,
                'description': tool.description,
                'parameters': tool.parameters
            }
            tools_info.append(tool_info)
        
        return tools_info
    
    def get_tools_count(self) -> int:
        """
        Get the count of registered tools
        
        Returns:
            Number of tools
        """
        return len(self.tools)