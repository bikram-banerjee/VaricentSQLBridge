# XML to SQL Converter - Architecture Documentation

## Overview

This document describes the decoupled, modular architecture of the XML to SQL Converter application. The project follows SOLID principles and common design patterns to ensure maintainability, testability, and extensibility.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                         Application                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              GUI Layer (gui.py)                        │ │
│  │                                                        │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │    GUIController (MVC Controller)               │ │ │
│  │  │  - Window management                             │ │ │
│  │  │  - Widget creation and layout                    │ │ │
│  │  │  - Event handling                                │ │ │
│  │  │  - User interaction logic                        │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                      ▲                                 │ │
│  │                      │ uses                            │ │
│  │                      ▼                                 │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │ ConversionService (Business Logic Facade)       │ │ │
│  │  │  - Orchestrates conversions                      │ │ │
│  │  │  - Error handling                                │ │ │
│  │  │  - Service layer interface                       │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
                 ┌────────────┴────────────┐
                 │                         │
    ┌────────────▼──────────┐   ┌──────────▼─────────────┐
    │   Converters Layer    │   │  Parser Layer         │
    │  (converters.py)      │   │  (xml_parser.py)      │
    │                       │   │                       │
    │ ┌─────────────────┐   │   │ ┌─────────────────┐   │
    │ │ SQLConverter    │   │   │ │  XMLParser      │   │
    │ │ (Abstract)      │   │   │ │                 │   │
    │ └─────────────────┘   │   │ │ - Parse string  │   │
    │          ▲             │   │ │ - Parse file    │   │
    │          │ implements  │   │ │ - Extract data  │   │
    │ ┌─────────────────────┴───┬─│ │ - Analyze      │   │
    │ │         │               │ │ - Convert to   │   │
    │ ├─────────┴──────────┐    │ │   dict         │   │
    │ │                    │    │ └─────────────────┘   │
    │ ▼                    ▼    │                       │
    │ GenericData-        Query-│                       │
    │ Converter           Definition                    │
    │                    Converter                      │
    │                             │                       │
    │ ┌─────────────────────┐    │                       │
    │ │ ConverterFactory    │    │                       │
    │ │ - Get converter     │    │                       │
    │ │ - Auto-detect      │    │                       │
    │ │ - Register custom  │    │                       │
    │ └─────────────────────┘    │                       │
    └─────────────────────────────┴───────────────────────┘

Supporting Modules:
├── config.py        - Configuration management
├── utils.py         - Utility functions
└── main.py          - Application entry point
```

## Module Descriptions

### 1. **gui.py** - User Interface Layer

**Responsibility**: Presentation logic only

**Key Classes**:
- `GUIController`: Main GUI orchestrator
  - Manages window and widget creation
  - Handles user events
  - Delegates business logic to `ConversionService`

**Key Methods**:
- `create_widgets()`: Build UI components
- `do_convert()`: Event handler for conversion
- `do_copy()`, `do_paste()`: Clipboard operations
- `open_xml_file()`, `save_sql_file()`: File operations

**Design Principles**:
- No business logic in GUI
- Uses dependency injection (receives `ConversionService`)
- Separation of concerns: UI and logic are independent
- Event-driven architecture

**Example Usage**:
```python
from gui import main
main()  # Starts the application
```

### 2. **conversion_service.py** - Business Logic Facade

**Responsibility**: Orchestrate XML to SQL conversion

**Key Classes**:
- `ConversionService`: Main service
  - Parse XML
  - Auto-detect converter type
  - Execute conversion
  - Handle errors

- `BatchConversionService`: Batch processing
  - Process multiple files
  - Aggregate results

**Key Methods**:
- `convert_xml_string()`: Convert XML string
- `convert_xml_file()`: Convert XML file
- `get_xml_structure()`: Get XML preview
- `get_supported_converters()`: List available converters

**Design Pattern**: **Facade Pattern**
- Simplifies complex subsystem interactions
- Provides clean API for GUI and other clients

**Example Usage**:
```python
from conversion_service import ConversionService

service = ConversionService()
sql = service.convert_xml_string(xml_data)
```

### 3. **converters.py** - Conversion Strategies

**Responsibility**: Implement different XML to SQL conversion strategies

**Key Classes**:
- `SQLConverter` (Abstract Base Class)
  - Defines converter interface
  - Common utility methods

- `GenericDataConverter`
  - Converts generic data XML to INSERT statements
  - Assumes XML structure: `<root><record><field>value</field></record></root>`

- `QueryDefinitionConverter`
  - Converts query definition XML to SELECT statements
  - Supports SELECT, FROM, WHERE, JOIN, UNION, etc.

- `ConverterFactory`
  - Creates converters
  - Auto-detects appropriate converter type
  - Registers custom converters

**Design Patterns**:
- **Strategy Pattern**: Different conversion algorithms
- **Factory Pattern**: Converter creation and selection
- **Template Method**: Base converter class defines structure

**Extension Example**:
```python
from converters import SQLConverter, ConverterFactory

class CustomConverter(SQLConverter):
    def convert(self, xml_element):
        # Custom logic
        return sql_output

ConverterFactory.register_converter("Custom", CustomConverter)
```

### 4. **xml_parser.py** - XML Parsing and Analysis

**Responsibility**: Generic XML operations independent of conversion

**Key Classes**:
- `XMLParser`: XML parsing and manipulation
  - Parse XML strings and files
  - Namespace handling
  - Record extraction
  - Structure analysis

**Key Methods**:
- `parse_string()`: Parse XML from string
- `parse_file()`: Parse XML from file
- `extract_records()`: Extract data records
- `to_dict()`: Convert XML to dictionary
- `get_element_tree_structure()`: Get structure preview
- `strip_namespace()`: Remove XML namespaces

**Design Principles**:
- Single Responsibility: Only handles XML parsing
- Reusable: Can be used independently
- Error handling: Validates input

**Example Usage**:
```python
from xml_parser import XMLParser

parser = XMLParser()
root = parser.parse_file("data.xml")
records = parser.extract_records(root)
```

### 5. **config.py** - Configuration Management

**Responsibility**: Centralized configuration handling

**Key Classes**:
- `Config`: Configuration manager
  - Load/save configuration
  - Get/set values with dot notation
  - Default values

**Design Pattern**: **Singleton Pattern**
- `get_config()`: Get or create global instance

**Features**:
- Hierarchical configuration
- File persistence
- Default values

**Example Usage**:
```python
from config import get_config

config = get_config()
auto_detect = config.get("converters.auto_detect")
config.set("converters.default_converter", "QueryDefinition")
config.save()
```

### 6. **utils.py** - Utility Functions

**Responsibility**: General utility functions

**Key Classes**:
- `SQLFormatter`: SQL formatting and highlighting
- `XMLValidator`: XML validation
- `TextProcessor`: Text manipulation
- `Logger`: Simple logging

**Example Usage**:
```python
from utils import SQLFormatter, XMLValidator

sql = SQLFormatter.prettify(raw_sql)
is_valid = XMLValidator.is_valid_xml(xml_string)
```

### 7. **main.py** - Application Entry Point

**Responsibility**: Start the application

**Role**: Simple entry point that imports and runs GUI

```python
from gui import main

if __name__ == "__main__":
    main()
```

## Design Patterns Used

### 1. **Strategy Pattern** (converters.py)
- Different conversion strategies for different XML types
- Interchangeable algorithms
- Runtime selection

### 2. **Factory Pattern** (converters.py)
- `ConverterFactory` creates appropriate converters
- Auto-detection based on XML structure
- Extensible through registration

### 3. **Facade Pattern** (conversion_service.py)
- `ConversionService` simplifies complex operations
- Single point of access for GUI
- Hides converter selection logic

### 4. **Template Method Pattern** (converters.py)
- `SQLConverter` defines conversion template
- Subclasses implement specific logic
- Ensures consistent interface

### 5. **Singleton Pattern** (config.py)
- Global config instance
- Single source of truth for configuration
- Lazy initialization

### 6. **Dependency Injection** (gui.py)
- GUI receives `ConversionService` instance
- Loose coupling between components
- Easy to test and mock

### 7. **MVC Pattern** (gui.py)
- `GUIController` acts as controller
- Text widgets are views
- `ConversionService` acts as model

## Data Flow

### Typical Conversion Flow

```
User Input (GUI)
       ↓
    GUIController.do_convert()
       ↓
ConversionService.convert_xml_string()
       ↓
XMLParser.parse_string()
       ↓
ConverterFactory.detect_converter_type()
       ↓
Get appropriate Converter (Strategy)
       ↓
Converter.convert(xml_element)
       ↓
Generate SQL
       ↓
Display in GUI
       ↓
User sees result
```

## SOLID Principles Implementation

### Single Responsibility Principle
- Each module has one clear responsibility
- `xml_parser.py`: Parsing only
- `converters.py`: Conversion logic only
- `gui.py`: UI presentation only

### Open/Closed Principle
- Open for extension (custom converters)
- Closed for modification (base classes stable)
- Factory allows new converters without changing existing code

### Liskov Substitution Principle
- All converters implement `SQLConverter` interface
- Can be substituted transparently
- Consistent contract for all implementations

### Interface Segregation Principle
- Clients depend on specific interfaces
- GUI only needs `ConversionService` interface
- Not tied to implementation details

### Dependency Inversion Principle
- High-level modules depend on abstractions
- GUI depends on `ConversionService` interface
- Low-level modules implement abstractions
- Converters implement `SQLConverter` interface

## Error Handling Strategy

```
GUI Input
    ↓
Validation (XMLValidator)
    ↓
Parse XML (exception handling)
    ↓
Detect Converter (validation)
    ↓
Execute Conversion (try-catch)
    ↓
Return Result or Error Message
    ↓
Display to User
```

## Extensibility Examples

### Adding a New Converter

```python
from converters import SQLConverter, ConverterFactory

class YAMLConverter(SQLConverter):
    def convert(self, xml_element):
        # Convert to YAML-style SQL
        pass

ConverterFactory.register_converter("YAML", YAMLConverter)
```

### Adding a Custom Utility

```python
from utils import Logger

logger = Logger(level=Logger.DEBUG)
logger.debug("Debug message")
logger.info("Info message")
```

## Testing Strategy

### Unit Tests
- `test_xml_parser.py`: XML parsing functionality
- `test_converters.py`: Conversion logic
- `test_config.py`: Configuration management
- `test_utils.py`: Utility functions

### Integration Tests
- File I/O operations
- End-to-end conversion flows
- Error scenarios

### GUI Testing
- Manual testing (complex to automate)
- Event handling verification
- File dialog operations

## Performance Considerations

1. **Lazy Loading**: Converters created only when needed
2. **Efficient Parsing**: Uses ElementTree for memory efficiency
3. **Batch Processing**: Service for processing multiple files
4. **Caching**: Can cache parsed structures if needed

## Security Considerations

1. **Input Validation**: XML validation before processing
2. **SQL Injection Prevention**: Proper escaping of values
3. **File Access**: Safe file I/O with error handling
4. **Resource Limits**: Can be added for large files

## Future Enhancements

1. **API Server Mode**: REST API wrapper
2. **Database Direct Output**: Direct insertion to databases
3. **Schema Validation**: XSD schema support
4. **Performance Optimization**: Streaming for large files
5. **Advanced Logging**: Structured logging system
6. **Configuration UI**: Interactive configuration wizard
7. **Plugin System**: Dynamic module loading
8. **Multi-language Support**: i18n framework

## Conclusion

This modular, decoupled architecture provides:
- **Maintainability**: Clear separation of concerns
- **Testability**: Easy to unit test components
- **Extensibility**: Simple to add new converters
- **Reusability**: Components can be used independently
- **Scalability**: Foundation for future enhancements
