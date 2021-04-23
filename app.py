#Import
import streamlit as st
import pandas as pd
from selenium import webdriver
import chromedriver_binary
# from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import os

CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"


def bien_ici_loc(ville,cp):
    apt_dict = { 'place': [], 'location': [], 'price': [], 'picture':[] }
    num_pg = 4
    for npage in range(1, num_pg + 1):
        url = f"https://www.bienici.com/recherche/location/{ville}-{cp}?page={npage}"
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get(GOOGLE_CHROME_BIN)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH") ,chrome_options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "tt-input")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for div_p in soup.find_all(name='span', attrs={"class":'generatedTitleWithHighlight'}):
            apt_dict['place'].append(div_p.text.strip().replace('\xa0', ' '))
    #             print(apt_dict['place'])
        for div_l in soup.find_all(name='div', attrs={"class":'details'}):
            for a_l in div_l.find_all(name="div", attrs={"class":"cityAndDistrict"}):
                apt_dict['location'].append(a_l.text.strip().replace('\xa0', ' '))
    #                 print(apt_dict['location'])
        for div_pr in soup.find_all(name='div', attrs={"class":'details'}):
            for a_pr in div_pr.find_all(name="span", attrs={"class":"thePrice"}):
                apt_dict['price'].append(int(a_pr.text.strip().replace('\xa0', '',).replace('€','')))
    #                 print(apt_dict['price'])
        for div_pic in soup.find_all(name='div', attrs={"class":'detailsContent adOverview changeStyleOnHover'}):
            for a_pic in div_pic.find_all("img"):
                apt_dict['picture'].append(a_pic['src'])
    #                 print(apt_dict['picture'])
    return pd.DataFrame.from_dict(apt_dict,orient='index')

input_city = st.text_input("Choisissez votre ville", "rennes")
input_cp =  st.text_input("entrez le code postal", "35000")

df = bien_ici_loc(input_city, input_cp)
df = df.transpose()


if st.checkbox('Show result', False):
    for i in range(10):
        st.image(df.iloc[i]['picture'],width=300,
                        caption=df.iloc[i]['place'])
        st.write(df.iloc[i]['location'])
        st.write("prix loyer cc: (€)",df.iloc[i]['price'])
        # st.write(df.iloc[i]['location'])


