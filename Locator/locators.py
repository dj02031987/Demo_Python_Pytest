from selenium.webdriver.common.by import By


class Locators:
    ln_carreer = (By.XPATH, "//*[@href='/career/']")
    ln_lifeattenforce = (By.XPATH, "//*[@data-type='people']")
    ln_jobopenings = (By.XPATH, "//*[@data-type='job']")
    ls_article = (By.XPATH, "//*[@data-filter-type='people']//span")
    ln_agree_checkbox= (By.XPATH, "//button[text()='I Agree']")
