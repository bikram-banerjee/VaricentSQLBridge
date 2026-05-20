"""
Generic XML parser for handling various XML structures.
"""
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Tuple


class XMLParser:
    """
    Generic XML parser that can handle various XML structures.
    """
    
    def __init__(self):
        self.namespaces = {}
    
    @staticmethod
    def strip_namespace(tag: str) -> str:
        """Remove XML namespace from tag if present."""
        if tag and tag.startswith("{"):
            return tag.split("}")[1]
        return tag
    
    def parse_string(self, xml_string: str) -> Optional[ET.Element]:
        """
        Parse XML from string.
        
        Args:
            xml_string: XML content as string
            
        Returns:
            Root element or None if parsing fails
            
        Raises:
            ValueError: If XML is invalid
        """
        if not xml_string or not xml_string.strip():
            raise ValueError("Empty XML string provided")
        
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {str(e)}")
    
    def parse_file(self, filepath: str) -> Optional[ET.Element]:
        """
        Parse XML from file.
        
        Args:
            filepath: Path to XML file
            
        Returns:
            Root element or None if parsing fails
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If XML is invalid
        """
        try:
            tree = ET.parse(filepath)
            return tree.getroot()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML in file: {str(e)}")
    
    def to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        Convert XML element to dictionary recursively.
        
        Args:
            element: XML element to convert
            
        Returns:
            Dictionary representation of XML
        """
        result = {}
        tag = self.strip_namespace(element.tag)
        
        # Add attributes
        if element.attrib:
            result['@attributes'] = {self.strip_namespace(k): v for k, v in element.attrib.items()}
        
        # Add text if present
        if element.text and element.text.strip():
            result['#text'] = element.text.strip()
        
        # Add children
        children_dict = {}
        for child in element:
            child_tag = self.strip_namespace(child.tag)
            child_data = self.to_dict(child)
            
            if child_tag in children_dict:
                # Multiple children with same tag - convert to list
                if not isinstance(children_dict[child_tag], list):
                    children_dict[child_tag] = [children_dict[child_tag]]
                children_dict[child_tag].append(child_data)
            else:
                children_dict[child_tag] = child_data
        
        result.update(children_dict)
        return {tag: result} if not result.get('#text') or element else result
    
    def extract_records(self, root: ET.Element) -> List[Dict[str, str]]:
        """
        Extract records from XML assuming first level children are table rows.
        
        Args:
            root: Root XML element
            
        Returns:
            List of dictionaries representing records
            
        Example:
            <data>
                <user><name>John</name><age>30</age></user>
                <user><name>Jane</name><age>25</age></user>
            </data>
            
            Returns: [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
        """
        records = []
        for element in root:
            record = {}
            for child in element:
                tag = self.strip_namespace(child.tag)
                text = child.text.strip() if child.text else ""
                record[tag] = text
            if record:
                records.append(record)
        
        return records
    
    def find_element_path(self, root: ET.Element, target_tag: str) -> Optional[List[str]]:
        """
        Find path to first element with target tag.
        
        Args:
            root: Root element to search from
            target_tag: Tag name to find
            
        Returns:
            List of tag names representing path, or None
        """
        def search_recursive(element, path):
            if self.strip_namespace(element.tag) == target_tag:
                return path + [self.strip_namespace(element.tag)]
            
            for child in element:
                result = search_recursive(child, path + [self.strip_namespace(element.tag)])
                if result:
                    return result
            
            return None
        
        return search_recursive(root, [])
    
    def get_element_tree_structure(self, root: ET.Element, max_depth: int = 3) -> str:
        """
        Get string representation of XML tree structure.
        
        Args:
            root: Root element
            max_depth: Maximum depth to traverse
            
        Returns:
            String representation of tree structure
        """
        def format_element(element, depth=0):
            if depth > max_depth:
                return ""
            
            indent = "  " * depth
            tag = self.strip_namespace(element.tag)
            attrs = " ".join(f'{k}="{v}"' for k, v in element.attrib.items())
            
            text_preview = ""
            if element.text and element.text.strip():
                preview = element.text.strip()[:30]
                text_preview = f' -> "{preview}"' if preview else ""
            
            line = f"{indent}{tag}"
            if attrs:
                line += f" [{attrs}]"
            line += text_preview
            
            children = "\n".join(format_element(child, depth + 1) for child in element)
            
            if children:
                return line + "\n" + children
            return line
        
        return format_element(root)
