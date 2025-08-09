from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class Tool(ABC, BaseModel):
    """
    抽象基类，定义所有工具的基本接口
    
    所有具体的工具都应该继承这个基类并实现execute方法
    """
    
    name: str
    description: str
    parameters: Dict[str, Any]
    
    class Config:
        arbitrary_types_allowed = True
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        执行工具的主要功能
        
        Args:
            **kwargs: 工具执行所需的参数
            
        Returns:
            str: 工具执行的结果
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """
        返回工具的JSON Schema
        
        Returns:
            Dict[str, Any]: 工具的schema信息
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    def validate_parameters(self, **kwargs) -> bool:
        """
        验证传入的参数是否符合要求
        
        Args:
            **kwargs: 要验证的参数
            
        Returns:
            bool: 参数是否有效
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
