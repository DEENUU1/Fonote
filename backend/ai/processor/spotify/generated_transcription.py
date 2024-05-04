import logging
import time
from typing import Optional

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from ai.processor.audio.fragment import Fragment
from ai.processor.audio.fragment_list import FragmentList

logger = logging.getLogger(__name__)


class SpotifyGeneratedTranscription:
    def __init__(self, url: str):
        self.url = url
        self.driver = self.get_driver()

    @staticmethod
    def get_driver():
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def click_transcription_button(self) -> bool:
        try:
            transcript_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.Link-sc-1g2blu2-0.dQcCmw.xTENSk0_RmQ8qEeEuhnE"))
            )
            transcript_button.click()
            return True

        except Exception as e:
            logger.error(e)

        return False

    @staticmethod
    def convert_time_to_seconds(time_str: str) -> float:
        """
        Converts time in format 'mm:ss' or 'hh:mm:ss' to seconds.
        """
        parts = time_str.split(':')
        if len(parts) == 3:  # 'hh:mm:ss' format
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:  # 'mm:ss' format
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        else:
            logger.error("Invalid time format")
            return 0.0

    def get_next_time(self, start_time: Optional[float], containers) -> Optional[float]:
        """
        Finds the end time for the current transcript segment.
        """
        for idx, container in enumerate(containers):
            time_button = container.find("button", class_="OexEjZt7Kf7pFUW701v8")
            if time_button:
                start_time_str = container.find("span").text
                if self.convert_time_to_seconds(start_time_str) == start_time:
                    if idx < len(containers) - 1:
                        next_container = containers[idx + 1]
                        next_time_button = next_container.find("button", class_="OexEjZt7Kf7pFUW701v8")
                        if next_time_button:
                            next_time_str = next_container.find("span").text
                            return self.convert_time_to_seconds(next_time_str)
                    break
        return None

    def parse_data(self, page: str):
        soup = BeautifulSoup(page, "html.parser")

        containers = soup.find_all("div", class_="l6peddfW1BiAnd1a_mF3")
        fragments = []

        for container in containers:
            time_button = container.find("button", class_="OexEjZt7Kf7pFUW701v8")
            start_time = None
            if time_button:
                start_time_str = container.find("span").text
                start_time = self.convert_time_to_seconds(start_time_str)

            text_containers = container.find_all("span", class_="Text__TextElement-sc-if376j-0")
            full_text = ""
            for text in text_containers[1:]:
                full_text += text.text

            end_time = self.get_next_time(start_time, containers) if start_time else None

            fragment = Fragment(start_time=start_time, end_time=end_time, transcriptions=full_text)
            fragments.append(fragment)

        return FragmentList(type_="GENERATED", fragments=fragments)

    def run(self):
        self.driver.get(self.url)

        self.driver.add_cookie({'name': 'sp_dc',
                                'value': 'AQBwO8eQN9t_5AQrKiRvh92rabQS9RAc3vU_2KWAsrccfmiHt4xXBacWRcWiOV-20NJIVNC6I3c64U_NILkMp5cMmWqF-tGCLKSX6_myGRhqcetV-bSBSHebtnVJgpX3wmIV25iI6SpwWEUeXtA5_QPrAR9LGnlM'})
        self.driver.add_cookie({'name': 'sp_key', 'value': '4edf59e3-ab29-4fea-ac6b-3050e04a5b97'})
        self.driver.add_cookie({'name': 'sp_landing',
                                'value': 'https%3A%2F%2Fopen.spotify.com%2F%3Fsp_cid%3D7835a571ce47dd4579cf0929be9a3062%26device%3Ddesktop'})
        self.driver.add_cookie({'name': 'sp_m', 'value': 'pl'})
        self.driver.add_cookie({'name': 'sp_t', 'value': '7835a571ce47dd4579cf0929be9a3062'})
        time.sleep(2)

        self.driver.get(self.url)
        time.sleep(5)

        clicked_button = self.click_transcription_button()
        if not clicked_button:
            logger.error("Failed to click transcription button")
            return

        page_content = self.driver.page_source

        parsed_data = self.parse_data(page_content)

        return parsed_data
