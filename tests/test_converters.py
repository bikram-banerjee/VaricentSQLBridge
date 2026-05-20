"""
Unit tests for Converters module.
"""
import unittest
from converters import GenericDataConverter, QueryDefinitionConverter, ConverterFactory
import xml.etree.ElementTree as ET


class TestGenericDataConverter(unittest.TestCase):
    """Test cases for GenericDataConverter."""
    
    def setUp(self):
        self.converter = GenericDataConverter()
    
    def test_simple_insert_conversion(self):
        """Test simple INSERT statement generation."""
        xml_string = """
        <users>
            <user><name>John</name><age>30</age></user>
        </users>
        """
        sql = self.converter.from_string(xml_string)
        
        self.assertIn("INSERT INTO users", sql)
        self.assertIn("John", sql)
        self.assertIn("30", sql)
    
    def test_multiple_records_conversion(self):
        """Test conversion of multiple records."""
        xml_string = """
        <products>
            <product><id>1</id><name>Item1</name><price>10.99</price></product>
            <product><id>2</id><name>Item2</name><price>20.99</price></product>
        </products>
        """
        sql = self.converter.from_string(xml_string)
        statements = sql.strip().split('\n')
        
        self.assertEqual(len(statements), 2)
        self.assertIn("INSERT INTO products", statements[0])
    
    def test_empty_xml_handling(self):
        """Test handling of empty XML."""
        xml_string = "<data></data>"
        sql = self.converter.from_string(xml_string)
        
        self.assertIn("No records found", sql)


class TestQueryDefinitionConverter(unittest.TestCase):
    """Test cases for QueryDefinitionConverter."""
    
    def setUp(self):
        self.converter = QueryDefinitionConverter()
    
    def test_basic_query_generation(self):
        """Test basic query generation."""
        xml_string = """
        <query>
            <select>
                <select-item>
                    <table>users</table>
                    <column>name</column>
                </select-item>
            </select>
            <from>
                <datasource>
                    <table>users</table>
                </datasource>
            </from>
        </query>
        """
        root = ET.fromstring(xml_string)
        sql = self.converter.convert(root)
        
        self.assertIn("SELECT", sql)
        self.assertIn("FROM", sql)
        self.assertIn("users", sql)


class TestConverterFactory(unittest.TestCase):
    """Test cases for ConverterFactory."""
    
    def test_factory_get_converter(self):
        """Test factory converter retrieval."""
        converter = ConverterFactory.get_converter("GenericData")
        self.assertIsInstance(converter, GenericDataConverter)
    
    def test_invalid_converter_type(self):
        """Test invalid converter type."""
        with self.assertRaises(ValueError):
            ConverterFactory.get_converter("InvalidType")
    
    def test_auto_detect_generic_data(self):
        """Test auto-detection of generic data."""
        xml_string = "<users><user><name>John</name></user></users>"
        root = ET.fromstring(xml_string)
        converter_type = ConverterFactory.detect_converter_type(root)
        
        self.assertEqual(converter_type, "GenericData")
    
    def test_auto_detect_query_definition(self):
        """Test auto-detection of query definition."""
        xml_string = "<query><select></select></query>"
        root = ET.fromstring(xml_string)
        converter_type = ConverterFactory.detect_converter_type(root)
        
        self.assertEqual(converter_type, "QueryDefinition")


if __name__ == '__main__':
    unittest.main()
