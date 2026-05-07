"""
Mobile Search Test Module

Comprehensive test suite for mobile search functionality including:
- Search item execution
- Results verification
- Lot details extraction
- Multi-assertion validation
"""

import logging
import allure
from pages.mobile.mobile_home_page import MobileHomePage
from pages.mobile.mobile_search_result_page import SearchResultsPage
from pages.mobile.mobile_lot_page import LotPage
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()


@allure.feature("Mobile")
@allure.story("Mobile search functionality")
def test_mobile_search_flow(mobile_page) -> None:
    """
    Test mobile search flow from search to lot details retrieval.

    Verifies:
    - Mobile search functionality
    - Results loaded correctly
    - Lot details can be fetched
    - Data validation and assertions

    Args:
        mobile_page: Pytest fixture providing Playwright page instance
    """
    logger.info("=" * 60)
    logger.info("TEST STARTED | Mobile Search Flow")
    logger.info("=" * 60)

    # Initialize page objects
    home = MobileHomePage(mobile_page)
    results = SearchResultsPage(mobile_page)
    lot = LotPage(mobile_page)

    try:
        # ========================================================================
        # STEP 1: SEARCH FLOW
        # ========================================================================

        with allure.step("Search item on mobile"):
            #logger.info("→ Searching for 'train' on mobile device")
            home.search_item("train")
            #logger.info("✓ Mobile search completed successfully")

        # ========================================================================
        # STEP 2: VERIFY SEARCH RESULTS
        # ========================================================================

        with allure.step("Verify results loaded on mobile"):
            logger.info("→ Verifying mobile search results are loaded")
            assert results.is_results_loaded(), "Mobile search results failed to load"
            logger.info("✓ Mobile search results verified successfully")

        # ========================================================================
        # STEP 3: OPEN SECOND LOT
        # ========================================================================

        with allure.step("Open second lot from results"):
            logger.info("→ Clicking on second lot from search results")
            results.click_lot_by_index(1)
            logger.info("✓ Second lot opened successfully")

        # ========================================================================
        # STEP 4: FETCH LOT DETAILS
        # ========================================================================

        with allure.step("Fetch and validate lot details"):
            logger.info("→ Extracting lot details")
            details = lot.get_lot_details()
            logger.info("✓ Lot details fetched successfully")

        # ========================================================================
        # STEP 5: DATA VALIDATION
        # ========================================================================

        with allure.step("Validate lot details"):
            logger.info("→ Performing data validations")
            assert details["name"] != "", "Lot name is empty"
            assert details["bid"] != "", "Current bid is empty"
            logger.info("✓ All assertions passed successfully")

        logger.info("=" * 60)
        logger.info("✓ TEST PASSED | Mobile Search Flow")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"✗ TEST FAILED | Error: {str(e)}")
        logger.info("=" * 60)
        raise