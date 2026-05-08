"""
Desktop Search and Lot Details Test Module

Comprehensive test suite for desktop search functionality including:
- Search item execution
- Results verification
- Lot details extraction
- Multi-assertion validation
"""
import logging
import allure
from pages.desktop.home_page import HomePage
from pages.desktop.search_results_page import SearchResultsPage
from pages.desktop.lot_page import LotPage
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()


@allure.feature("Search")
@allure.story("Search and open lot")
def test_search_and_fetch_lot_details(page) -> None:
    """
    Test desktop search flow from search to lot details retrieval.

    Verifies:
    - Desktop search functionality
    - Results loaded correctly
    - Lot details can be fetched
    - Data validation and assertions

    Args:
        page: Pytest fixture providing Playwright page instance
    """
    logger.info("=" * 60)
    logger.info("TEST STARTED | Desktop Search Flow")
    logger.info("=" * 60)

    # Initialize page objects
    home = HomePage(page)
    results = SearchResultsPage(page)
    lot = LotPage(page)

    try:
        # ========================================================================
        # STEP 1: SEARCH FLOW
        # ========================================================================

        with allure.step("Search for train"):
            #logger.info("→ Searching for keyword: train")
            home.search_item("train")
            #logger.info("✓ Search operation completed successfully")

        # ========================================================================
        # STEP 2: VERIFY SEARCH RESULTS
        # ========================================================================

        with allure.step("Verify search results loaded"):
            assert results.is_results_loaded(), "Search results failed to load"
            logger.info("✓ Search results verification successful")

        # ========================================================================
        # STEP 3: OPEN SECOND LOT
        # ========================================================================

        with allure.step("Open second lot"):
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
        logger.info("✓ TEST PASSED | Desktop Search Flow")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"✗ TEST FAILED | Error: {str(e)}")
        logger.info("=" * 60)
        raise


@allure.feature("Search")
@allure.story("Validate related search terms API and UI consistency")
def test_related_search_terms_match_ui(page):
    
    logger.info("=" * 60)
    logger.info("TEST STARTED | Backend API and UI consistency for related search terms")
    logger.info("=" * 60)


    home = HomePage(page)
    results = SearchResultsPage(page)

    api_terms = home.get_related_search_terms_from_api(
        "train"
    )

    ui_terms = results.get_related_search_terms()
    logger.info(f"→ Validating API terms match UI terms i.e. {api_terms} == {ui_terms}")
    assert api_terms == ui_terms