"""
Desktop Lot Page Module

Page Object Model for desktop lot details page.
Handles extraction of lot information including name, favorites, and current bid.
"""

import logging
from pages.base_page import BasePage
from utils.loggers import Logger

logger = Logger(__name__, logging.INFO).get_logger()


class LotPage(BasePage):
    """Page Object for Desktop Lot Details Page."""

    LOT_NAME = "[class='tw:text-h3 tw:mb-xl LotTitle_title__rXYHd']"
    FAVORITES = "div[data-sentry-component='LotDetailsFavoriteButton'] [title='favourite']"
    CURRENT_BID = "div[data-testid='lot-bid-status-section'] div[data-sentry-source-file='BidStatusSectionBidAmount.tsx']"

    # ============================================================================
    # LOT DETAILS EXTRACTION
    # ============================================================================

    def get_lot_details(self) -> dict:
        """
        Extract lot details from desktop lot page.

        Retrieves:
        - Lot name
        - Favorites count
        - Current bid amount

        Returns:
            dict: Dictionary containing lot details with keys: name, favorites, bid

        Raises:
            Exception: If any lot detail cannot be fetched
        """
        logger.info("=" * 60)
        logger.info("Fetching Lot Details")
        logger.info("=" * 60)

        try:
            logger.info("→ Extracting lot name")
            lot_name = self.get_text("css", self.LOT_NAME)
            logger.info(f"✓ Lot name: {lot_name}")

            logger.info("→ Extracting favorites count")
            favorites = self.get_text("css", self.FAVORITES)
            logger.info(f"✓ Favorites: {favorites}")

            logger.info("→ Extracting current bid amount")
            current_bid = self.get_text("css", self.CURRENT_BID)
            logger.info(f"✓ Current bid: {current_bid}")

            logger.info("=" * 60)
            logger.info("✓ Lot Details Fetched Successfully")
            logger.info("=" * 60)

            print("\n" + "=" * 60)
            print("LOT DETAILS")
            print("=" * 60)
            print(f"Name:      {lot_name}")
            print(f"Favorites: {favorites}")
            print(f"Bid:       {current_bid}")
            print("=" * 60 + "\n")
            #for assertions or reuse
            return {"name": lot_name, "favorites": favorites, "bid": current_bid}

        except Exception as e:
            logger.error(f"✗ Failed to fetch lot details. Error: {str(e)}")
            raise