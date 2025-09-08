# Contributing to Google Calendar Time Finder

Thank you for your interest in contributing to Google Calendar Time Finder! We welcome contributions from the community and are grateful for any help you can provide.

## 🎯 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- **Clear description** of the bug
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Log output** or error messages (if applicable)

### Suggesting Features

We love feature suggestions! Please create an issue with:

- **Clear description** of the feature
- **Use case** or problem it solves
- **Possible implementation** approach (if you have ideas)

### Contributing Code

1. **Fork** the repository
2. **Create a branch** for your feature (`git checkout -b feature/amazing-feature`)
3. **Make your changes** following our coding standards
4. **Add tests** for your changes
5. **Run the test suite** to ensure everything works
6. **Commit your changes** with a clear commit message
7. **Push** to your branch (`git push origin feature/amazing-feature`)
8. **Create a Pull Request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Google Calendar API credentials
- Git

### Local Setup

```bash
# Clone your fork
git clone https://github.com/your-username/gcal-pal.git
cd gcal-pal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If you create this file

# Set up pre-commit hooks (optional but recommended)
pre-commit install
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=gcal_pal

# Run specific test file
python -m pytest tests/test_specific.py
```

## 📝 Coding Standards

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused on a single task

### Example Function

```python
def find_available_slots(start_date: datetime, end_date: datetime, 
                        min_duration: int = 60) -> List[Tuple[datetime, datetime]]:
    """
    Find available time slots within a date range.
    
    Args:
        start_date: Start of the search range
        end_date: End of the search range
        min_duration: Minimum slot duration in minutes
        
    Returns:
        List of (start_time, end_time) tuples for available slots
        
    Raises:
        ValueError: If start_date is after end_date
    """
    # Implementation here
    pass
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for recurring events
fix: handle timezone conversion edge case
docs: update installation instructions
test: add tests for color filtering
refactor: simplify busy time calculation
```

### Testing

- Write tests for all new functionality
- Ensure tests cover edge cases
- Use descriptive test names
- Mock external API calls in tests

```python
def test_finds_available_slots_with_no_conflicts():
    """Test that available slots are found when no events conflict."""
    # Test implementation
    pass

def test_respects_working_hours_boundaries():
    """Test that slots don't extend beyond working hours."""
    # Test implementation
    pass
```

## 🔍 Code Review Process

### For Contributors

- Ensure your PR has a clear description
- Link to any related issues
- Include screenshots for UI changes
- Be responsive to feedback
- Keep PRs focused and reasonably sized

### Review Criteria

We look for:

- **Functionality**: Does it work as expected?
- **Code Quality**: Is it readable and maintainable?
- **Tests**: Are there adequate tests?
- **Documentation**: Is it properly documented?
- **Performance**: Does it maintain good performance?

## 🚀 Release Process

1. Version bumping follows [Semantic Versioning](https://semver.org/)
2. Update CHANGELOG.md with new features and fixes
3. Create a release PR
4. Tag the release after merging

## 💬 Getting Help

- **Questions?** Open a [discussion](https://github.com/your-username/gcal-pal/discussions)
- **Stuck?** Ask in the issue comments
- **Need guidance?** Email us at support@nurelm.com

## 📋 Issue Labels

We use these labels to organize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to docs
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

## 🎉 Recognition

Contributors will be:

- Added to the contributor list in README
- Mentioned in release notes
- Given credit in commit messages

Thank you for contributing! 🙏

---

**Happy coding!**  
The NuRelm Team

