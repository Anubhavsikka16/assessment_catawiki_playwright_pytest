import os
import pytest
import allure

from playwright.sync_api import sync_playwright
from utils.config_reader import config


# =========================
# Create required folders
# =========================
os.makedirs("reports/screenshots", exist_ok=True)
os.makedirs("traces", exist_ok=True)


# =========================
# Hook: Capture screenshots
# and DOM on failure
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    # Store test result for later use
    setattr(item, "rep_" + rep.when, rep)

    # Capture only test execution failures
    if rep.when == "call" and rep.failed:

        page = item.funcargs.get("page", None)

        if page:

            screenshot_path = (
                f"reports/screenshots/{item.name}.png"
            )

            # Screenshot
            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # DOM Snapshot
            html = page.content()

            allure.attach(
                html,
                name="DOM Snapshot",
                attachment_type=allure.attachment_type.HTML
            )


# =========================
# Cross-browser fixture
# =========================
@pytest.fixture(params=config["browsers"])
def browser_type(request):
    return request.param


# =========================
# Main Playwright fixture
# =========================
@pytest.fixture(scope="function")
def page(request, browser_type):

    with sync_playwright() as p:

        # Launch browser dynamically
        browser = getattr(p, browser_type).launch(
            headless=config["headless"]
        )

        test_name = request.node.name

        # Create isolated browser context
        context = browser.new_context()

        # =========================
        # Start Playwright tracing
        # =========================
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        # Create page
        page = context.new_page()

        # Default timeout
        page.set_default_timeout(config["timeout"])

        # Navigate to application
        page.goto(config["base_url"])

        yield page

        # =========================
        # Save trace after execution
        # =========================
        trace_path = f"traces/{test_name}.zip"

        context.tracing.stop(path=trace_path)

        # Cleanup
        context.close()
        browser.close()