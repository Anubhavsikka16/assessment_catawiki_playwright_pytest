"""
Desktop Home Page Module

Page Object Model for desktop home page with search functionality.
Handles desktop search flow including cookie acceptance and search submission.
"""

import logging
import re
from pages.base_page import BasePage
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()


class HomePage(BasePage):
    """Page Object for Desktop Home Page."""

    SEARCH_BOX = "input[data-testid='search-field'][id='field_r_2_']"
    MAGNIFIER_BUTTON = "text-field-prefix"

    # ============================================================================
    # SEARCH FUNCTIONALITY
    # ============================================================================

    def search_item(self, keyword: str) -> None:
        """
        Execute desktop search flow for a given keyword.

        Handles:
        - Homepage load verification
        - Cookie acceptance popup
        - Search input with keyword
        - Search button click
        - Results page navigation

        Args:
            keyword: Search term to query

        Raises:
            Exception: If search flow fails at any step
        """
        logger.info("=" * 60)
        logger.info("Starting Desktop Search Flow")
        logger.info("=" * 60)

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
                logger.info("⚠ Cookies popup not displayed")

            logger.info(f"→ Entering keyword in search box: {keyword}")
            self.fill("css", self.SEARCH_BOX, keyword)

            logger.info("→ Clicking search magnifier button")
            self.click_nth("testid", self.MAGNIFIER_BUTTON, 0)

            logger.info(f"→ Current page URL: {self.page.url}")

            logger.info("→ Verifying search results page opened")
            self.wait_for_url(re.compile(r".*s\?q=train"))
            logger.info("✓ Search results page verification successful")

            logger.info("=" * 60)
            logger.info("✓ Desktop Search Completed Successfully")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"✗ Search flow failed for keyword '{keyword}'. Error: {str(e)}")
            logger.info("=" * 60)
            raise

    def get_related_search_terms_from_api(self,keyword: str) -> list:
        """
        Fetch related search terms from API response.

        Args:
        keyword: Search keyword

        Returns:
        list: Related search terms returned by API
        """


        try:
            self.click("text", "Accept All")

        except Exception:
            pass

        with self.page.expect_response(
            lambda response:
            "related_terms" in response.url
            and response.status == 200
        ) as response_info:

            self.fill("css", self.SEARCH_BOX, keyword)

            logger.info("→ Clicking search magnifier button")

            self.click_nth( "testid",self.MAGNIFIER_BUTTON,0)

        response = response_info.value

        api_terms = response.json()["terms"]

        logger.info(f"API Terms: {api_terms}")

        return api_terms