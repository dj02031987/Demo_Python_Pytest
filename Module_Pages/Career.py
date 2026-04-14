from Locator.locators import Locators as lc
from Utils.global_driver_utility import GlobalLocator as gl

class Career:
    def __init__(self, driver):
        self.driver = driver

    def click_on_career_link(self):
        gl(self.driver).click(*lc.ln_carreer)

    def scroll_down_to_element(self, *args):
        gl(self.driver).scroll_by_visibility_of_element(*args)

    def click_on_LifeatTenforcesession(self):
        gl(self.driver).click(*lc.ln_lifeattenforce)

    def select_article(self, article_name):
        element = gl(self.driver).element_list(*lc.ls_article)
        for i in element:
            if i.text == article_name:
                i.click()
                break

    def click_on_Jobopenings(self):
        gl(self.driver).click(*lc.ln_jobopenings)

    def validation_of_Jobopenings(self):
        return gl(self.driver).is_element_displayed(*lc.ln_jobopenings, timeout=5)
