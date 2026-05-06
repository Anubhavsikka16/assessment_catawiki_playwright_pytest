from pages.base_page import BasePage
import time
import re
class HomePage(BasePage):
    
    SEARCH_BOX = "input[data-testid= 'search-field'][id='field_r_2_']"
    MAGNIFIER_BUTTON = "text-field-prefix"  
     

    def search_item(self, keyword):
        #accepting cookies if popup appears
        try: 
            self.click("text", "Accept All")
        except:
            pass
        self.fill("css", self.SEARCH_BOX, keyword)
        self.click_nth("testid", self.MAGNIFIER_BUTTON, 0)
        time.sleep(2)
        print("URL OF THE PAGE IS: ", self.page.url)
        self.wait_for_url(re.compile(r"s\?q=train"))
        