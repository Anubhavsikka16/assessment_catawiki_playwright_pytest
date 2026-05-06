PYTEST := pytest
TEST_DIR := tests/

ALLURE_RESULTS := reports/allure-results
SCREENSHOTS := screenshots
TRACES := traces

.PHONY: test parallel headed report clean run

# =========================
# Clean old artifacts
# =========================
clean:
	@echo "Cleaning old reports..."
	@rm -rf $(ALLURE_RESULTS)
	@rm -rf allure-report
	@rm -rf $(SCREENSHOTS)
	@rm -rf $(TRACES)

# =========================
# Run tests
# =========================
test:
	@echo "Running Pytest tests..."
	@$(PYTEST) $(TEST_DIR) --alluredir=$(ALLURE_RESULTS)

# =========================
# Run tests in parallel
# =========================
parallel:
	@echo "Running tests in parallel..."
	@$(PYTEST) -n auto $(TEST_DIR) --alluredir=$(ALLURE_RESULTS)

# =========================
# Run tests in headed mode
# =========================
headed:
	@echo "Running tests in headed mode..."
	@HEADLESS=false $(PYTEST) $(TEST_DIR) --alluredir=$(ALLURE_RESULTS)

# =========================
# Open Allure report
# =========================
report:
	@echo "Opening Allure report..."
	@allure serve $(ALLURE_RESULTS)

# =========================
# Full execution flow
# Clean -> Run -> Report
# =========================
run:
	@make clean
	-@make test
	@make report