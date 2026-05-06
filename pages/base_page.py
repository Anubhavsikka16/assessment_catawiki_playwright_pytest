from playwright.sync_api import Page, expect
import logging
from utils.loggers import Logger
log = Logger(__name__, logging.INFO)

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
    

    # 🔥 Core locator resolver (THIS is the brain)
    def _get_locator(self, locator_type, locator_value, **kwargs):

        if locator_type == "css":
            return self.page.locator(locator_value)

        elif locator_type == "xpath":
            return self.page.locator(f"xpath={locator_value}")

        elif locator_type == "text":
            return self.page.get_by_text(locator_value)

        elif locator_type == "role":
            return self.page.get_by_role(locator_value, **kwargs)

        elif locator_type == "label":
            return self.page.get_by_label(locator_value)

        elif locator_type == "placeholder":
            return self.page.get_by_placeholder(locator_value)

        elif locator_type == "testid":
            return self.page.get_by_test_id(locator_value)

        elif locator_type == "alt_text":
            return self.page.get_by_alt_text(locator_value)

        elif locator_type == "title":
            return self.page.get_by_title(locator_value)

        else:
            raise ValueError(f"Unsupported locator type: {locator_type}")

    # ========================
    # 🔹 GENERIC ACTIONS
    # ========================

    def click(self, locator_type, locator_value, **kwargs):
        self._get_locator(locator_type, locator_value, **kwargs).click()

    def fill(self, locator_type, locator_value, value, **kwargs):
        self._get_locator(locator_type, locator_value, **kwargs).fill(value)

    def type(self, locator_type, locator_value, value, **kwargs):
        self._get_locator(locator_type, locator_value, **kwargs).type(value)

    def get_text(self, locator_type, locator_value, **kwargs):
        return self._get_locator(locator_type, locator_value, **kwargs).inner_text()

    def get_all_texts(self, locator_type, locator_value, **kwargs):
        return self._get_locator(locator_type, locator_value, **kwargs).all_inner_texts()

    def is_visible(self, locator_type, locator_value, **kwargs):
        return self._get_locator(locator_type, locator_value, **kwargs).is_visible()

    def count(self, locator_type, locator_value, **kwargs):
        return self._get_locator(locator_type, locator_value, **kwargs).count()

    def hover(self, locator_type, locator_value, **kwargs):
        self._get_locator(locator_type, locator_value, **kwargs).hover()

    def press(self, locator_type, locator_value, key, **kwargs):
        self._get_locator(locator_type, locator_value, **kwargs).press(key)

    # ========================
    # 🔹 WAITS & ASSERTIONS
    # ========================

    def wait_for_visible(self, locator_type, locator_value, **kwargs):
        expect(self._get_locator(locator_type, locator_value, **kwargs)).to_be_visible()

    def wait_for_text(self, locator_type, locator_value, text, **kwargs):
        expect(self._get_locator(locator_type, locator_value, **kwargs)).to_have_text(text)

    def wait_for_url(self, url):
        expect(self.page).to_have_url(url)
        
    def is_title_contains(self, text):
        return text in self.page.title()

    # ========================
    # 🔹 ADVANCED UTILITIES
    # ========================

    def click_nth(self, locator_type, locator_value, index, **kwargs):
        self._get_locator(locator_type, locator_value, **kwargs).nth(index).click()

    def get_nth_text(self, locator_type, locator_value, index, **kwargs):
        return self._get_locator(locator_type, locator_value, **kwargs).nth(index).inner_text()

    def scroll_into_view(self, locator_type, locator_value, **kwargs):
        self._get_locator(locator_type, locator_value, **kwargs).scroll_into_view_if_needed()

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")