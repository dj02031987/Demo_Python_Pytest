from selenium.webdriver.common.by import By


class Locators:
    ### Carreer Page Locator #####
    ln_carreer = (By.XPATH, "//*[@href='/career/']")
    ln_lifeattenforce = (By.XPATH, "//*[@data-type='people']")
    ln_jobopenings = (By.XPATH, "//*[@data-type='job']")
    ls_article = (By.XPATH, "//*[@data-filter-type='people']//span")
