import undetected_chromedriver as ucd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time, json

def extract_text(soup_obj, tag, attribute_name, attribute_value):
    txt = soup_obj.find(tag, {attribute_name: attribute_value}).text.strip() if soup_obj.find(tag, {attribute_name: attribute_value}) else ''
    return txt

all_views = {}
channels = []
base_url = "https://www.youtube.com/results?search_query="
print('''
\ /      ___            ___         
 Y  _     |    |_  _     |  _  _  | 
 | (_)|_| | |_||_)(/_    | (_)(_) | 
by dom is offline
''')
print("Input your keyword!")
keyword = input("()>> ")

options = Options()
options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = ucd.Chrome(chrome_options=options)

driver.get(base_url + keyword)

try:
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]')))
except TimeoutException:
    print("Loading took too much time!")
else:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    vidlist = soup.find('div', {'id': 'contents', 'class': 'ytd-section-list-renderer'})
    channel_infos = vidlist.find_all('div', {'class': 'style-scope ytd-video-renderer', 'id': 'channel-info'})
    
    for info in channel_infos:
        channel_name = info.find('a', {'class': 'style-scope ytd-video-renderer'})['href']
        channels.append(channel_name)
        channels = list(dict.fromkeys(channels))
    for channel_name in channels:
        url = "https://www.youtube.com" + channel_name + "/about"
        driver.get(url)
        time.sleep(0.6)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        about_section = soup.find('ytd-channel-about-metadata-renderer', {'class': 'style-scope ytd-item-section-renderer'})
        collumn = about_section.find('div', {'id': 'right-column'})
        views = collumn.find_all('yt-formatted-string', {'class': 'style-scope ytd-channel-about-metadata-renderer'})[1].text.strip()
        strippedviews = views.replace(',', '').split(' views')[0]
        all_views[channel_name] = int(strippedviews)
        print(f"Finished {channel_name}.")
    
    driver.quit()

# driver.find_element_by_xpath('//*[@id="text"]/a').text
with open('views.json', "w") as f:
    f.write(json.dumps(all_views, indent=2))