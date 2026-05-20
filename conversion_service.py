"""
Conversion service that orchestrates XML to SQL conversion.
Separates business logic from UI.
"""
from typing import Optional, Dict, Any
from converters import ConverterFactory, SQLConverter
from xml_parser import XMLParser
import xml.etree.ElementTree as ET


class ConversionService:
    """
    Service for handling XML to SQL conversions.
    Provides high-level interface for conversion operations.
    """
    
    def __init__(self):
        self.parser = XMLParser()
        self.factory = ConverterFactory()
        self.last_converter_type = None
        self.last_error = None
    
    def convert_xml_string(self, xml_string: str, converter_type: Optional[str] = None) -> str:
        """
        Convert XML string to SQL.
        
        Args:
            xml_string: XML content as string
            converter_type: Type of converter to use. If None, auto-detect.
            
        Returns:
            SQL statement(s) or error message
        """
        self.last_error = None
        
        try:
            # Parse XML
            root = self.parser.parse_string(xml_string)
            
            # Detect or use specified converter
            if converter_type is None:
                converter_type = self.factory.detect_converter_type(root)
            
            self.last_converter_type = converter_type
            
            # Get converter and convert
            converter = self.factory.get_converter(converter_type)
            sql = converter.convert(root)
            
            return sql
            
        except ValueError as e:
            self.last_error = str(e)
            return f"-- Error: {str(e)}"
        except Exception as e:
            self.last_error = str(e)
            return f"-- Unexpected error: {str(e)}"
    
    def convert_xml_file(self, filepath: str, converter_type: Optional[str] = None) -> str:
        """
        Convert XML file to SQL.
        
        Args:
            filepath: Path to XML file
            converter_type: Type of converter to use. If None, auto-detect.
            
        Returns:
            SQL statement(s) or error message
        """
        self.last_error = None
        
        try:
            root = self.parser.parse_file(filepath)
            
            if converter_type is None:
                converter_type = self.factory.detect_converter_type(root)
            
            self.last_converter_type = converter_type
            
            converter = self.factory.get_converter(converter_type)
            sql = converter.convert(root)
            
            return sql
            
        except (FileNotFoundError, ValueError) as e:
            self.last_error = str(e)
            return f"-- Error: {str(e)}"
        except Exception as e:
            self.last_error = str(e)
            return f"-- Unexpected error: {str(e)}"
    
    def get_xml_structure(self, xml_string: str) -> str:
        """
        Get structure preview of XML.
        
        Args:
            xml_string: XML content
            
        Returns:
            String representation of XML structure
        """
        try:
            root = self.parser.parse_string(xml_string)
            return self.parser.get_element_tree_structure(root)
        except ValueError as e:
            return f"Error: {str(e)}"
    
    def get_supported_converters(self) -> list:
        """Get list of supported converter types."""
        return list(self.factory._converters.keys())
    
    def get_last_error(self) -> Optional[str]:
        """Get last error message."""
        return self.last_error
    
    def get_last_converter_type(self) -> Optional[str]:
        """Get type of last converter used."""
        return self.last_converter_type


class BatchConversionService:
    """
    Service for batch converting multiple XML files.
    """
    
    def __init__(self):
        self.service = ConversionService()
        self.results = []
    
    def convert_files(self, file_paths: list, converter_type: Optional[str] = None) -> Dict[str, str]:
        """
        Convert multiple XML files.
        
        Args:
            file_paths: List of XML file paths
            converter_type: Converter type to use
            
        Returns:
            Dictionary mapping file paths to SQL results
        """
        results = {}
        for filepath in file_paths:
            try:
                sql = self.service.convert_xml_file(filepath, converter_type)
                results[filepath] = sql
            except Exception as e:
                results[filepath] = f"-- Error: {str(e)}"
        
        self.results = results
        return results
    
    def get_results(self) -> Dict[str, str]:
        """Get last batch conversion results."""
        return self.results
