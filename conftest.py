"""
Pytest Configuration and Fixtures

Centralized configuration for Playwright browser setup and test fixtures.
Provides both desktop and mobile browser contexts with tracing enabled.
"""

import logging
import os
import re
import allure
import pytest

from datetime import datetime
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
# CREATE REQUIRED DIRECTORIES
# ============================================================================

os.makedirs("screenshots", exist_ok=True)
os.makedirs("traces", exist_ok=True)
os.makedirs("videos/desktop", exist_ok=True)
os.makedirs("videos/mobile", exist_ok=True)

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
# PYTEST HOOK FOR TEST STATUS
# ============================================================================


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result status.
    Required for screenshot-on-failure handling.
    """

    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)


# ============================================================================
# HELPER METHOD
# ============================================================================


def generate_test_filename(test_name: str) -> str:
    """
    Generate safe filename using test name + timestamp.
    """

    safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', test_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{safe_name}_{timestamp}"


# ============================================================================
# DESKTOP PAGE FIXTURE
# ============================================================================


@pytest.fixture
def page(browser, request):
    """
    Create desktop browser context and page.

    Features:
    - Video recording
    - Tracing enabled
    - Screenshot on failure
    - Allure attachments
    """

    logger.info("→ Creating desktop browser context")

    context = browser.new_context(
        record_video_dir="videos/desktop"
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    page = context.new_page()

    logger.info("→ Opening Catawiki homepage (Desktop)")

    page.goto("https://www.catawiki.com/en/")

    yield page

    # =========================================================================
    # GENERATE COMMON FILE NAME
    # =========================================================================

    filename = generate_test_filename(request.node.name)

    # =========================================================================
    # SCREENSHOT ON FAILURE
    # =========================================================================

    if request.node.rep_call.failed:

        logger.error("✗ Test failed - capturing screenshot")

        screenshot_path = f"screenshots/{filename}.png"

        page.screenshot(
            path=screenshot_path,
            full_page=True
        )

        allure.attach.file(
            screenshot_path,
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

    # =========================================================================
    # SAVE TRACE
    # =========================================================================

    trace_path = f"traces/{filename}.zip"

    context.tracing.stop(path=trace_path)

    allure.attach.file(
        trace_path,
        name="Desktop Trace",
        attachment_type=allure.attachment_type.ZIP
    )

    # =========================================================================
    # CLOSE CONTEXT FIRST TO SAVE VIDEO
    # =========================================================================

    context.close()

    # =========================================================================
    # ATTACH VIDEO
    # =========================================================================

    try:

        video_path = page.video.path()

        allure.attach.file(
            video_path,
            name="Execution Video",
            attachment_type=allure.attachment_type.WEBM
        )

        logger.info(f"✓ Video attached: {video_path}")

    except Exception as e:

        logger.warning(f"Unable to attach video: {e}")

    logger.info("✓ Desktop context closed")


# ============================================================================
# MOBILE PAGE FIXTURE
# ============================================================================


@pytest.fixture
def mobile_page(browser, request):
    """
    Create mobile browser context and page with iPhone 13 emulation.

    Features:
    - Mobile emulation
    - Video recording
    - Tracing enabled
    - Screenshot on failure
    - Allure attachments
    """

    logger.info("→ Creating mobile browser context (iPhone 13)")

    context = browser.new_context(
        **IPHONE_13,
        record_video_dir="videos/mobile"
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    page = context.new_page()

    logger.info("→ Opening Catawiki homepage (Mobile)")

    page.goto("https://www.catawiki.com/en/")

    yield page

    # =========================================================================
    # GENERATE COMMON FILE NAME
    # =========================================================================

    filename = generate_test_filename(request.node.name)

    # =========================================================================
    # SCREENSHOT ON FAILURE
    # =========================================================================

    if request.node.rep_call.failed:

        logger.error("✗ Mobile test failed - capturing screenshot")

        screenshot_path = f"screenshots/{filename}.png"

        page.screenshot(
            path=screenshot_path,
            full_page=True
        )

        allure.attach.file(
            screenshot_path,
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

    # =========================================================================
    # SAVE TRACE
    # =========================================================================

    trace_path = f"traces/{filename}.zip"

    context.tracing.stop(path=trace_path)

    allure.attach.file(
        trace_path,
        name="Mobile Trace",
        attachment_type=allure.attachment_type.ZIP
    )

    # =========================================================================
    # CLOSE CONTEXT FIRST TO SAVE VIDEO
    # =========================================================================

    context.close()

    # =========================================================================
    # ATTACH VIDEO
    # =========================================================================

    try:

        video_path = page.video.path()

        allure.attach.file(
            video_path,
            name="Execution Video",
            attachment_type=allure.attachment_type.WEBM
        )

        logger.info(f"✓ Video attached: {video_path}")

    except Exception as e:

        logger.warning(f"Unable to attach video: {e}")

    logger.info("✓ Mobile context closed")