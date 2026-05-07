"""
Mobile Search Results Page Module

Page Object Model for mobile search results page with lot listing and navigation.
Handles verification of search results and navigation to individual lot details.
"""

import logging
import re
from pages.base_page import BasePage
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()


class SearchResultsPage(BasePage):
    """Page Object for Mobile Search Results."""

    LOT_ITEMS = "div[data-sentry-component='LotList']>div"

    # ============================================================================
    # RESULTS VERIFICATION
    # ============================================================================

    def is_results_loaded(self) -> bool:
        """
        Verify if search results are loaded on the page.

        Returns:
            bool: True if results are loaded, False otherwise
        """
        logger.info("Verifying search results are loaded")
        try:
            #logger.info("→ Checking if search result items are loaded")
            results_count = self.count("css", self.LOT_ITEMS)
            logger.info(f"✓ Total search results found: {results_count}")

            if results_count > 0:
                logger.info("✓ Search results loaded successfully")
                return True

            logger.warning("⚠ No search results found")
            return False

        except Exception as e:
            logger.error(f"✗ Failed while verifying search results. Error: {str(e)}")
            raise

    # ============================================================================
    # LOT NAVIGATION
    # ============================================================================

    def click_lot_by_index(self, index: int) -> None:
        """
        Click on a lot item by its index position.

        Args:
            index: Index of the lot item to click (0-based)

        Raises:
            Exception: If lot item cannot be clicked or lot page doesn't load
        """
        logger.info(f"Opening lot item at index: {index}")
        try:
            logger.info(f"→ Clicking lot item at index {index}")
            self.page.locator(self.LOT_ITEMS).nth(index).click()
            logger.info("✓ Lot item clicked successfully")

            logger.info(f"→ Verifying lot page URL: {self.page.url}")
            self.wait_for_url(re.compile(r".*/l/.*"))
            logger.info("✓ Lot page opened and navigated successfully")

        except Exception as e:
            logger.error(f"✗ Failed to open lot item at index {index}. Error: {str(e)}")
            raise