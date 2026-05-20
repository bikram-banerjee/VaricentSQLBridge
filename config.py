"""
Configuration management for XML to SQL Converter.
"""
import json
import os
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the application."""
    
    # Default configuration
    DEFAULTS = {
        "window": {
            "width": 0.80,  # Percentage of screen width
            "height": 0.70,  # Percentage of screen height
        },
        "converters": {
            "auto_detect": True,
            "default_converter": "GenericData",
        },
        "ui": {
            "theme": "default",
            "font_size": 10,
        },
        "output": {
            "format": "sql",
            "indent": 4,
        },
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to config JSON file
        """
        self.config_file = config_file or os.path.expanduser("~/.xml_to_sql_config.json")
        self.config = self.DEFAULTS.copy()
        
        if os.path.exists(self.config_file):
            self.load()
    
    def load(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(self.config_file, 'r') as f:
                user_config = json.load(f)
                self._deep_merge(self.config, user_config)
            return True
        except (IOError, json.JSONDecodeError):
            return False
    
    def save(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Dot-separated key path (e.g., "converters.auto_detect")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Dot-separated key path
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def _deep_merge(self, base: Dict, update: Dict):
        """
        Deep merge update dict into base dict.
        
        Args:
            base: Base dictionary
            update: Dictionary to merge in
        """
        for key, value in update.items():
            if isinstance(value, dict) and isinstance(base.get(key), dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def to_dict(self) -> Dict:
        """Get configuration as dictionary."""
        return self.config.copy()


# Global config instance
_config = None


def get_config(config_file: Optional[str] = None) -> Config:
    """
    Get or create global config instance.
    
    Args:
        config_file: Path to config file
        
    Returns:
        Config instance
    """
    global _config
    
    if _config is None:
        _config = Config(config_file)
    
    return _config
