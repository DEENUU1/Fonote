from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://open.spotify.com/episode/5C5K1SsR3nUhQlh8UZQyxd"


def get_driver() -> WebDriver:
    """
    Get a Chrome WebDriver instance.

    Returns:
        WebDriver: Chrome WebDriver instance.
    """
    return webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        )
    )


def scrape() -> None:
    driver = get_driver()

    driver.get(BASE_URL)
    driver.add_cookie({'name': 'sp_dc', 'value': 'AQBwO8eQN9t_5AQrKiRvh92rabQS9RAc3vU_2KWAsrccfmiHt4xXBacWRcWiOV-20NJIVNC6I3c64U_NILkMp5cMmWqF-tGCLKSX6_myGRhqcetV-bSBSHebtnVJgpX3wmIV25iI6SpwWEUeXtA5_QPrAR9LGnlM'})
    driver.add_cookie({'name': 'sp_key', 'value': '4edf59e3-ab29-4fea-ac6b-3050e04a5b97'})
    driver.add_cookie({'name': 'sp_landing', 'value': 'https%3A%2F%2Fopen.spotify.com%2F%3Fsp_cid%3D7835a571ce47dd4579cf0929be9a3062%26device%3Ddesktop'})
    driver.add_cookie({'name': 'sp_m', 'value': 'pl'})
    driver.add_cookie({'name': 'sp_t', 'value': '7835a571ce47dd4579cf0929be9a3062'})

    time.sleep(2)

    driver.get(BASE_URL)

    time.sleep(5)

    try:
        transcript_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.Link-sc-1g2blu2-0.dQcCmw.xTENSk0_RmQ8qEeEuhnE"))
        )
        transcript_button.click()
    except Exception as e:
        pass

    time.sleep(3)

    page = driver.page_source
    with open("spotify.html", "w", encoding="utf-8") as f:
        f.write(page)

    driver.quit()

scrape()

