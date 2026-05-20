"""
Base converter classes and implementations for XML to SQL conversion.
Implements Strategy pattern for different XML structures.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import xml.etree.ElementTree as ET
from xml_parser import XMLParser


class SQLConverter(ABC):
    """
    Abstract base class for XML to SQL converters.
    Defines interface for different conversion strategies.
    """
    
    def __init__(self):
        self.parser = XMLParser()
    
    @abstractmethod
    def convert(self, xml_element: ET.Element) -> str:
        """
        Convert XML element to SQL statement(s).
        
        Args:
            xml_element: Root XML element
            
        Returns:
            SQL statement(s) as string
        """
        pass
    
    def from_string(self, xml_string: str) -> str:
        """
        Convert XML string to SQL.
        
        Args:
            xml_string: XML content
            
        Returns:
            SQL statement(s)
        """
        try:
            root = self.parser.parse_string(xml_string)
            return self.convert(root)
        except ValueError as e:
            return f"-- Error: {str(e)}"
    
    def from_file(self, filepath: str) -> str:
        """
        Convert XML file to SQL.
        
        Args:
            filepath: Path to XML file
            
        Returns:
            SQL statement(s)
        """
        try:
            root = self.parser.parse_file(filepath)
            return self.convert(root)
        except (FileNotFoundError, ValueError) as e:
            return f"-- Error: {str(e)}"
    
    def escape_sql_value(self, value: str, is_numeric: bool = False) -> str:
        """
        Escape value for SQL.
        
        Args:
            value: Value to escape
            is_numeric: Whether value is numeric
            
        Returns:
            Escaped value for SQL
        """
        if is_numeric:
            return value
        
        value = str(value).replace("'", "''")
        return f"'{value}'"


class GenericDataConverter(SQLConverter):
    """
    Convert generic XML data (records) to SQL INSERT statements.
    
    Assumes structure:
        <root>
            <record>
                <column1>value1</column1>
                <column2>value2</column2>
            </record>
        </root>
    """
    
    def convert(self, xml_element: ET.Element) -> str:
        """
        Generate INSERT statements from XML data.
        """
        records = self.parser.extract_records(xml_element)
        
        if not records:
            return "-- No records found in XML"
        
        sql_statements = []
        
        # Assume all records have same structure (first record determines columns)
        columns = list(records[0].keys())
        table_name = self.parser.strip_namespace(xml_element.tag)
        
        for record in records:
            values = []
            for col in columns:
                val = record.get(col, "")
                values.append(self.escape_sql_value(val))
            
            col_str = ", ".join(columns)
            val_str = ", ".join(values)
            sql = f"INSERT INTO {table_name} ({col_str}) VALUES ({val_str});"
            sql_statements.append(sql)
        
        return "\n".join(sql_statements)


class QueryDefinitionConverter(SQLConverter):
    """
    Convert query definition XML to SQL.
    
    Supports: SELECT, FROM, WHERE, JOIN, UNION, etc.
    """
    
    def __init__(self):
        super().__init__()
        self.aliases = {}
        self.operators = {
            "equals": "=",
            "notequals": "!=",
            "lessthan": "<",
            "greaterthan": ">",
            "lessthanorequals": "<=",
            "greaterthanorequals": ">=",
            "in": "IN",
            "notin": "NOT IN",
            "like": "LIKE",
            "isnull": "IS NULL",
            "isnotnull": "IS NOT NULL",
        }
    
    def convert(self, xml_element: ET.Element) -> str:
        """Generate SQL from query definition."""
        self.aliases = {}
        return self._generate_sql(xml_element, 0)
    
    def _generate_sql(self, element: ET.Element, level: int) -> str:
        """Recursively generate SQL from XML elements."""
        sql = ""
        tag = self.parser.strip_namespace(element.tag)
        
        for child in element:
            child_tag = self.parser.strip_namespace(child.tag)
            
            # SELECT clause
            if child_tag == "select" and tag == "query":
                sql += "SELECT \n" + self._generate_sql(child, level)[:-2]
            
            # SELECT items
            elif child_tag == "select-item" and tag == "select":
                sql += self._generate_sql(child, level) + ",\n"
            
            # Table reference
            elif child_tag == "table":
                sql += f"{' ' * 4 * (level + 1)}{child.text}."
            
            # Column reference
            elif child_tag == "column":
                sql += child.text
            
            # Alias
            elif child_tag == "alias":
                if tag == "datasource":
                    comment = f" --{self.aliases.get(child.text, '')}" if child.text in self.aliases else ""
                    sql += f" AS {child.text}{comment}"
                else:
                    sql += f" AS {child.text}"
            
            # FROM clause
            elif child_tag == "from" and tag == "query":
                sql += "\n" + " " * 4 * level + "FROM \n" + self._generate_sql(child, level)
            
            # Datasource (table)
            elif child_tag == "datasource":
                sql += " " * 4 * (level + 1) + self._generate_sql(child, level + 1)
            
            # JOIN clauses
            elif child_tag == "joins" and tag == "query":
                sql += self._generate_sql(child, level)
            
            elif child_tag == "join" and tag == "joins":
                join_type = child.get("type", "inner").upper()
                if join_type == "LEFT":
                    sql += "\n" + " " * 4 * level + "LEFT JOIN\n"
                else:
                    sql += "\n" + " " * 4 * level + "JOIN\n"
                sql += self._generate_sql(child, level)
            
            # WHERE clause
            elif child_tag == "where" and tag == "query":
                sql += "\nWHERE\n" + self._generate_sql(child, level)
            
            # Constraints and conditions
            elif child_tag == "constraint":
                sql += self._generate_sql(child, level) + f" {element.get('type', 'AND').upper()}\n"
            
            # Operators
            elif child_tag == "operator":
                op_text = child.text or ""
                sql += self.operators.get(op_text, op_text)
                sql += self._generate_sql(child, level)
            
            # Literals
            elif child_tag == "literal":
                lit_type = child.get("type", "string")
                if lit_type == "decimal":
                    sql += child.text or ""
                else:
                    sql += f"'{child.text or ''}'"
            
            # Union
            elif child_tag == "union":
                sql += "\n\nUNION ALL\n\n" + self._generate_sql(child, level)
            
            # Mappings (aliases)
            elif child_tag == "mapping":
                if len(child) >= 2:
                    alias_tag = self.parser.strip_namespace(child[0].tag)
                    name_tag = self.parser.strip_namespace(child[1].tag)
                    if alias_tag == "alias" and name_tag == "name":
                        self.aliases[child[0].text or ""] = child[1].text or ""
                sql += self._generate_sql(child, level)
            
            else:
                sql += self._generate_sql(child, level)
        
        return sql


class ConverterFactory:
    """
    Factory for creating appropriate converter based on XML structure.
    """
    
    _converters = {
        "GenericData": GenericDataConverter,
        "QueryDefinition": QueryDefinitionConverter,
    }
    
    @classmethod
    def get_converter(cls, converter_type: str) -> SQLConverter:
        """
        Get converter instance by type.
        
        Args:
            converter_type: Type of converter (GenericData, QueryDefinition)
            
        Returns:
            Converter instance
            
        Raises:
            ValueError: If converter type not found
        """
        if converter_type not in cls._converters:
            raise ValueError(f"Unknown converter type: {converter_type}. Available: {list(cls._converters.keys())}")
        
        return cls._converters[converter_type]()
    
    @classmethod
    def detect_converter_type(cls, xml_element: ET.Element) -> str:
        """
        Auto-detect converter type based on XML structure.
        
        Args:
            xml_element: Root XML element
            
        Returns:
            Detected converter type
        """
        tag = XMLParser.strip_namespace(xml_element.tag)
        
        # Check for query definition structure
        if tag == "query" or tag == "datasource":
            return "QueryDefinition"
        
        # Check if children have query-like tags
        for child in xml_element:
            child_tag = XMLParser.strip_namespace(child.tag)
            if child_tag in ("query", "select", "from", "where", "join", "union"):
                return "QueryDefinition"
        
        # Default to generic data converter
        return "GenericData"
    
    @classmethod
    def register_converter(cls, name: str, converter_class: type):
        """
        Register custom converter.
        
        Args:
            name: Converter name
            converter_class: Converter class (should inherit from SQLConverter)
        """
        if not issubclass(converter_class, SQLConverter):
            raise TypeError("Converter must inherit from SQLConverter")
        
        cls._converters[name] = converter_class
