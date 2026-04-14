from Module_Pages.Launch_url import HomePage as hp
from Module_Pages.Career import Career as cp
from Locator.locators import Locators as lc
import pytest


class Test_CareePage:

    def test_launch_url(self, driver, config):
        hp(driver).launch_url(config["url"])
        title = hp(driver).get_title()
        assert title == config["title"]

    def test_career_page(self, driver, config):
        cp(driver).scroll_down_to_element(*lc.ln_carreer)
        cp(driver).click_on_career_link()
        cp(driver).select_article(config['article_name'])
        cp(driver).click_on_Jobopenings()
        assert cp(driver).validation_of_Jobopenings == True
