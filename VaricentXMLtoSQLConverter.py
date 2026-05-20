"""
DEPRECATED: Legacy XML to SQL Converter Module

This module is now DEPRECATED. The code has been refactored into a modular,
decoupled architecture. Please migrate to the new structure:

NEW MODULAR STRUCTURE:
  ├── main.py               : Application entry point
  ├── gui.py                : GUI layer (Tkinter)
  ├── conversion_service.py : Main conversion orchestration
  ├── converters.py         : Conversion strategies (Factory pattern)
  ├── xml_parser.py         : XML parsing utilities
  ├── config.py             : Configuration management
  └── utils.py              : Utility functions

MIGRATION GUIDE:
  OLD APPROACH (monolithic):
    from VaricentXMLtoSQLConverter import generic_xml_to_sql_inserts
    
  NEW APPROACH (modular):
    from conversion_service import ConversionService
    service = ConversionService()
    sql = service.convert_xml_string(xml_string)

BENEFITS OF NEW ARCHITECTURE:
  ✓ Separation of concerns (UI, business logic, data layer)
  ✓ Highly testable components
  ✓ Extensible converter system (Strategy pattern)
  ✓ Support for multiple XML formats with auto-detection
  ✓ Reusable service layer for programmatic access
  ✓ Better error handling and validation
  ✓ Configuration management
  ✓ Batch processing support

This file is kept for backward compatibility only.
All new code should use the modular components directly.
"""

# Import from new modular structure for backward compatibility
from conversion_service import ConversionService
from converters import GenericDataConverter, QueryDefinitionConverter, ConverterFactory
from xml_parser import XMLParser
import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET

__all__ = [
    'ConversionService',
    'GenericDataConverter',
    'QueryDefinitionConverter',
    'ConverterFactory',
    'XMLParser',
    'generic_xml_to_sql_inserts',
    'do_convert',
]


# Backward compatibility functions

def generic_xml_to_sql_inserts(xml_string):
    """
    DEPRECATED: Use ConversionService instead.

    Takes generic XML data and converts it into SQL INSERT statements.
    Example XML: <data><user><name>John</name><age>30</age></user></data>
    Produces: INSERT INTO user (name, age) VALUES ('John', '30');
    """
    service = ConversionService()
    return service.convert_xml_string(xml_string, converter_type="GenericData")


def generate_sql(root, level):
    """
    DEPRECATED: This function is now in QueryDefinitionConverter.
    Use converters.QueryDefinitionConverter instead.
    """
    converter = QueryDefinitionConverter()
    return converter.convert(root)

def generic_xml_to_sql_inserts(xml_string):
    """
    Takes generic XML data and converts it into SQL INSERT statements.
    Example XML: <data><user><name>John</name><age>30</age></user></data>
    Produces: INSERT INTO user (name, age) VALUES ('John', '30');
    """
    try:
        root = ET.fromstring(xml_string)
        sql_statements = []
        
        # Iterate through the first level of children (treating them as table rows)
        for row in root:
            table_name = row.tag
            columns = []
            values = []
            
            # Iterate through the second level (treating them as columns)
            for col in row:
                columns.append(col.tag)
                # Clean the text and escape single quotes for SQL safety
                val = col.text.strip() if col.text else ""
                val = val.replace("'", "''") 
                values.append(f"'{val}'")
            
            if columns:
                col_str = ", ".join(columns)
                val_str = ", ".join(values)
                sql = f"INSERT INTO {table_name} ({col_str}) VALUES ({val_str});"
                sql_statements.append(sql)
                
        return "\n".join(sql_statements)
        
    except Exception as e:
        return f"-- Error parsing XML: {str(e)}"


def populate_aliases(root):
    """
    DEPRECATED: This functionality is now handled internally
    by QueryDefinitionConverter.
    """
    pass


def do_convert(root, query_out, xmlString):
    """
    DEPRECATED: Use ConversionService and GUI module instead.

    Legacy conversion function - kept for backward compatibility.
    This function mixed UI and business logic. Use the new modular
    approach for better separation of concerns.

    New approach:
        from conversion_service import ConversionService
        service = ConversionService()
        sql = service.convert_xml_string(xmlString)
    """
    if xmlString == "":
        messagebox.showerror("Error", "No XML Provided.")
        return

    try:
        service = ConversionService()
        sql = service.convert_xml_string(xmlString)

        query_out.config(state="normal")
        query_out.delete("1.0", tk.END)
        query_out.insert("1.0", sql)

        # SQL Highlighting
        query_out.tag_remove("sqlkeywords", "1.0", tk.END)

        KEYWORDS = ["SELECT", "FROM", "JOIN", "LEFT JOIN", "ON", "WHERE",
                   "AS", "UNION ALL", "UNION", "AND", "OR", "IS NULL",
                   "IS NOT NULL", "INSERT", "INTO", "VALUES"]
        pattern = r"\b(" + "|".join(KEYWORDS) + r")\b"

        import re
        for m in re.finditer(pattern, query_out.get("1.0", tk.END), re.IGNORECASE):
            s = "1.0 + {} chars".format(m.start())
            e = "1.0 + {} chars".format(m.end())
            query_out.tag_add("sqlkeywords", s, e)

        query_out.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", "Failed to convert XML.")


def do_copy(root, text):
    """DEPRECATED: Use GUI module instead."""
    try:
        root.clipboard_clear()
        root.clipboard_append(text.get("1.0", tk.END))
    except:
        pass


def do_paste(root, text):
    """DEPRECATED: Use GUI module instead."""
    try:
        text_content = root.clipboard_get()
        text.delete("1.0", tk.END)
        text.insert("1.0", text_content)
    except:
        pass


def main():
    """
    DEPRECATED: Use gui.py and main.py instead.

    This launches the new GUI application. The old main() function
    is replaced by the new modular GUI.

    New approach:
        python main.py
    """
    # Import and run the new GUI
    from gui import main as gui_main
    gui_main()


if __name__ == "__main__":
    main()