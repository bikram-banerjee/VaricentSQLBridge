# XML to SQL Converter - Decoupled Architecture

A flexible, modular XML to SQL converter that handles various XML file formats with auto-detection capabilities.

## 🏗️ Architecture Overview

The project follows a **decoupled, modular design** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│                   GUI Module (gui.py)               │
│              Tkinter UI - No Business Logic         │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            ConversionService (conversion_service.py)│
│              Orchestrates Conversions               │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────────────┐  ┌─────────────────────┐
│ Converters (Factory) │  │  XMLParser          │
│                      │  │                     │
│ • GenericData        │  │ • Parse XML string  │
│ • QueryDefinition    │  │ • Parse XML file    │
│ • Custom (extensible)│  │ • Extract records   │
└──────────────────────┘  │ • Analyze structure │
                          └─────────────────────┘
```

## 📁 Project Structure

```
XML_to_SQL_Converter/
├── main.py                      # Application entry point
├── gui.py                       # GUI layer (Tkinter UI)
├── conversion_service.py        # Business logic orchestration
├── converters.py                # Conversion strategies (Factory pattern)
├── xml_parser.py                # XML parsing utilities
├── config.py                    # Configuration management
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
```

## 🔑 Key Modules

### 1. **xml_parser.py** - XML Parsing Layer
- Generic XML parsing and manipulation
- Namespace handling
- Record extraction from XML
- Tree structure analysis

```python
from xml_parser import XMLParser

parser = XMLParser()
root = parser.parse_string(xml_content)
records = parser.extract_records(root)
```

### 2. **converters.py** - Conversion Strategies
Implements **Strategy Pattern** for different conversion types:

- **GenericDataConverter**: For generic data XML → INSERT statements
- **QueryDefinitionConverter**: For query definition XML → SELECT statements
- **ConverterFactory**: Auto-detects and creates appropriate converters
- Extensible for custom converters

```python
from converters import ConverterFactory

# Auto-detect
factory = ConverterFactory()
converter_type = factory.detect_converter_type(root)

# Or specify explicitly
converter = factory.get_converter("GenericData")
sql = converter.convert(root)
```

### 3. **conversion_service.py** - Business Logic
High-level service that orchestrates conversions:

- Handles XML string/file conversions
- Auto-detection of converter types
- Error handling and reporting
- Batch conversion support

```python
from conversion_service import ConversionService

service = ConversionService()
sql = service.convert_xml_string(xml_string)
# or
sql = service.convert_xml_file(filepath)
```

### 4. **gui.py** - User Interface
Tkinter-based GUI completely decoupled from business logic:

- File operations
- Context menus
- SQL syntax highlighting
- Status bar
- No conversion logic in GUI

### 5. **config.py** - Configuration Management
Centralized configuration handling:

```python
from config import get_config

config = get_config()
auto_detect = config.get("converters.auto_detect")
config.set("converters.default_converter", "QueryDefinition")
config.save()
```

## 🎯 Features

### Supported XML Formats

1. **Generic Data XML**
   ```xml
   <data>
       <user><name>John</name><age>30</age></user>
       <user><name>Jane</name><age>25</age></user>
   </data>
   ```
   Converts to: `INSERT INTO user (name, age) VALUES ('John', '30');`

2. **Query Definition XML**
   ```xml
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
   ```

### Auto-Detection
Automatically detects XML format and applies the correct converter.

### Extensibility
Register custom converters:

```python
from converters import ConverterFactory, SQLConverter

class CustomConverter(SQLConverter):
    def convert(self, xml_element):
        # Your conversion logic
        pass

ConverterFactory.register_converter("Custom", CustomConverter)
```

## 🚀 Usage

### GUI Application
```bash
python main.py
```

### Programmatic Usage
```python
from conversion_service import ConversionService

service = ConversionService()

# Convert XML string
xml_content = "<data><user><name>John</name></user></data>"
sql = service.convert_xml_string(xml_content)
print(sql)

# Convert XML file
sql = service.convert_xml_file("data.xml")

# Get structure preview
structure = service.get_xml_structure(xml_content)
```

### Batch Processing
```python
from conversion_service import BatchConversionService

batch_service = BatchConversionService()
files = ["file1.xml", "file2.xml", "file3.xml"]
results = batch_service.convert_files(files)

for filepath, sql in results.items():
    print(f"{filepath}: {sql}")
```

## 🔌 Decoupling Benefits

1. **Separation of Concerns**
   - UI logic completely separated from conversion logic
   - Each module has single responsibility

2. **Testability**
   - Business logic can be tested independently
   - Mock GUI for testing conversion logic

3. **Extensibility**
   - Add new converters without modifying existing code
   - Add new parsers/generators without GUI changes

4. **Reusability**
   - Use conversion service in other applications
   - Import individual modules as needed

5. **Maintainability**
   - Clear, modular structure
   - Easy to locate and fix bugs
   - Simple to add new features

## 📋 Design Patterns Used

1. **Factory Pattern** - `ConverterFactory` for converter creation
2. **Strategy Pattern** - Different conversion strategies (converters)
3. **Singleton Pattern** - Global config instance
4. **Dependency Injection** - Service receives parser dependency
5. **Service Layer Pattern** - `ConversionService` orchestrates operations

## 🛠️ Configuration

Configuration file: `~/.xml_to_sql_config.json`

```json
{
  "converters": {
    "auto_detect": true,
    "default_converter": "GenericData"
  },
  "ui": {
    "font_size": 10
  },
  "output": {
    "format": "sql",
    "indent": 4
  }
}
```

## 📦 Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=.
```

## 🔮 Future Enhancements

1. Support for XSD schemas
2. YAML/JSON converter modes
3. Database direct output
4. SQL dialect selection (MySQL, PostgreSQL, etc.)
5. Advanced XML validation
6. Configuration UI wizard
7. Conversion history/templates
8. API server mode

## 📝 License

MIT License

## 👨‍💻 Author
Author : Bikram Banerjee
Email : [bikrambanerjee32@gmail.com]
XML to SQL Converter - Version 1.0
