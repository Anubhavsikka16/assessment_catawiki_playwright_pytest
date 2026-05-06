PYTEST := pytest
TEST_DIR := tests/

ALLURE_RESULTS := reports/allure-results
ALLURE_REPORT := reports/allure-report

SCREENSHOTS := screenshots
TRACES := traces
LOGS := logs

.PHONY: test parallel headed report clean run

# =========================
# Clean old artifacts
# =========================
clean:
	@echo "Cleaning old reports..."
	@rm -rf $(ALLURE_RESULTS)
	@rm -rf $(ALLURE_REPORT)
	@rm -rf $(SCREENSHOTS)
	@rm -rf $(TRACES)
	@rm -rf $(LOGS)

# =========================
# Run tests
# =========================
test:
	@echo "Running Pytest tests..."
	@$(PYTEST) -v -s --capture=no --tb=short $(TEST_DIR) --alluredir=$(ALLURE_RESULTS)

# =========================
# Run tests in parallel
# =========================
parallel:
	@echo "Running tests in parallel..."
	@$(PYTEST) -n auto -v -s --capture=no --tb=short $(TEST_DIR) --alluredir=$(ALLURE_RESULTS)

# =========================
# Run tests in headed mode
# =========================
headed:
	@echo "Running tests in headed mode..."
	@HEADLESS=false $(PYTEST) -v -s --tb=short $(TEST_DIR) --alluredir=$(ALLURE_RESULTS)

# =========================
# Generate + Open Allure Report
# =========================
report:
	@echo "Generating Allure report..."
	@allure generate $(ALLURE_RESULTS) -o $(ALLURE_REPORT) --clean

	@echo "Opening Allure report..."
	@allure open $(ALLURE_REPORT)

# =========================
# Show traces folder
# =========================
traces:
	@echo "Available traces:"
	@ls -la $(TRACES) || echo "No traces found"

# =========================
# Full execution flow
# Always generate report
# even if tests fail
# =========================
run:
	@make clean
	-@make testß
	@make traces
	@make report