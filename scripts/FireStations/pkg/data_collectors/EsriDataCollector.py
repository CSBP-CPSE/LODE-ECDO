'''
File:    EsriDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Selenium bot to download data from ESRI portals

Created on: 2023-01-18
'''

import os, time

from .AbstractDataCollector import AbstractDataCollector

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 


class EsriDataCollector(AbstractDataCollector):
    """
    Selenium bot to download data from ESRI portals
    """

    def __init__(self, cfg):
        self._url = cfg['url']
        self._reference = cfg["reference"]
        self._data_type = cfg["data_type"]
        self._data = None

        return

    def set_output_dir(self, d):
        self._output_dir = d

    def set_output_file(self, f):
        self._output_file = f

    def get_data(self):
        # Check if data has been read into memory
        if self._data:
            self._logger.info("%s data in memory." % self)
            return True

        # if not, check if data cache is availble
        o_f = os.path.join(self._output_dir, self._output_file)
        if os.path.exists(o_f):
            self._logger.info("%s reading data from cache: %s" % (self, o_f))
            with open(o_f, "r", encoding="utf8") as f:
                self._data = f.read()
                self._logger.info("%s data read." % self)
                return True

        # otherwise download
        self._logger.info("%s collecting data from: %s" % (self, self._url))

        # initialise web driver
        # Edge is chosen by default
        # could be diversified at a later stage
        self._driver = webdriver.Edge()
        self._driver.maximize_window()
        self._driver.implicitly_wait(20)

        self._driver.get(self._url)

        side_panel = self._driver.find_element(By.CSS_SELECTOR, 'div.side-panel-ref')

        # last update
        last_update = side_panel.find_element(By.XPATH, ".//div/ul/li[@data-test='modified']/div").text
        self._logger.info("Last data update: %s" % last_update)

        # Find the button to open the download tab: it is the first one
        dwld_button = side_panel.find_element(By.XPATH, './/button')

        # Click on the button to open panel
        dwld_button.click()

        # Now the download tab has opened, parse it to find "calcite cards"
        dwld_cards = self._driver.find_elements(By.CSS_SELECTOR, "div.dataset-download-card")

        w = WebDriverWait(self._driver, 10)
        w.until(EC.visibility_of(dwld_cards[0]))

        # Keep only the one with the desired datatype
        calcite_card = list(filter(lambda x: x["data_type"].lower() == self._data_type,
                                    [self._find_calcite_card(e) for e in dwld_cards]
                        ))[0]["calcite-card"]

        # scroll to bottom of side panel to keep content in sight
        side_panel_dwld = list(filter(self._find_scrollable_element , 
                                self._driver.find_elements(By.CSS_SELECTOR, "div.side-panel-content")))
        
        # if the side panel is scrollable, scroll to the bottom
        if len(side_panel_dwld):                    
            scroll_height = side_panel_dwld[0].get_attribute("scrollHeight")
            self._driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", side_panel_dwld[0], scroll_height)

        push_button = self._find_download_button(calcite_card)
        push_button.click()

        # Assume the download path is the standard one
        # TODO: get it from the driver?
        # also, the environment is Windows-specific
        out_dir = os.path.join(os.environ['USERPROFILE'], "Downloads")

        self._wait_for_downloads(out_dir)

        out_name = self._getDownLoadedFileName()
        out_name = os.path.join(out_dir, out_name)

        self._logger.info("%s Downloaded data in: %s" % (self, out_name))

        # close the browser, removing the file lock
        self._driver.quit()

        # now read the data to memory and remove the file
        try:
            f = open(out_name, "r")
            self._data = f.read()
            f.close()
            self._logger.info("%s data collected" % self)
            succeed = True
        except IOError as e:
            self._logger.error("%s %s %s" % (self, e, e.errno))
            succeed = False
            
        os.remove(out_name)

        return succeed

    def get_reference(self):
        return self._reference

    def save_data(self):
        o_f = os.path.join(self._output_dir, self._output_file)
        self._logger.info("%s saving data to: %s" % (self, o_f))
        with open(o_f, "w", encoding="utf8") as f:
            f.write(self._data)
            self._logger.info("%s data saved." % self)

    def set_logger(self, logger):
        self._logger = logger

    def _find_calcite_card(self, element):
        """
        Find "calcite" card that contains download info
        """

        # hub card has a shadow root
        hub_card = element.find_element(By.XPATH, './/hub-download-card').shadow_root     

        # "calcite card contains button and data type"
        calcite_card = hub_card.find_element(By.CSS_SELECTOR, 'calcite-card')
        
        ActionChains(self._driver)\
            .move_to_element(calcite_card)\
            .perform()

        data_type = calcite_card.find_element(By.XPATH, './/h3').text

        return {'data_type': data_type, 'calcite-card': calcite_card}

    def _find_download_button(self, element):
                
        # check if calcite card has calcite button for update & download
        try:
            calcite_button = element.find_element(By.XPATH, './/div/calcite-dropdown/calcite-button')
        
            self._driver.execute_script("arguments[0].scrollIntoView(true);", calcite_button)

            calcite_button.click()
            
            # select the immediate download span element
            dwld_button = element.find_element(By.XPATH, './/div/calcite-dropdown/calcite-dropdown-group/calcite-dropdown-item[2]/span')
        except NoSuchElementException:
            # only one download button
            dwld_button = element.find_element(By.XPATH, './/div/calcite-button')
        
        return dwld_button

    @staticmethod
    def _wait_for_downloads(dwn_dir):
        time.sleep(2)
        while any([filename.endswith(".crdownload") for filename in 
                os.listdir(dwn_dir)]):
            time.sleep(2)

    @staticmethod
    def _find_scrollable_element(x):
        return int(x.get_attribute("scrollHeight")) > int(x.get_attribute("clientHeight"))

    def _getDownLoadedFileName(self):
        """
        Get name of latest downloaded file
        source: https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading
        """
        
        self._driver.execute_script("window.open()")
        WebDriverWait(self._driver, 10).until(EC.new_window_is_opened)
        self._driver.switch_to.window(self._driver.window_handles[-1])
        self._driver.get("edge://downloads/all")

        # get the first element, usually the download is quite quick
        name = self._driver.find_element(By.XPATH, '//button[contains(@id, "open_file")]').text
        
        # close and return to first window
        self._driver.execute_script("window.close()")
        self._driver.switch_to.window(self._driver.window_handles[0])
        
        return name