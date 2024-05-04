from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup


@dataclass
class Transcript:
    start_time: Optional[str] = None
    text: Optional[str] = None


with open('spotify.html', encoding="utf-8") as f:
    data = BeautifulSoup(f, 'html.parser')


def parse(soup) -> None:
    containers = soup.find_all("div", class_="l6peddfW1BiAnd1a_mF3")

    for container in containers:
        time_button = container.find("button", class_="OexEjZt7Kf7pFUW701v8")
        start_time = None
        if time_button:
            start_time = container.find("span").text
        text_containers = container.find_all("span", class_="Text__TextElement-sc-if376j-0")

        full_text = ""
        for text in text_containers[1:]:
            full_text += text.text

        transcript = Transcript(start_time=start_time, text=full_text)
        print(transcript)


parse(data)
