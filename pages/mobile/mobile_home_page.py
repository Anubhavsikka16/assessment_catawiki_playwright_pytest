"""
Mobile Home Page Module

Page Object Model for mobile home page with search functionality.
Handles mobile search flow including cookie acceptance and search submission.
"""

import logging
import re
from pages.base_page import BasePage
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()


class MobileHomePage(BasePage):
    """Page Object for Mobile Home Page."""

    SEARCH_ICON = "div[class*='mobile-nav'] button"  # Mobile search icon
    SEARCH_BOX = "input[data-testid='search-field']:visible"  # Visible search field only

    # ============================================================================
    # SEARCH FUNCTIONALITY
    # ============================================================================

    def search_item(self, keyword: str) -> None:
        """
        Execute mobile search flow for a given keyword.

        Handles:
        - Homepage load verification
        - Cookie acceptance popup
        - Mobile search icon click
        - Search input and submission
        - Results page navigation

        Args:
            keyword: Search term to query

        Raises:
            Exception: If search flow fails at any step
        """
        
        try:
            logger.info("→ Waiting for homepage to load")
            self.page.wait_for_load_state("domcontentloaded")
            logger.info("✓ Homepage loaded successfully")

            # Handle cookies popup
            logger.info("→ Checking for cookies popup")
            try:
                self.click("text", "Accept All")
                logger.info("✓ Cookies popup accepted")
            except Exception:
                logger.info("⚠ Cookies popup not present")

            # Wait for React mobile hydration
            self.page.wait_for_timeout(3000)

            logger.info("→ Locating mobile search icon")
            search_buttons = self.page.locator(self.SEARCH_ICON)
            logger.info(f"✓ Search buttons found: {search_buttons.count()}")

            # Use last visible button
            search_button = search_buttons.last
            search_button.wait_for(state="visible", timeout=10000)

            logger.info("→ Clicking mobile search icon")
            search_button.click(force=True)

            # Wait for mobile drawer animation
            self.page.wait_for_timeout(2000)

            logger.info(f"→ Entering keyword: {keyword}")

            # Mobile creates a NEW visible search input
            search_input = self.page.locator(self.SEARCH_BOX).last
            search_input.wait_for(state="visible", timeout=15000)
            search_input.click(force=True)
            search_input.fill(keyword)

            logger.info("→ Pressing Enter to submit search")
            search_input.press("Enter")

            logger.info("→ Waiting for results page")
            self.wait_for_url(re.compile(r".*s\?q=.*"))

            logger.info("=" * 60)
            logger.info("✓ Mobile Search Completed Successfully")
            logger.info("=" * 60)

        except Exception as e:
            self.page.screenshot(path="mobile_search_failure.png", full_page=True)
            logger.error(f"✗ Mobile search failed. Error: {str(e)}")
            logger.info("=" * 60)
            raise