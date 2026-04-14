from Locator.locators import Locators as lc
from Utils.global_driver_utility import GlobalLocator as gl

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def launch_url(self, url):
        gl(self.driver).launch_url(url)

    def get_title(self):
        actual_title = gl(self.driver).get_title()
        return actual_title

    def click_On_I_agree_checkbox(self):
        gl(self.driver).click(*lc.ln_agree_checkbox)
