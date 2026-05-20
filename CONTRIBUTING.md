# Contributing to XML to SQL Converter

Thank you for your interest in contributing to the XML to SQL Converter project! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and professional
- Welcome diverse perspectives
- Focus on constructive feedback
- Report issues responsibly

## Getting Started

### Prerequisites
- Python 3.7+
- Git
- Virtual environment (venv)

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd XML_to_SQL_Converter

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov pylint black flake8
```

## Architecture Overview

Please familiarize yourself with [ARCHITECTURE.md](ARCHITECTURE.md) before contributing. Key principles:

- **Decoupled Design**: Each module has a single responsibility
- **Design Patterns**: Factory, Strategy, Facade, Template Method, Singleton
- **SOLID Principles**: Code should follow SOLID guidelines
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Testing**: All new features must include tests

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Keep functions small and focused
- Update docstrings

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Lint code
pylint *.py

# Format code
black *.py

# Check style
flake8 *.py
```

### 4. Commit Changes

```bash
git add .
git commit -m "Brief description of changes"
```

Use clear, descriptive commit messages:
- `fix: Correct XML parsing issue`
- `feat: Add new converter type`
- `docs: Update README`
- `refactor: Improve error handling`

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to related issues
- Test results screenshot (if applicable)

## Adding New Features

### Adding a New Converter

1. **Extend `SQLConverter`**:
   ```python
   from converters import SQLConverter
   import xml.etree.ElementTree as ET
   
   class MyConverter(SQLConverter):
       def convert(self, xml_element: ET.Element) -> str:
           # Implementation
           return sql_output
   ```

2. **Register with Factory**:
   ```python
   from converters import ConverterFactory
   ConverterFactory.register_converter("MyConverter", MyConverter)
   ```

3. **Add Tests**:
   ```python
   # tests/test_my_converter.py
   import unittest
   from converters import MyConverter
   
   class TestMyConverter(unittest.TestCase):
       def test_conversion(self):
           # Test implementation
           pass
   ```

### Adding a New Module

1. Create new file following naming convention
2. Include module docstring
3. Follow existing patterns
4. Add comprehensive docstrings
5. Create unit tests
6. Update imports in `__init__.py` if needed

## Code Style Guidelines

### PEP 8 Compliance

```python
# Good
def process_xml_data(xml_string: str) -> str:
    """Process XML data and return SQL."""
    if not xml_string:
        raise ValueError("Empty XML string")
    
    return generate_sql(xml_string)

# Bad
def process_xml_data(xmlString):
    if xmlString=="":
        raise ValueError("Empty")
    return generateSql(xmlString)
```

### Naming Conventions

- `Classes`: `PascalCase` (e.g., `SQLConverter`)
- `Functions`: `snake_case` (e.g., `convert_xml`)
- `Constants`: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_INDENT`)
- `Private`: Prefix with `_` (e.g., `_internal_method`)

### Docstring Format

```python
def convert(self, xml_element: ET.Element) -> str:
    """
    Convert XML element to SQL statement.
    
    Args:
        xml_element: Root XML element to convert
        
    Returns:
        Generated SQL statement(s)
        
    Raises:
        ValueError: If XML structure is invalid
        
    Example:
        >>> converter = MyConverter()
        >>> xml = ET.fromstring("<data></data>")
        >>> sql = converter.convert(xml)
    """
```

### Type Hints

Use type hints for all functions:

```python
def process(data: str, count: int = 10) -> List[str]:
    """Process data and return results."""
    pass
```

## Testing Guidelines

### Test Structure

```python
import unittest
from module import FunctionOrClass

class TestFunctionOrClass(unittest.TestCase):
    """Test cases for FunctionOrClass."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.instance = FunctionOrClass()
    
    def test_valid_input(self):
        """Test with valid input."""
        result = self.instance.method()
        self.assertEqual(result, expected)
    
    def test_invalid_input(self):
        """Test with invalid input."""
        with self.assertRaises(ValueError):
            self.instance.method(invalid_arg)
    
    def tearDown(self):
        """Clean up after tests."""
        pass
```

### Test Coverage Requirements

- Minimum 80% code coverage
- All public methods tested
- Edge cases covered
- Error conditions tested

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_converters.py

# Run specific test
pytest tests/test_converters.py::TestConverterFactory::test_factory_get_converter

# Run with coverage report
pytest --cov=. --cov-report=html
```

## Documentation Guidelines

### README.md

- Keep it concise and helpful
- Include quick start guide
- Add examples
- Link to detailed docs

### Docstrings

- Every module should have module-level docstring
- Every class should have class-level docstring
- Every public method should have method docstring
- Document parameters, returns, and exceptions

### Comments

- Use sparingly - code should be self-documenting
- Explain "why", not "what"
- Update comments when updating code

```python
# Good: Explains why
# Use list comprehension for performance (3x faster than loop)
result = [process(item) for item in items]

# Bad: States obvious
# Loop through items
for item in items:
    process(item)
```

## Performance Considerations

When contributing code:
- Consider memory usage for large files
- Profile code for bottlenecks
- Avoid unnecessary loops
- Use appropriate data structures

## Security Considerations

- Validate all user input
- Sanitize SQL values to prevent injection
- Handle files safely
- Protect sensitive information

## Reporting Issues

### Before Reporting

- Check existing issues
- Search documentation
- Try reproducing with latest version

### Issue Template

```
**Description**
Clear description of the issue

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- Python version: 3.x
- OS: Windows/Mac/Linux
- Dependencies: (output of `pip list`)
```

## Pull Request Process

1. Update documentation as needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG if applicable
5. Get code reviewed
6. Merge after approval

## Review Checklist

When reviewing code:
- [ ] Follows code style guidelines
- [ ] Includes tests
- [ ] Documentation updated
- [ ] No breaking changes (without discussion)
- [ ] Performance acceptable
- [ ] Error handling adequate
- [ ] Security considerations addressed

## Questions?

- Check [ARCHITECTURE.md](ARCHITECTURE.md) for design overview
- Review existing code for patterns
- Open an issue to discuss
- Ask in pull request comments

## License

By contributing, you agree that your contributions will be licensed under the project's license.

## Acknowledgments

Thank you for contributing to make this project better!
