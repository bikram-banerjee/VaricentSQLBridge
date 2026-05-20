"""
Unit tests for XML Parser module.
"""
import unittest
from xml_parser import XMLParser
import xml.etree.ElementTree as ET


class TestXMLParser(unittest.TestCase):
    """Test cases for XMLParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = XMLParser()
    
    def test_strip_namespace(self):
        """Test namespace stripping."""
        self.assertEqual(self.parser.strip_namespace("{http://example.com}tag"), "tag")
        self.assertEqual(self.parser.strip_namespace("tag"), "tag")
        self.assertEqual(self.parser.strip_namespace(""), "")
    
    def test_parse_valid_xml(self):
        """Test parsing valid XML."""
        xml_string = "<root><child>value</child></root>"
        root = self.parser.parse_string(xml_string)
        self.assertIsNotNone(root)
        self.assertEqual(root.tag, "root")
    
    def test_parse_invalid_xml(self):
        """Test parsing invalid XML."""
        xml_string = "<root><unclosed>"
        with self.assertRaises(ValueError):
            self.parser.parse_string(xml_string)
    
    def test_parse_empty_xml(self):
        """Test parsing empty XML."""
        with self.assertRaises(ValueError):
            self.parser.parse_string("")
    
    def test_extract_records(self):
        """Test record extraction from XML."""
        xml_string = """
        <users>
            <user><name>John</name><age>30</age></user>
            <user><name>Jane</name><age>25</age></user>
        </users>
        """
        root = self.parser.parse_string(xml_string)
        records = self.parser.extract_records(root)
        
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['name'], 'John')
        self.assertEqual(records[0]['age'], '30')
        self.assertEqual(records[1]['name'], 'Jane')
    
    def test_to_dict_conversion(self):
        """Test XML to dictionary conversion."""
        xml_string = "<root><child attr='value'>text</child></root>"
        root = self.parser.parse_string(xml_string)
        result = self.parser.to_dict(root)
        
        self.assertIn('root', result)


class TestXMLParserIntegration(unittest.TestCase):
    """Integration tests for XMLParser."""
    
    def setUp(self):
        self.parser = XMLParser()
    
    def test_complex_xml_structure(self):
        """Test parsing complex XML structure."""
        xml_string = """
        <database>
            <tables>
                <table name="users">
                    <row><id>1</id><name>Alice</name></row>
                    <row><id>2</id><name>Bob</name></row>
                </table>
            </tables>
        </database>
        """
        root = self.parser.parse_string(xml_string)
        self.assertIsNotNone(root)
        self.assertEqual(root.tag, 'database')


if __name__ == '__main__':
    unittest.main()
