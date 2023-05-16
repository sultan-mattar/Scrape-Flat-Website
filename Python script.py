from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil


username = 'Your@Email.com' # Type You Email
password = '***********'    # Type You Password
executable_path = 'msedgedriver.exe'
source_folder = 'C:/Users/Sulta/Downloads'
destination_folder = 'C:/Users/Sulta/Downloads/Flat Music'
file_extension = '.mid'


def scraper():
    # create a new instance of the Edge driver
    driver = webdriver.Edge(executable_path)

    # navigate to the Flat page
    driver.get("https://flat.io/auth/signin?hl=en")
    driver.maximize_window()
    time.sleep(2)

    driver.find_element(By.ID, 'emailInput').send_keys(username)  # Use By.ID instead of By.XPATH
    driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(password)  # Use CSS selector
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()  # Use CSS selector

    print('Login Successfully!')
    time.sleep(5)

    # ---------------------------------------------------------------------------------------------
    driver.get("https://flat.io/community/popular/weekly")
    time.sleep(5)

    print("Scrolling The Page Now!............")
    for i in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')  # Specify the HTML parser
    time.sleep(5)

    print(len(soup.find_all('div', attrs={'class': 'wrapper_OQWyG'})))

    div_elements = driver.find_elements(By.CLASS_NAME, "title")
    links = []

    for div_element in div_elements:
        link_elements = div_element.find_elements(By.TAG_NAME, "a")
        for link in link_elements:
            href = link.get_attribute("href")
            if href:
                links.append(href)

    for link in links:
        try:
            driver.get(link)
            time.sleep(10)
            div_element = driver.find_element(By.XPATH, "//span[normalize-space()='Download or Print']")
            div_element.click()
            time.sleep(10)
            driver.find_element(By.XPATH, "//span[normalize-space()='MIDI (*.mid)']").click()

        except TimeoutError:
            print('TimeOut')

    driver.quit()


scraper()


def move_files_by_extension(source_folder, destination_folder, file_extension):
    # Get the list of files in the source folder
    files = os.listdir(source_folder)

    # Move files with the specified extension from the source folder to the destination folder
    for file in files:
        # Check if the file has the desired extension
        if file.endswith(file_extension):
            # Construct the source and destination paths
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)

            # Move the file
            shutil.move(source_path, destination_path)


move_files_by_extension(source_folder, destination_folder, file_extension)
