import time
import pyperclip
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from conftest import DATA_DIR
import os
import zxing


class GlobalLocator:
    maps = {}

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 18)

    def wait_for_visibility_of_ele(self, ele, timeout=None):
        self.wait = WebDriverWait(self.driver, timeout or 18)
        return self.wait.until(ec.visibility_of_element_located(ele))

    def wait_for_clickable_of_ele(self, ele):
        return self.wait.until(ec.element_to_be_clickable(ele))

    def invisibility_of_ele(self, ele, timeout=None):
        self.wait = WebDriverWait(self.driver, timeout or 18)
        return self.wait.until(ec.invisibility_of_element_located(ele))

    def wait_for_presence_of_ele(self, ele):
        return self.wait.until(ec.presence_of_element_located(ele))

    def wait_for_all_visibility_of_ele(self, ele):
        return self.wait.until(ec.visibility_of_all_elements_located(ele))

    def wait_until_text_present_in_attribute(self, *ele, attribute, expected_text):
        return self.wait.until(ec.text_to_be_present_in_element_attribute(ele, attribute, expected_text))

    def launch_url(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def send_key(self, *args, value):
        self.wait_for_visibility_of_ele(args).clear()
        self.wait_for_visibility_of_ele(args).send_keys(value)

    def click(self, *args):
        try:
            self.wait_for_visibility_of_ele(args)
            self.wait_for_clickable_of_ele(args).click()
        except ElementClickInterceptedException:
            element = self.wait_for_visibility_of_ele(args)
            self.driver.execute_script("arguments[0].click();", element)

    def gettext(self, *args, timeout=None):
        return self.wait_for_visibility_of_ele(args, timeout= timeout).text

    def clear(self, *args):
        self.wait_for_visibility_of_ele(args).clear()

    def element_list(self, *args):
        listofelement = self.driver.find_elements(*args)
        return listofelement

    def element_list_value(self, *args):
        listofelement_value = []
        listofelement = self.wait_for_all_visibility_of_ele(args)
        for value in listofelement:
            listofelement_value.append(value.text)
        return listofelement_value

    def enterkey(self, *args):
        self.wait_for_visibility_of_ele(args).send_keys(Keys.ENTER)

    def mouse_rightKey(self, *args):
        self.wait_for_visibility_of_ele(args).send_keys(Keys.ENTER)

    def get_window_handles_map(self):
        set_of_handles = self.driver.window_handles
        print("Window handles:", set_of_handles)

        if len(set_of_handles) < 2:
            raise ValueError(
                "Not enough window handles found. Expected at least 2, but found {}".format(len(set_of_handles)))

        iterator = iter(set_of_handles)
        pID = next(iterator)
        cID = next(iterator)

        maps = {
            "parentID": pID,
            "childID": cID
        }

        return maps

    def get_window_handles(self):
        set_of_handles = self.driver.window_handles
        for handle in set_of_handles:
            self.driver.switch_to.window(handle)

    def selectByIndex(self, *args, index):
        sel = Select(self.driver.find_element(*args))
        sel.select_by_index(index)

    def selectByValue(self, *args, value):
        sel = Select(self.driver.find_element(*args))
        sel.select_by_value(value)

    def selectByText(self, *args, text):
        sel = Select(self.driver.find_element(*args))
        sel.select_by_visible_text(text)

    def selectByOption(self, *args, path, option):
        sel = Select(self.driver.find_element(*args))
        plist = sel.options
        for x in plist:
            op = str(x.text)
            if op.__contains__(option):
                x.click()

    def scroll_by_visibility_of_element(self, *args):
        js = self.driver.execute_script
        js("arguments[0].scrollIntoView();", self.wait_for_visibility_of_ele(args))

    def scrollToTop(self):
        self.driver.execute_script(self.driver, script="window.scrollTo(document.body.scrollHeight, 0);")

    def alertCancel(self):
        alt = Alert(self.driver)
        alt.accept()

    def attachFile(self, *args, filepath):
        self.driver.find_element(*args).send_keys(filepath)

    def is_element_displayed(self, *args, timeout=None):
        try:
            element = self.wait_for_visibility_of_ele(args, timeout=timeout)
            return element.is_displayed()
        except TimeoutException:
            return False

    def is_element_enabled(self, *args):
        try:
            element = self.wait_for_visibility_of_ele(args)
            return element.is_enabled()
        except Exception:
            return False

    def is_element_disable(self, *args):
        try:
            element = self.wait_for_visibility_of_ele(args)
            return not element.is_enabled()
        except Exception:
            return False

    def is_element_not_displayed(self, *args, timeout=None):
        try:
            return self.invisibility_of_ele(args, timeout=timeout)
        except TimeoutException:
            return False

    def get_attribute(self, *args, attribute):
        return self.wait_for_visibility_of_ele(args).get_attribute(attribute)


    def mouse_over(self, *args):
        actions = ActionChains(self.driver)
        element = self.driver.find_element(*args)
        actions.move_to_element(element).perform()

    def get_current_url(self):
        return self.driver.current_url

    def get_percentage_value(self, percentage, total):
        return round((percentage / 100) * total, 6)


    def select_value_by_text(self, *args, custom_text):
        elements = self.wait_for_all_visibility_of_ele(args)

        for element in elements:
            if element.text.strip() == custom_text:
                element.click()
                return element

        return None

    def verify_text_from_the_elements(self, *args, custom_text):
        elements = self.wait_for_all_visibility_of_ele(args)

        for element in elements:
            if element.text.strip() == custom_text.strip():
                return element.text

        return None

    def verify_first_element_text_until_match(self, *args, custom_text, timeout=480, poll_frequency=1):
        end_time = time.time() + timeout

        while time.time() < end_time:
            elements = self.wait_for_all_visibility_of_ele(args)
            if elements:
                try:
                    first_element_text = elements[0].text.strip()
                    if first_element_text == custom_text.strip():
                        return first_element_text
                except Exception:
                    pass

            time.sleep(poll_frequency)

        return None
