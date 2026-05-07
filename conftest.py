"""
Pytest Configuration and Fixtures

Centralized configuration for Playwright browser setup and test fixtures.
Provides both desktop and mobile browser contexts with tracing enabled.
"""

import logging
import os
import allure
import pytest
from playwright.sync_api import sync_playwright
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()

# ============================================================================
# MOBILE DEVICE CONFIGURATION
# ============================================================================

IPHONE_13 = {
    "viewport": {"width": 390, "height": 844},
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 "
        "Mobile/15E148 Safari/604.1"
    ),
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
}

# ============================================================================
# PLAYWRIGHT SESSION FIXTURE
# ============================================================================


@pytest.fixture(scope="session")
def playwright():
    """Initialize Playwright session."""
    logger.info("✓ Starting Playwright session")
    with sync_playwright() as p:
        yield p
    logger.info("✓ Stopping Playwright session")


# ============================================================================
# BROWSER SESSION FIXTURE
# ============================================================================


@pytest.fixture(scope="session")
def browser(playwright):
    """Launch Chromium browser for the session."""
    logger.info("✓ Launching Chromium browser")
    browser = playwright.chromium.launch(headless=False)
    yield browser
    logger.info("✓ Closing Chromium browser")
    browser.close()


# ============================================================================
# DESKTOP PAGE FIXTURE
# ============================================================================


@pytest.fixture
def page(browser):
    """
    Create desktop browser context and page.

    Features:
    - Tracing enabled for debugging
    - Screenshots and snapshots captured
    - Trace saved to traces/desktop_trace.zip
    - Attached to Allure report

    Yields:
        Page: Playwright page object for desktop
    """
    logger.info("→ Creating desktop browser context")
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    logger.info("→ Opening Catawiki homepage (Desktop)")
    page.goto("https://www.catawiki.com/en/")

    yield page

    logger.info("→ Closing desktop context and saving trace")
    os.makedirs("traces", exist_ok=True)
    trace_path = "traces/desktop_trace.zip"
    context.tracing.stop(path=trace_path)

    allure.attach.file(
        trace_path,
        name="Desktop Trace",
        attachment_type=allure.attachment_type.ZIP
    )
    context.close()
    logger.info("✓ Desktop context closed")


# ============================================================================
# MOBILE PAGE FIXTURE
# ============================================================================


@pytest.fixture
def mobile_page(browser):
    """
    Create mobile browser context and page with iPhone 13 emulation.

    Features:
    - iPhone 13 device emulation
    - Tracing enabled for debugging
    - Screenshots and snapshots captured
    - Trace saved to traces/mobile_trace.zip
    - Attached to Allure report

    Yields:
        Page: Playwright page object for mobile
    """
    logger.info("→ Creating mobile browser context (iPhone 13)")
    context = browser.new_context(**IPHONE_13)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    logger.info("→ Opening Catawiki homepage (Mobile)")
    page.goto("https://www.catawiki.com/en/")

    yield page

    logger.info("→ Closing mobile context and saving trace")
    os.makedirs("traces", exist_ok=True)
    trace_path = "traces/mobile_trace.zip"
    context.tracing.stop(path=trace_path)

    allure.attach.file(
        trace_path,
        name="Mobile Trace",
        attachment_type=allure.attachment_type.ZIP
    )
    context.close()
    logger.info("✓ Mobile context closed")