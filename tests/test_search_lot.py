from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.lot_page import LotPage
import allure

@allure.feature("Search")
@allure.story("Search and open lot")
def test_search_and_fetch_lot_details(page):

    home = HomePage(page)
    results = SearchResultsPage(page)
    lot = LotPage(page)

    # No navigation needed 🚀
    with allure.step("Search for train"):
        home.search_item("train")
    with allure.step("Verify search results loaded"):
        assert results.is_results_loaded()


    with allure.step("Open second lot"):
        results.click_lot_by_index(1)
    with allure.step("Fetch lot details"):
        details = lot.get_lot_details()

    print("\nLot Details:", details)

    assert details["name"] != ""
    assert details["bid"] != ""