from pages.base_page import BasePage

class LotPage(BasePage):

    LOT_NAME = "[class='tw:text-h3 tw:mb-xl LotTitle_title__rXYHd']"
    FAVORITES = "div[data-sentry-component='LotDetailsFavoriteButton'] [title='favourite']"
    CURRENT_BID = "div[data-testid='lot-bid-status-section'] div[data-sentry-source-file='BidStatusSectionBidAmount.tsx']"

    def get_lot_details(self):
        return {
            "name": self.get_text("css", self.LOT_NAME),
            "favorites": self.get_text("css", self.FAVORITES),
            "bid": self.get_text("css", self.CURRENT_BID)
        }