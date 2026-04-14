from Locator.locators import Locators as lc


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def launch_url(self, url):
        self.driver.get(url)

    def get_title(self):
        actual_title = self.driver.title
        return actual_title
