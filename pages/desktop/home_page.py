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
        """
        #Waiting for the homepage to load and handling cookies popup can be common steps for all search tests, so we can include them in this method to ensure they are executed before performing the search action.
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
                logger.info("Cookies popup not displayed")

            logger.info(f"→ Entering keyword in search box: {keyword}")
            self.fill("css", self.SEARCH_BOX, keyword)

            logger.info("→ Clicking search magnifier button")
            self.click_nth("testid", self.MAGNIFIER_BUTTON, 0)

            logger.info(f"→ Current page URL: {self.page.url}")

            logger.info("→ Verifying search results page opened")
            self.wait_for_url(re.compile(r".*s\?q=train"))
            logger.info("✓ Search results page verification successful")

            logger.info("=" * 60)
            logger.info("✓ Desktop Search Completed Successfully and navigated to Search Results Page")
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

        logger.info("=" * 60)
        logger.info("Starting related search terms extraction from API")
        logger.info(f"→ Search keyword: '{keyword}'")
        logger.info("=" * 60)

        #ACCEPTING COOKIES
        try:
            logger.info("→ Checking for cookies popup")
            self.click("text", "Accept All")
            logger.info("✓ Cookies popup accepted")
        except Exception:
            logger.info("Cookies popup not displayed")

        with self.page.expect_response(
            lambda response:
                "related_terms" in response.url
                and response.status == 200
        ) as response_info:
            
            #Adding keyword in search box and clicking search button to trigger the API call for related search terms. This ensures that we are capturing the correct API response that corresponds to the search action performed in the test.
            logger.info("→ Filling search box for API request")
            self.fill("css", self.SEARCH_BOX, keyword)

            logger.info("→ Clicking search magnifier button")
            self.click_nth("testid", self.MAGNIFIER_BUTTON, 0)

        response = response_info.value
        logger.info(f"✓ API response received: {response.url}")
        logger.info(f"→ Response status: {response.status}")

        try:
            api_terms = response.json()["terms"]
            logger.info(f"✓ Extracted related search terms: {api_terms}")
        except Exception as e:
            logger.error(f"✗ Failed to parse related search terms from API response: {e}")
            raise

        logger.info("✓ Related search terms fetched successfully")
        logger.info("=" * 60)

        return api_terms