"""
Utility functions for XML to SQL Converter.
"""
from typing import List, Dict, Any
import re


class SQLFormatter:
    """Format and beautify SQL statements."""
    
    SQL_KEYWORDS = [
        "SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN",
        "OUTER JOIN", "CROSS JOIN", "ON", "AND", "OR", "NOT", "AS", "UNION",
        "UNION ALL", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
        "CREATE", "TABLE", "ALTER", "DROP", "IF", "EXISTS", "PRIMARY", "KEY",
        "FOREIGN", "UNIQUE", "CHECK", "DEFAULT", "CONSTRAINT", "LIKE", "IN",
        "BETWEEN", "IS", "NULL", "GROUP", "BY", "ORDER", "HAVING", "LIMIT",
        "OFFSET", "CASE", "WHEN", "THEN", "ELSE", "END", "CAST", "DISTINCT"
    ]
    
    @staticmethod
    def prettify(sql: str, indent: int = 4) -> str:
        """
        Format SQL for better readability.
        
        Args:
            sql: SQL statement
            indent: Indentation level
            
        Returns:
            Formatted SQL
        """
        indent_str = " " * indent
        
        # Add line breaks before keywords
        for keyword in SQLFormatter.SQL_KEYWORDS:
            pattern = rf'\b{keyword}\b'
            sql = re.sub(pattern, f"\n{keyword}", sql, flags=re.IGNORECASE)
        
        # Clean up multiple spaces
        sql = re.sub(r'\n\s+', '\n', sql)
        sql = re.sub(r'\s+', ' ', sql)
        
        return sql.strip()
    
    @staticmethod
    def highlight_keywords(sql: str) -> Dict[str, Any]:
        """
        Find and return positions of SQL keywords.
        
        Args:
            sql: SQL statement
            
        Returns:
            Dictionary with keyword positions
        """
        keywords_found = {}
        
        for keyword in SQLFormatter.SQL_KEYWORDS:
            pattern = rf'\b{keyword}\b'
            for match in re.finditer(pattern, sql, re.IGNORECASE):
                if match.group() not in keywords_found:
                    keywords_found[match.group()] = []
                keywords_found[match.group()].append({
                    'start': match.start(),
                    'end': match.end()
                })
        
        return keywords_found


class XMLValidator:
    """Validate XML content."""
    
    @staticmethod
    def is_valid_xml(xml_string: str) -> bool:
        """
        Check if string is valid XML.
        
        Args:
            xml_string: XML content
            
        Returns:
            True if valid, False otherwise
        """
        if not xml_string or not xml_string.strip():
            return False
        
        try:
            import xml.etree.ElementTree as ET
            ET.fromstring(xml_string)
            return True
        except ET.ParseError:
            return False
    
    @staticmethod
    def get_validation_error(xml_string: str) -> str:
        """
        Get validation error message.
        
        Args:
            xml_string: XML content
            
        Returns:
            Error message or empty string if valid
        """
        if not xml_string or not xml_string.strip():
            return "Empty XML string"
        
        try:
            import xml.etree.ElementTree as ET
            ET.fromstring(xml_string)
            return ""
        except ET.ParseError as e:
            return str(e)


class TextProcessor:
    """Process and manipulate text."""
    
    @staticmethod
    def escape_quotes(text: str, quote_char: str = "'") -> str:
        """
        Escape quotes in text.
        
        Args:
            text: Text to escape
            quote_char: Quote character to escape
            
        Returns:
            Escaped text
        """
        if quote_char == "'":
            return text.replace("'", "''")
        elif quote_char == '"':
            return text.replace('"', '""')
        return text
    
    @staticmethod
    def unescape_quotes(text: str, quote_char: str = "'") -> str:
        """
        Unescape quotes in text.
        
        Args:
            text: Text to unescape
            quote_char: Quote character to unescape
            
        Returns:
            Unescaped text
        """
        if quote_char == "'":
            return text.replace("''", "'")
        elif quote_char == '"':
            return text.replace('""', '"')
        return text
    
    @staticmethod
    def truncate(text: str, length: int = 50, suffix: str = "...") -> str:
        """
        Truncate text to specified length.
        
        Args:
            text: Text to truncate
            length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated text
        """
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix


class Logger:
    """Simple logging utility."""
    
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    
    def __init__(self, level: int = INFO):
        """Initialize logger."""
        self.level = level
        self.messages = []
    
    def debug(self, message: str):
        """Log debug message."""
        if self.level <= self.DEBUG:
            self._log("DEBUG", message)
    
    def info(self, message: str):
        """Log info message."""
        if self.level <= self.INFO:
            self._log("INFO", message)
    
    def warning(self, message: str):
        """Log warning message."""
        if self.level <= self.WARNING:
            self._log("WARNING", message)
    
    def error(self, message: str):
        """Log error message."""
        if self.level <= self.ERROR:
            self._log("ERROR", message)
    
    def _log(self, level: str, message: str):
        """Internal logging method."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.messages.append(log_entry)
        print(log_entry)
    
    def get_logs(self) -> List[str]:
        """Get all logged messages."""
        return self.messages.copy()
    
    def clear(self):
        """Clear logs."""
        self.messages.clear()
