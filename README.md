# Catawiki Playwright Test Automation Suite

## Project Overview

This is a comprehensive end-to-end test automation framework for the Catawiki platform, built with **Playwright** and **Python**. The suite validates search functionality, go to search result page and click on the second element on the page and fetches current bid, title and favourites.

## Add ons

-Mobile emulation added on iPhone 13 device
-It checks API response for the search keyword 'train' and matches with Frontend display under 'Related Search Items'

- It supports Allure reporting, screenshots attached on failure



## What It Tests

### Core Functionality
- **Desktop Search**: Search items, verify results load, and navigate to lot details
- **Mobile Search**: Mobile-optimized search flow with responsive layout handling
- **Lot Details**: Extract and validate lot information (name, bid, favorites)
- **API Request/Response Capture**: Intercept network calls and validate response data
- **UI-API Consistency**: Verify that frontend elements match API response values
- **Related Search Terms**: Validate that suggested search terms in the UI match API response data

### Test Coverage
- Search with keywords (e.g., "train")
- Special character searches (e.g., "##@@")
- Related search term validation
- Multi-lot navigation
- Data extraction and assertion

## Project Structure

```
assessment_catawiki_playwright/
├── conftest.py                 # Pytest fixtures and browser setup
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── Makefile                    # Build and test commands
├── configs/
│   └── config.yaml            # Test configuration (URLs, timeouts)
├── pages/                      # Page Object Models
│   ├── base_page.py           # Base page class with common methods
│   ├── desktop/
│   │   ├── home_page.py       # Desktop search page
│   │   ├── search_results_page.py  # Desktop results page
│   │   └── lot_page.py        # Desktop lot details page
│   └── mobile/
│       ├── mobile_home_page.py
│       ├── mobile_search_result_page.py
│       └── mobile_lot_page.py
├── tests/                      # Test files
│   ├── test_search_lot.py     # Desktop search tests
│   └── test_mobile_search.py  # Mobile search tests
├── utils/                      # Utilities
│   ├── config_reader.py       # YAML config loader
│   └── loggers.py             # Custom logging setup
├── logs/                       # Test execution logs
├── traces/                     # Playwright trace files
└── reports/                    # Allure test reports
```

## Key Features

### 1. **Page Object Model (POM)**
- Organized page structure with reusable locators and methods
- Separation of test logic and page interactions
- Easier maintenance and scalability

### 2. **Network Interception**
- Capture HTTP requests and responses using Playwright's `expect_request()` and `expect_response()`
- Validate API response bodies match frontend displays
- Extract and compare related search terms between API and UI

### 3. **Comprehensive Logging**
- Centralized logger with file and console output
- Structured logging with status indicators (✓, ✗, →)
- Separate log files per execution date

### 4. **Allure Reporting**
- Rich test reports with steps and attachments
- Failure analysis and trend tracking
- Visual HTML reports with interactive features

### 5. **Configuration Management**
- YAML-based configuration for dynamic test parameters
- Supports multiple environments

### 6. **Cross-Platform Testing**
- Desktop browser automation
- Mobile viewport testing
- Responsive design validation

## Setup Instructions

### Prerequisites
- Python 3.10+
- Playwright browsers installed

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd assessment_catawiki_playwright
   ```

2. **Create a virtual environment** (if not already created)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v -s
```

### Run Specific Test File
```bash
pytest tests/test_search_lot.py -v -s
```

### Run Specific Test
```bash
pytest tests/test_search_lot.py::test_capture_search_request_for_train -v -s
```

### Run with Allure Reports
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run Desktop Tests Only
```bash
pytest tests/test_search_lot.py -v -s
```

### Run Mobile Tests Only
```bash
pytest tests/test_mobile_search.py -v -s
```

## Test Execution Examples

### Test 1: Desktop Search Flow
```python
test_search_and_fetch_lot_details
```
- Searches for "train"
- Verifies results load
- Opens the second lot
- Extracts lot details (name, bid, favorites)
- Validates data is not empty

### Test 2: API Request/Response Capture
```python
test_capture_search_request_for_train
```
- Captures the search request URL with query parameters
- Intercepts and validates the API response status (200)
- Extracts related search terms from the API response
- Compares API terms with UI-displayed related search terms
- Validates consistency between frontend and backend data

### Test 3: Mobile Search Flow
```python
test_mobile_search_flow
```
- Performs search on mobile viewport
- Verifies mobile-specific layout
- Validates lot details on mobile

## Configuration

Edit `configs/config.yaml` to customize:
- Base URL
- Browser type (chromium, firefox, webkit)
- Timeout values
- Mobile device settings
- Headless mode

Example:
```yaml
base_url: "https://www.catawiki.com"
timeout: 30000
headless: true
viewport:
  width: 1280
  height: 720
```

## Logging

Logs are automatically generated in the `logs/` directory with timestamps:
- `log_YYYY-MM-DD.txt` - Daily log files
- Console output with color-coded status indicators
- Comprehensive error messages and stack traces

## Reports

### Allure Reports
After test execution, generate and view reports:
```bash
allure generate --clean -o allure-report allure-results
allure open allure-report
```

### Traces and Screenshots
- Playwright traces saved in `traces/` directory
- Screenshots captured on failures
- Detailed execution history

## Dependencies

Key packages used:
- **playwright**: Browser automation
- **pytest**: Testing framework
- **allure-pytest**: Test reporting
- **pyyaml**: Configuration management

See `requirements.txt` for complete list.

## Common Issues & Solutions

### Issue: Tests fail with "Element not found"
**Solution**: Check page load time and adjust timeout in `config.yaml` or use `wait_for_visible()` before interaction.

### Issue: Trace files grow too large
**Solution**: Clear `traces/` directory periodically and adjust trace recording settings.

### Issue: Mobile tests fail on desktop viewport
**Solution**: Ensure fixtures in `conftest.py` are using correct device context.

## Development Guidelines

### Adding New Tests
1. Create test file in `tests/` directory
2. Use page objects from `pages/` directory
3. Follow naming convention: `test_*.py`
4. Use `@allure.feature()` and `@allure.story()` decorators

### Adding New Page Objects
1. Create class inheriting from `BasePage`
2. Define locators as class constants
3. Implement methods for page interactions
4. Use centralized logger for consistency

### Best Practices
- Use descriptive test names
- Keep tests focused on single functionality
- Leverage page objects to avoid code duplication
- Add meaningful assertions with clear error messages
- Use Allure steps to structure test flow

## Useful Commands

```bash
# Run tests with headless mode disabled (see browser)
pytest tests/ -v -s --headed

# Run tests with specific marker
pytest tests/ -m "smoke" -v

# Run tests and generate coverage report
pytest tests/ --cov=pages --cov-report=html

# Lint Python code
pylint pages/ tests/ utils/

# Format code
black pages/ tests/ utils/
```

## Contributing

When contributing:
1. Follow PEP 8 style guidelines
2. Add docstrings to new methods
3. Use type hints where applicable
4. Update tests for new features
5. Document changes in README

## Support

For issues or questions, review:
- Test logs in `logs/` directory
- Allure reports for failure details
- Playwright traces for visual debugging

---

**Last Updated**: May 7, 2026  
**Framework**: Playwright + Pytest  
**Target Platform**: Catawiki.com
