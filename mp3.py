from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from ytmusicapi import YTMusic
import re
import os
import shutil

videourl = ""
videoname = ""

def search_youtube1(query):
    videos_search = VideosSearch(query, limit = 1)
    results = videos_search.result()
    
    if len(results["result"]) > 0:
        first_video = results["result"][0]
        video_title = first_video["title"]
        video_url = first_video["link"]

        global videoname
        global videourl
        videoname = video_title
        videourl = video_url
        print("Title:", video_title)
        print("URL:", video_url)
        return video_url
    else:
        print("No videos found for the given query.")


def search_youtube2(query):
    ytmusic = YTMusic()
    search_results = ytmusic.search(query, filter = 'songs', limit = 1)
    
    if len(search_results) > 0:
        first_track = search_results[0]
        video_title = first_track['title']
        video_url = f'https://music.youtube.com/watch?v={first_track["videoId"]}'
        
        global videoname
        global videourl
        videoname = video_title
        videourl = video_url
        print("Title:", video_title)
        print("URL:", video_url)
        
        return video_url
    else:
        print("No tracks found for the given query.")


user_query = input("Enter your query: ")
ip = input("From where [1. Youtube  2. YT Music] : ")
if(ip == 1): 
    a = search_youtube1(user_query)
else: 
    a = search_youtube2(user_query)


# converter website 
# url = "https://ytmp3.nu/nBlF/"
# url = "https://ytmp3.page/txn/"
# url = "https://yt1s.de/youtube-to-mp4?l=en"
url = "https://cobalt.tools/"



# Path to your web driver executable (chromedriver)
driver_path = "C:/Users/ASUS/OneDrive/Desktop/DEV/youtube/chromedriver.exe"

service = Service(executable_path='C:/Users/ASUS/OneDrive/Desktop/dev/ytmusic/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.minimize_window()
driver.implicitly_wait(20)

chrome_options = Options()

try:
    driver.get(url)

    # Find the search input element by its name attribute (you need to inspect the page to find the correct attribute)
    # search_input = driver.find_element(By.NAME, "url")
    # search_input = driver.find_element(By.NAME, "q")
    search_input = driver.find_element(By.ID, "url-input-area")

    # YouTube/ YT Music video link
    youtube_link = videourl
    search_input.send_keys(youtube_link)

    # Submit the form (press Enter)
    search_input.send_keys(Keys.RETURN)

    # Wait for some time (you can adjust this as needed)
    time.sleep(20)

    # Locate and click the "Download" button (you need to inspect the page to find the correct element)
    # element = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]")
    # element = driver.find_element(By.XPATH, "//div[@mp3data]//a[@name='Download']")
    # element = driver.find_element(By.XPATH, "//a[@onclick=\"downloaddata('128')\"]")

    # element = driver.find_element(By.LINK_TEXT, "Download")
    # element.click()
    # driver.minimize_window()s

    # time.sleep(20)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    driver.quit()


# method to get the downloaded file name
filename = max([os.path.join('C:/Users/ASUS/Downloads', f) for f in os.listdir('C:/Users/ASUS/Downloads')], key=os.path.getctime)
shutil.move(filename,os.path.join('C:/Users/ASUS/Downloads',videoname + '.mp3'))