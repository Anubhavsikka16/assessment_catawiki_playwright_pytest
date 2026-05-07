"""
Catawiki Playwright Base Page Module

Provides core page object model functionality with locator resolution,
element interactions, and assertion utilities for Playwright automation.
"""

import logging
from playwright.sync_api import Page, expect
from utils.loggers import Logger

log = Logger(__name__, logging.INFO).get_logger()


class BasePage:
    """Base Page Object Model class for Playwright test automation."""

    def __init__(self, page: Page):
        """Initialize BasePage with Playwright page instance."""
        self.page = page

    # ============================================================================
    # LOCATOR RESOLUTION
    # ============================================================================

    def _get_locator(self, locator_type: str, locator_value: str, **kwargs):
        """
        Resolve element locator by type and value.

        Args:
            locator_type: Type of locator (css, xpath, text, role, etc.)
            locator_value: Value for the locator
            **kwargs: Additional arguments for specific locator types

        Returns:
            Playwright Locator object
        """
        log.info(f"Resolving locator | Type: {locator_type} | Value: {locator_value}")

        if locator_type == "css":
            return self.page.locator(locator_value)
        elif locator_type == "xpath":
            return self.page.locator(f"xpath={locator_value}")
        elif locator_type == "text":
            return self.page.get_by_text(locator_value)
        elif locator_type == "role":
            return self.page.get_by_role(locator_value, **kwargs)
        elif locator_type == "label":
            return self.page.get_by_label(locator_value)
        elif locator_type == "placeholder":
            return self.page.get_by_placeholder(locator_value)
        elif locator_type == "testid":
            return self.page.get_by_test_id(locator_value)
        elif locator_type == "alt_text":
            return self.page.get_by_alt_text(locator_value)
        elif locator_type == "title":
            return self.page.get_by_title(locator_value)
        else:
            log.error(f"Unsupported locator type: {locator_type}")
            raise ValueError(f"Unsupported locator type: {locator_type}")

    # ============================================================================
    # GENERIC ACTIONS
    # ============================================================================

    def click(self, locator_type: str, locator_value: str, **kwargs) -> None:
        """Click on an element."""
        log.info(f"Clicking element | {locator_type}: {locator_value}")
        try:
            self._get_locator(locator_type, locator_value, **kwargs).click()
            log.info("✓ Click successful")
        except Exception as e:
            log.error(f"✗ Failed to click element. Error: {str(e)}")
            raise

    def fill(self, locator_type: str, locator_value: str, value: str, **kwargs) -> None:
        """Fill input element with value."""
        log.info(f"Filling element | {locator_type}: {locator_value} | Value: {value}")
        try:
            self._get_locator(locator_type, locator_value, **kwargs).fill(value)
            log.info("✓ Fill successful")
        except Exception as e:
            log.error(f"✗ Failed to fill element. Error: {str(e)}")
            raise

    def type(self, locator_type: str, locator_value: str, value: str, **kwargs) -> None:
        """Type text into element."""
        log.info(f"Typing into element | {locator_type}: {locator_value}")
        try:
            self._get_locator(locator_type, locator_value, **kwargs).type(value)
            log.info("✓ Typing successful")
        except Exception as e:
            log.error(f"✗ Failed typing action. Error: {str(e)}")
            raise

    def get_text(self, locator_type: str, locator_value: str, **kwargs) -> str:
        """Get text content from element."""
        log.info(f"Getting text from element | {locator_type}: {locator_value}")
        try:
            text = self._get_locator(locator_type, locator_value, **kwargs).inner_text()
            log.info(f"✓ Retrieved text: {text}")
            return text
        except Exception as e:
            log.error(f"✗ Failed to get text. Error: {str(e)}")
            raise

    def get_all_texts(self, locator_type: str, locator_value: str, **kwargs) -> list:
        """Get all text values from multiple elements."""
        log.info(f"Getting all texts | {locator_type}: {locator_value}")
        try:
            texts = self._get_locator(locator_type, locator_value, **kwargs).all_inner_texts()
            log.info(f"✓ Retrieved {len(texts)} text values")
            return texts
        except Exception as e:
            log.error(f"✗ Failed to get all texts. Error: {str(e)}")
            raise

    def is_visible(self, locator_type: str, locator_value: str, **kwargs) -> bool:
        """Check if element is visible."""
        log.info(f"Checking visibility | {locator_type}: {locator_value}")
        try:
            visible = self._get_locator(locator_type, locator_value, **kwargs).is_visible()
            log.info(f"✓ Visibility status: {visible}")
            return visible
        except Exception as e:
            log.error(f"✗ Visibility check failed. Error: {str(e)}")
            raise

    def count(self, locator_type: str, locator_value: str, **kwargs) -> int:
        """Count elements matching locator."""
        log.info(f"Counting elements | {locator_value}")
        try:
            count = self._get_locator(locator_type, locator_value, **kwargs).count()
            log.info(f"✓ Element count: {count}")
            return count
        except Exception as e:
            log.error(f"✗ Count failed. Error: {str(e)}")
            raise

    def hover(self, locator_type: str, locator_value: str, **kwargs) -> None:
        """Hover over element."""
        log.info(f"Hovering over element | {locator_value}")
        try:
            self._get_locator(locator_type, locator_value, **kwargs).hover()
            log.info("✓ Hover successful")
        except Exception as e:
            log.error(f"✗ Hover failed. Error: {str(e)}")
            raise

    def press(self, locator_type: str, locator_value: str, key: str, **kwargs) -> None:
        """Press key on element."""
        log.info(f"Pressing key '{key}' on | {locator_value}")
        try:
            self._get_locator(locator_type, locator_value, **kwargs).press(key)
            log.info("✓ Key press successful")
        except Exception as e:
            log.error(f"✗ Key press failed. Error: {str(e)}")
            raise

    # ============================================================================
    # WAITS & ASSERTIONS
    # ============================================================================

    def wait_for_visible(self, locator_type: str, locator_value: str, **kwargs) -> None:
        """Wait for element to be visible."""
        log.info(f"Waiting for visibility | {locator_value}")
        try:
            expect(self._get_locator(locator_type, locator_value, **kwargs)).to_be_visible()
            log.info("✓ Element is visible")
        except Exception as e:
            log.error(f"✗ Visibility wait failed. Error: {str(e)}")
            raise

    def wait_for_text(self, locator_type: str, locator_value: str, text: str, **kwargs) -> None:
        """Wait for element to contain specific text."""
        log.info(f"Waiting for text '{text}' | {locator_value}")
        try:
            expect(self._get_locator(locator_type, locator_value, **kwargs)).to_have_text(text)
            log.info("✓ Text verification successful")
        except Exception as e:
            log.error(f"✗ Text verification failed. Error: {str(e)}")
            raise

    def wait_for_url(self, url: str) -> None:
        """Wait for page URL to match."""
        log.info(f"Waiting for URL: {url}")
        try:
            expect(self.page).to_have_url(url)
            log.info("✓ URL verification successful")
        except Exception as e:
            log.error(f"✗ URL verification failed. Error: {str(e)}")
            raise

    def is_title_contains(self, text: str) -> bool:
        """Check if page title contains text."""
        title = self.page.title()
        log.info(f"Checking title contains '{text}'")
        result = text in title
        log.info(f"✓ Title verification result: {result}")
        return result

    # ============================================================================
    # ADVANCED UTILITIES
    # ============================================================================

    def click_nth(self, locator_type: str, locator_value: str, index: int, **kwargs) -> None:
        """Click on the nth element."""
        log.info(f"Clicking nth({index}) element | {locator_value}")
        try:
            self._get_locator(locator_type, locator_value, **kwargs).nth(index).click()
            log.info("✓ Nth click successful")
        except Exception as e:
            log.error(f"✗ Nth click failed. Error: {str(e)}")
            raise

    def get_nth_text(self, locator_type: str, locator_value: str, index: int, **kwargs) -> str:
        """Get text from the nth element."""
        log.info(f"Getting text from nth({index}) element | {locator_value}")
        try:
            text = self._get_locator(locator_type, locator_value, **kwargs).nth(index).inner_text()
            log.info(f"✓ Nth text retrieved: {text}")
            return text
        except Exception as e:
            log.error(f"✗ Failed to get nth text. Error: {str(e)}")
            raise

    def scroll_into_view(self, locator_type: str, locator_value: str, **kwargs) -> None:
        """Scroll element into view."""
        log.info(f"Scrolling into view | {locator_value}")
        try:
            self._get_locator(locator_type, locator_value, **kwargs).scroll_into_view_if_needed()
            log.info("✓ Scroll successful")
        except Exception as e:
            log.error(f"✗ Scroll failed. Error: {str(e)}")
            raise

    def wait_for_load(self) -> None:
        """Wait for page to reach networkidle state."""
        log.info("Waiting for page load state: networkidle")
        try:
            self.page.wait_for_load_state("networkidle")
            log.info("✓ Page fully loaded")
        except Exception as e:
            log.error(f"✗ Page load wait failed. Error: {str(e)}")
            raise