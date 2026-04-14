from Locator.locators import Locators as lc


class Career:
    def __init__(self, driver):
        self.driver = driver

    def click_on_career_link(self):
        self.driver.find_element(*lc.ln_carreer).click()

    def scroll_down_to_element(self,*args):
        element = self.driver.find_element(args)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_on_LifeatTenforcesession(self):
        self.driver.find_element().click(*lc.ln_lifeattenforce)

    def select_article(self, article_name):
        element = self.driver.find_elements(*lc.ls_article)
        for i in element:
            if i.text == article_name:
                i.click()
                break

    def click_on_Jobopenings(self):
        self.driver.find_element().click(*lc.ln_jobopenings)

    def validation_of_Jobopenings(self):
        element = self.driver.find_element(*lc.ln_jobopenings)
        return element.is_displayed()
