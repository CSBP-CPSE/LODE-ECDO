'''
File:    SeleniumDataCollector.py
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


class SeleniumDataCollector(AbstractDataCollector):
    """
    Selenium bot to download data from ESRI portals
    """

    def __init__(self, cfg):
        self._url = cfg['url']
        self._reference = cfg["reference"]

        # initialise web driver
        # Edge is chosen by default
        # could be diversified at a later stage
        self._driver = webdriver.Edge()
        self._driver.maximize_window()
        self._driver.implicitly_wait(30)

        return

    def set_output_dir(self, d):
        self._output_dir = d

    def set_output_file(self, f):
        self._output_file = f

    def get_data(self):
        self._logger.info("%s collecting data from: %s" % (self, self._url))

        self._driver.get(self._url)

        side_panel = self._driver.find_element(By.CSS_SELECTOR, 'div.side-panel-ref')

        # last update
        last_update = side_panel.find_element(By.XPATH, ".//div/ul/li[@data-test='modified']/div").text
        self._logger.info("Last data update: %s" % last_update)

        # Find the button to open the download tab: it is the first one
        dwld_button = side_panel.find_element(By.XPATH, './/button')

        # Click on the button to open panel
        dwld_button.click()

        # Now the download tab has opened, parse it
        dwld_cards = self._driver.find_elements(By.CSS_SELECTOR, "div.dataset-download-card")

        w = WebDriverWait(self._driver, 10)
        w.until(EC.visibility_of(dwld_cards[0]))

        dwld_btns = [self._find_download_button(e) for e in dwld_cards]

        for btn in filter(lambda x: x["data_type"].lower() == "geojson", dwld_btns ):
            ActionChains(self._driver)\
                    .move_to_element(btn['button'])\
                    .click()\
                    .perform()

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
        #with open(os.path.join(self._output_dir, self._output_file), "w", encoding="utf8") as f:
        f = open(os.path.join(self._output_dir, self._output_file), "w", encoding="utf8")
        f.write(self._data)
        self._logger.info("%s data saved." % self)

    def set_logger(self, logger):
        self._logger = logger

    @staticmethod
    def _find_download_button(element):
        """
        Find download button from download panel
        """

        # hub card has a shadow root
        hub_card = element.find_element(By.XPATH, './/hub-download-card').shadow_root
        
        # "calcite card contains button and data type"
        calcite_card = hub_card.find_element(By.CSS_SELECTOR, 'calcite-card')
        
        data_type = calcite_card.find_element(By.XPATH, './/h3').text
        
        dwld_button = calcite_card.find_element(By.XPATH, './/div/calcite-button')
        
        return {'data_type': data_type, 'button': dwld_button}

    @staticmethod
    def _wait_for_downloads(dwn_dir):
        time.sleep(5)
        while any([filename.endswith(".crdownload") for filename in 
                os.listdir(dwn_dir)]):
            time.sleep(2)

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