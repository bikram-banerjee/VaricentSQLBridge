# Quick Start Guide

Get up and running with the XML to SQL Converter in 5 minutes!

## Installation

### 1. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### GUI Mode (Recommended)

```bash
python main.py
```

This launches the interactive GUI where you can:
- Paste or load XML files
- Convert to SQL with one click
- Copy results to clipboard
- Save SQL to file

### Command Line Mode

```bash
python -c "
from conversion_service import ConversionService

xml_data = '''
<users>
    <user><name>John</name><age>30</age></user>
    <user><name>Jane</name><age>25</age></user>
</users>
'''

service = ConversionService()
sql = service.convert_xml_string(xml_data)
print(sql)
"
```

## Common Use Cases

### Use Case 1: Convert Generic Data XML

**Input XML:**
```xml
<customers>
    <customer><id>1</id><name>Alice</name><email>alice@example.com</email></customer>
    <customer><id>2</id><name>Bob</name><email>bob@example.com</email></customer>
</customers>
```

**Output SQL:**
```sql
INSERT INTO customers (id, name, email) VALUES ('1', 'Alice', 'alice@example.com');
INSERT INTO customers (id, name, email) VALUES ('2', 'Bob', 'bob@example.com');
```

**Code:**
```python
from conversion_service import ConversionService

service = ConversionService()
sql = service.convert_xml_string(xml_data)
print(sql)
```

### Use Case 2: Convert from File

```python
from conversion_service import ConversionService

service = ConversionService()
sql = service.convert_xml_file("path/to/file.xml")
print(sql)
```

### Use Case 3: Batch Processing

```python
from conversion_service import BatchConversionService

batch = BatchConversionService()
files = ["file1.xml", "file2.xml", "file3.xml"]
results = batch.convert_files(files)

for filepath, sql in results.items():
    print(f"{filepath}:\n{sql}\n")
```

### Use Case 4: Programmatic Access

```python
from converters import ConverterFactory
from xml_parser import XMLParser

# Parse XML
parser = XMLParser()
root = parser.parse_file("data.xml")

# Auto-detect converter
factory = ConverterFactory()
converter_type = factory.detect_converter_type(root)
print(f"Using converter: {converter_type}")

# Convert
converter = factory.get_converter(converter_type)
sql = converter.convert(root)
print(sql)
```

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=.
```

### Run Specific Test

```bash
pytest tests/test_converters.py::TestGenericDataConverter::test_simple_insert_conversion
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'xml_parser'"

**Solution:**
Ensure you're running from the project root directory:
```bash
cd path/to/XML_to_SQL_Converter
python main.py
```

### Issue: GUI doesn't start

**Solution:**
Check if tkinter is installed:
```bash
python -c "import tkinter"
```

If not, install it:
- **Windows**: Already included with Python
- **macOS**: Already included with Python
- **Linux**: `sudo apt-get install python3-tk`

### Issue: "Invalid XML" error

**Solution:**
Ensure your XML is well-formed:
- All tags properly closed
- Proper nesting
- Special characters escaped

### Issue: Unexpected conversion output

**Solution:**
Try using the "XML Structure" tool in the GUI (Tools → XML Structure) to see how your XML is being interpreted, then verify the converter type being used.

## Examples

### Example 1: Simple Insert

```python
from conversion_service import ConversionService

xml = """<products>
    <product><id>1</id><name>Laptop</name><price>999.99</price></product>
</products>"""

service = ConversionService()
sql = service.convert_xml_string(xml)
print(sql)
# Output: INSERT INTO products (id, name, price) VALUES ('1', 'Laptop', '999.99');
```

### Example 2: Multiple Records

```python
from conversion_service import ConversionService

xml = """<orders>
    <order><id>1</id><customer>Alice</customer><amount>150</amount></order>
    <order><id>2</id><customer>Bob</customer><amount>200</amount></order>
    <order><id>3</id><customer>Charlie</customer><amount>175</amount></order>
</orders>"""

service = ConversionService()
sql = service.convert_xml_string(xml)
print(sql)
```

### Example 3: Auto-Detection

```python
from conversion_service import ConversionService

# Generic data
xml1 = "<users><user><name>John</name></user></users>"
service = ConversionService()
sql1 = service.convert_xml_string(xml1)
print(f"Converter: {service.get_last_converter_type()}")  # GenericData

# Query definition
xml2 = "<query><select></select><from><datasource><table>users</table></datasource></from></query>"
sql2 = service.convert_xml_string(xml2)
print(f"Converter: {service.get_last_converter_type()}")  # QueryDefinition
```

## Next Steps

1. **Read ARCHITECTURE.md** for design overview
2. **Explore examples.py** for more advanced examples
3. **Check CONTRIBUTING.md** for development guidelines
4. **Review tests/** for test examples

## Getting Help

- **Read Documentation**: Check README.md and ARCHITECTURE.md
- **Review Examples**: See examples.py for common patterns
- **Check Tests**: Unit tests demonstrate expected behavior
- **GUI Help**: Tools menu has helpful options

## Tips & Tricks

### Tip 1: Use Converter Selection
For more control, select a specific converter in the GUI instead of auto-detection.

### Tip 2: Preview XML Structure
Use Tools → XML Structure to understand how your XML will be interpreted.

### Tip 3: Validate Before Converting
Use the XML validation in status bar to catch issues early.

### Tip 4: Save Often
Use File → Save SQL to preserve your conversions.

### Tip 5: Check Error Messages
Error messages are in the SQL output area - read them carefully for clues.

## Performance Notes

- **Small files** (< 1MB): Instant conversion
- **Medium files** (1-10MB): Few seconds
- **Large files** (> 10MB): Consider using batch service
- **Streaming**: Use batch service for processing many files

## Frequently Asked Questions

**Q: How do I handle special characters in XML?**
A: The converter automatically escapes special characters. Just paste your XML as-is.

**Q: Can I customize the SQL output?**
A: You can register custom converters. See CONTRIBUTING.md for details.

**Q: How do I handle XML with namespaces?**
A: The parser automatically strips namespaces. Use the XML as-is.

**Q: Can I process files from command line?**
A: Yes! Use `conversion_service.py` directly. See examples.py for code.

**Q: Is there an API?**
A: `ConversionService` provides a clean API. See examples.py for usage.

## Keyboard Shortcuts (GUI)

- `Ctrl+O`: Open XML file
- `Ctrl+S`: Save SQL to file
- `Ctrl+A`: Select all text
- Right-click: Context menu

## Additional Resources

- **README.md**: Full project overview
- **ARCHITECTURE.md**: Design patterns and structure
- **CONTRIBUTING.md**: Development guidelines
- **examples.py**: Code examples
- **tests/**: Test examples
- **VaricentXMLtoSQLConverter.py**: Legacy API (backward compatible)

## Support

For issues, feature requests, or questions:
1. Check existing documentation
2. Review the examples
3. Look at unit tests
4. Open an issue on GitHub

---

**Happy Converting!** 🎉
