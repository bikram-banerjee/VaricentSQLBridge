"""
Examples demonstrating how to use the XML to SQL Converter.

This file shows various ways to use the modular components.
"""

# =============================================================================
# EXAMPLE 1: Basic XML to SQL Conversion using ConversionService
# =============================================================================

def example_basic_conversion():
    """Basic conversion using ConversionService."""
    from conversion_service import ConversionService
    
    # Initialize service
    service = ConversionService()
    
    # XML data
    xml_data = """
    <customers>
        <customer><id>1</id><name>Alice</name><email>alice@example.com</email></customer>
        <customer><id>2</id><name>Bob</name><email>bob@example.com</email></customer>
    </customers>
    """
    
    # Convert to SQL
    sql = service.convert_xml_string(xml_data)
    print("Generated SQL:")
    print(sql)
    # Output:
    # INSERT INTO customers (id, name, email) VALUES ('1', 'Alice', 'alice@example.com');
    # INSERT INTO customers (id, name, email) VALUES ('2', 'Bob', 'bob@example.com');


# =============================================================================
# EXAMPLE 2: File-based Conversion
# =============================================================================

def example_file_conversion():
    """Convert XML file to SQL."""
    from conversion_service import ConversionService
    
    service = ConversionService()
    
    # Convert file
    sql = service.convert_xml_file("data/sample.xml")
    print("Generated SQL from file:")
    print(sql)


# =============================================================================
# EXAMPLE 3: Using Specific Converter Type
# =============================================================================

def example_specific_converter():
    """Use a specific converter type."""
    from conversion_service import ConversionService
    
    service = ConversionService()
    
    xml_data = """
    <data>
        <user><name>John</name><age>30</age></user>
    </data>
    """
    
    # Explicitly use GenericData converter
    sql = service.convert_xml_string(xml_data, converter_type="GenericData")
    print("Using GenericData converter:")
    print(sql)


# =============================================================================
# EXAMPLE 4: Direct Converter Usage
# =============================================================================

def example_direct_converter():
    """Use converter directly."""
    from converters import GenericDataConverter
    
    converter = GenericDataConverter()
    
    xml_data = """
    <products>
        <product><id>1</id><name>Widget</name><price>9.99</price></product>
    </products>
    """
    
    sql = converter.from_string(xml_data)
    print("Direct converter usage:")
    print(sql)


# =============================================================================
# EXAMPLE 5: Auto-detection of Converter Type
# =============================================================================

def example_auto_detection():
    """Auto-detect appropriate converter."""
    from conversion_service import ConversionService
    
    service = ConversionService()
    
    # Generic data XML
    xml_generic = "<users><user><name>Alice</name></user></users>"
    sql1 = service.convert_xml_string(xml_generic)  # Auto-detects GenericData
    print("Auto-detected converter type:", service.get_last_converter_type())
    
    # Query definition XML
    xml_query = "<query><select></select><from><datasource><table>users</table></datasource></from></query>"
    sql2 = service.convert_xml_string(xml_query)  # Auto-detects QueryDefinition
    print("Auto-detected converter type:", service.get_last_converter_type())


# =============================================================================
# EXAMPLE 6: Batch Processing Multiple Files
# =============================================================================

def example_batch_processing():
    """Process multiple XML files in batch."""
    from conversion_service import BatchConversionService
    
    batch_service = BatchConversionService()
    
    files = [
        "data/customers.xml",
        "data/orders.xml",
        "data/products.xml"
    ]
    
    results = batch_service.convert_files(files)
    
    # Process results
    for filepath, sql in results.items():
        print(f"\n=== {filepath} ===")
        print(sql)


# =============================================================================
# EXAMPLE 7: XML Parsing and Analysis
# =============================================================================

def example_xml_parsing():
    """Use XMLParser for analysis."""
    from xml_parser import XMLParser
    
    parser = XMLParser()
    
    xml_data = """
    <database>
        <tables>
            <table name="users">
                <row><id>1</id><name>Alice</name></row>
            </table>
        </tables>
    </database>
    """
    
    root = parser.parse_string(xml_data)
    
    # Convert to dictionary
    data_dict = parser.to_dict(root)
    print("XML as dictionary:")
    print(data_dict)
    
    # Get structure preview
    structure = parser.get_element_tree_structure(root)
    print("\nXML structure:")
    print(structure)


# =============================================================================
# EXAMPLE 8: Error Handling
# =============================================================================

def example_error_handling():
    """Demonstrate error handling."""
    from conversion_service import ConversionService
    
    service = ConversionService()
    
    # Invalid XML
    invalid_xml = "<unclosed><tag>"
    sql = service.convert_xml_string(invalid_xml)
    print("Result with invalid XML:")
    print(sql)
    
    if service.get_last_error():
        print(f"Error: {service.get_last_error()}")


# =============================================================================
# EXAMPLE 9: Custom Converter Registration
# =============================================================================

def example_custom_converter():
    """Register and use a custom converter."""
    from converters import SQLConverter, ConverterFactory
    import xml.etree.ElementTree as ET
    
    class CustomXMLConverter(SQLConverter):
        """Custom converter for specific XML format."""
        
        def convert(self, xml_element: ET.Element) -> str:
            """Custom conversion logic."""
            return "-- Custom conversion result"
    
    # Register the custom converter
    ConverterFactory.register_converter("Custom", CustomXMLConverter)
    
    # Use it
    service = __import__('conversion_service').ConversionService()
    sql = service.convert_xml_string("<data></data>", converter_type="Custom")
    print("Custom converter result:")
    print(sql)


# =============================================================================
# EXAMPLE 10: Using Configuration
# =============================================================================

def example_configuration():
    """Use configuration management."""
    from config import get_config
    
    config = get_config()
    
    # Get configuration values
    auto_detect = config.get("converters.auto_detect")
    print(f"Auto-detect enabled: {auto_detect}")
    
    # Set configuration values
    config.set("converters.default_converter", "QueryDefinition")
    config.save()
    
    print("Configuration saved")


# =============================================================================
# EXAMPLE 11: Utility Functions
# =============================================================================

def example_utilities():
    """Use utility functions."""
    from utils import SQLFormatter, XMLValidator, TextProcessor
    
    # Validate XML
    xml_data = "<root><child>value</child></root>"
    is_valid = XMLValidator.is_valid_xml(xml_data)
    print(f"XML is valid: {is_valid}")
    
    # Format SQL
    sql = "SELECT * FROM users WHERE id = 1"
    formatted = SQLFormatter.prettify(sql)
    print("Formatted SQL:")
    print(formatted)
    
    # Process text
    text = "It's a test"
    escaped = TextProcessor.escape_quotes(text)
    print(f"Escaped text: {escaped}")


# =============================================================================
# EXAMPLE 12: GUI Application
# =============================================================================

def example_gui_application():
    """Launch the GUI application."""
    from gui import main
    
    # Start GUI
    main()


# =============================================================================
# RUN EXAMPLES
# =============================================================================

if __name__ == "__main__":
    print("XML to SQL Converter - Examples\n")
    print("=" * 60)
    
    print("\n1. Basic Conversion")
    print("-" * 60)
    example_basic_conversion()
    
    print("\n2. Specific Converter Type")
    print("-" * 60)
    example_specific_converter()
    
    print("\n3. Auto-detection")
    print("-" * 60)
    example_auto_detection()
    
    print("\n4. XML Parsing")
    print("-" * 60)
    example_xml_parsing()
    
    print("\n5. Error Handling")
    print("-" * 60)
    example_error_handling()
    
    print("\n6. Utilities")
    print("-" * 60)
    example_utilities()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
