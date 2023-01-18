from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Edge() #Firefox(executable_path=r"C:\Users\barisma\geckodriver-v0.32.0-win32\geckodriver.exe")

driver.get("https://catalogue-moncton.opendata.arcgis.com/datasets/moncton::points-of-interest/explore?filters=eyJDQVRFR09SWSI6WyJFTUVSR0VOQ1kiXX0%3D")
#driver.get("https://opendata.norfolkcounty.ca/datasets/fire-halls")
driver.maximize_window()
driver.implicitly_wait(30)
#driver.execute_script("document.body.style.zoom='80%'")

buttons = driver.find_element(By.CSS_SELECTOR, "div.hub-toolbar-inner.hide-overflow").find_elements(By.XPATH, './/button')  
buttons

buttons[-3].click()

# get side panel (could be used for metadata)
#side_panel = driver.find_element(By.CSS_SELECTOR, 'div.side-panel-content')
#side_panel

#card = driver.find_element(By.XPATH, '//hub-download-card')
#card

dwld_cards = driver.find_elements(By.CSS_SELECTOR, "div.dataset-download-card")

def find_download_button(element):
    # hub card has a shadow root
    hub_card = element.find_element(By.XPATH, './/hub-download-card').shadow_root
    
    # "calcite card contains button and data type"
    calcite_card = hub_card.find_element(By.CSS_SELECTOR, 'calcite-card')
    
    data_type = calcite_card.find_element(By.XPATH, './/h3').text
    
    dwld_button = calcite_card.find_element(By.XPATH, './/div/calcite-button')
    
    return {'data_type': data_type, 'button': dwld_button}

downloads = [find_download_button(e) for e in dwld_cards]
downloads

for btn in filter(lambda x: x["data_type"].lower() == "geojson", downloads):
    ActionChains(driver)\
            .move_to_element(btn['button'])\
            .click()\
            .perform()

# https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getDownLoadedFileName(driver):
    driver.execute_script("window.open()")
    WebDriverWait(driver, 10).until(EC.new_window_is_opened)
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("edge://downloads/all")

    # get the first element, usually the download is quite quick
    name = driver.find_element(By.XPATH, '//button[contains(@id, "open_file")]').text
    
    # close and return to first window
    driver.execute_script("window.close()")
    driver.switch_to.window(driver.window_handles[0])
    
    return name

out_name = getDownLoadedFileName(driver)

print(out_name)

driver.quit()