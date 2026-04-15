from selenium import webdriver
import pytest
import allure
from selenium.webdriver.chrome.options import Options
import os
from Utils.config import load_config

parent_dir = os.getcwd()
Project_dir = os.path.join(parent_dir, "Testcase")
screenshots_dirI = os.path.join(Project_dir, "Images")
DOWNLOAD_DIR = os.path.join(parent_dir, "Download")
PROJECT_PATH = os.path.join(parent_dir,"Testcases","Tenforce")
DATA_DIR = os.path.join(PROJECT_PATH, "Data")

def pytest_addoption(parser):
    parser.addoption("--P", action="store", default="QA", help="Env Setup")


@pytest.fixture(scope='session')
def config(request):
    env = request.config.getoption("--P")
    return load_config(env)


@pytest.fixture(scope='session')
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(50)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
