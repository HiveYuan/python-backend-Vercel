from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class Tool(ABC, BaseModel):
    """
    Abstract base class that defines the basic interface for all tools
    
    All concrete tools should inherit from this class and implement the execute method
    """
    
    name: str
    description: str
    parameters: Dict[str, Any]
    
    class Config:
        arbitrary_types_allowed = True
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Execute the main functionality of the tool
        
        Args:
            **kwargs: Parameters required for tool execution
            
        Returns:
            str: The result of tool execution
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Return the JSON Schema of the tool
        
        Returns:
            Dict[str, Any]: The schema information of the tool
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    def validate_parameters(self, **kwargs) -> bool:
        """
        Validate if the passed parameters meet the requirements
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            bool: Whether the parameters are valid
        """
        required_params = self.parameters.get("required", [])
        
        for param in required_params:
            if param not in kwargs:
                return False
                
        return True
    
    def __str__(self) -> str:
        return f"Tool({self.name})"
    
    def __repr__(self) -> str:
        return f"Tool(name='{self.name}', description='{self.description[:50]}...')"
