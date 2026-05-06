from pages.base_page import BasePage
import time
class SearchResultsPage(BasePage):

    LOT_ITEMS = "div[data-sentry-component='LotList']>div"
    #Getting lots count to verify if results are loaded
    def is_results_loaded(self):
        print("Checking if search results are loaded...", self.count("css", self.LOT_ITEMS))
        return self.count("css", self.LOT_ITEMS) > 0

    def click_lot_by_index(self, index):
        self.page.locator(self.LOT_ITEMS).nth(index).click()
        time.sleep(2)
        #Fetching URL of the clicked lot page to verify navigation
        print("Title OF THE CLICKED LOTS PAGE IS: ", self.page.title())
        self.is_title_contains("h0-149742-model-train-passenger-carriage")