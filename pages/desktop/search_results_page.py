"""
Desktop Search Results Page Module

Page Object Model for desktop search results page with lot listing and navigation.
Handles verification of search results and navigation to individual lot details.
"""

import logging
import re
from pages.base_page import BasePage
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()


class SearchResultsPage(BasePage):
    """Page Object for Desktop Search Results."""

    LOT_ITEMS = "div[data-sentry-component='LotList']>div"
    RELATED_SEARCH_TERMS = ".RelatedSearchTerms_relatedSearchTerms__xDEW_>li"

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
            results_count = self.count("css", self.LOT_ITEMS)
            logger.info(f"✓ Total search results found: {results_count}")

            if results_count > 0:
                logger.info("✓ Search results loaded successfully")
                return True

            logger.warning("No search results found")
            return False

        except Exception as e:
            logger.error(f"✗ Failed while verifying search results. Error: {str(e)}")
            raise


    def get_related_search_terms(self) -> list:
        """
        Fetch related search terms displayed in UI.

        Returns:
            list: Related search terms shown on search results page
        """
        logger.info("Fetching related search terms from UI")
        try:
            
            related_terms_locator = self.page.locator("ul[class*='RelatedSearchTerms'] a")

            logger.info("→ Waiting for related search terms to be visible")
            related_terms_locator.first.wait_for(state="visible", timeout=10000)
            logger.info("✓ Related search terms elements are visible")

            logger.info("→ Extracting text from all related search terms")
            ui_terms = related_terms_locator.all_inner_texts() # Lists
            logger.info(f"✓ Retrieved {len(ui_terms)} related search terms: {ui_terms}")

            return ui_terms

        except Exception as e:
            logger.error(f"✗ Failed to fetch related search terms from UI. Error: {str(e)}")
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
       
        try:
            logger.info(f"→ Clicking lot item at index {index}")
            self.page.locator(self.LOT_ITEMS).nth(index).click()
            logger.info("✓ Lot item clicked successfully")

            logger.info(f"→ Verifying lot page URL: {self.page.url} contains '/l/'")
            self.wait_for_url(re.compile(r".*/l/.*"))
            logger.info("✓ Lot page opened and navigated successfully")

        except Exception as e:
            logger.error(f"✗ Failed to open lot item at index {index}. Error: {str(e)}")
            raise