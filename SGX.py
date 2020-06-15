from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import os
import time
import datetime
import logging
import argparse
import shutil

# create global object
dateTimeObj = datetime.datetime.now()
typeOfDataChoice = ["tick", "tickdata_structure", "tc", "tc_structure", "all"]
typeOfData = ["tick", "tickdata_structure", "tc", "tc_structure"]
typeOfDataOptions_length = 0
dateOptions_length = 0

# Command Line Options
parser = argparse.ArgumentParser()
parser.add_argument("-wt", "--waittime", type=float, default=5,
                    help="Time for selenium web driver to wait for missing element(s) implicitly")
parser.add_argument("--number-of-dates", type=int, default=-1, choices=[-1, 1, 2, 3, 4],
                    help="Number of dates to retrieve (Default: -1, for all available dates)")
parser.add_argument("--type-of-data", type=str.lower, default="All", choices=typeOfDataChoice,
                    help="Type of data to retrieve (Default: all)")
args = parser.parse_args()

waitTime = args.waittime

# create and configure logger
logPath = "./logs/"
if not(os.path.isdir(logPath)):
    os.mkdir(logPath)

logFilename = logPath + dateTimeObj.strftime("%Y%m%d_%H-%M-%S") + '.log'
logging.basicConfig(filename=logFilename, format='[%(asctime)s] [Line %(lineno)d] [%(levelname)s] %(message)s', filemode='w', level=logging.INFO) 
logger=logging.getLogger()
logger.info("Logging [START]")

# create download folder
downloadPath = os.path.realpath("./" + dateTimeObj.strftime("%Y%m%d"))
if not(os.path.isdir(downloadPath)):
    os.mkdir(downloadPath)
    logger.info("Path \""+ downloadPath + "\" [CREATED]")
else:
    # In case when redownload needed, remove all previously downloaded files and redownload all
    shutil.rmtree(downloadPath)
    os.mkdir(downloadPath)
    logger.info("Path \""+ downloadPath + "\" [RECREATED]")

def checkAllFilesDownloaded():

    numberDownloads = len(os.listdir(downloadPath))
    numberRequired = typeOfDataOptions_length*dateOptions_length

    if(numberDownloads == numberRequired):
        logger.info("All required files has been downloaded")
    else:
        logger.warning("Some file(s) is/are missing or not downloaded")
        logger.warning("Downloaded files: " + str(numberDownloads))
        logger.warning("Required Files: " + str(numberRequired))
        actionAfterErrorOrFailureCaptured()
        
def actionAfterErrorOrFailureCaptured():
    # Any further actions should be done here:
    # Eg. Send Email/Message Notifications
    # Eg. Reschedule Task (Linux/Cloud Environment with Crantab)
    pass

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--start-maximised")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": downloadPath,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "useAutomationExtension": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--proxy-server=direct://')
chrome_options.add_argument('--proxy-bypass-list=*')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--allow-insecure-localhost')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver.exe")
logger.info("Chrome Driver [START]")

# get request to target the site selenium is active on
driver.get("https://www2.sgx.com/research-education/derivatives")

try:
    myElem = WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.ID, 'website-header')))
    logger.info("Webpage [LOADED]")

    driver.implicitly_wait(waitTime)
    time.sleep(waitTime)

    # find "Input-Select" css class for "Type of Data" and "Date"
    inputSelect = driver.find_elements_by_css_selector(".sgx-input-select-filter-wrapper")
    typeOfDataInputSelect = inputSelect[0]
    dateInputSelect = inputSelect[1]

    # get number of selections for "Type of Data" 
    typeOfDataInputSelect.click()
    typeOfDataOptions =  driver.find_elements_by_css_selector(".sgx-select-picker-list .sgx-select-picker-option label .sgx-select-picker-label")
    if(args.type_of_data == "all"):
        typeOfDataOptions_length = len(typeOfDataOptions)
        logger.debug("Type of Data: " + args.type_of_data)
        logger.debug("Number of Types: " + str(typeOfDataOptions_length))
    else:
        typeOfDataOptions_length = 1
        logger.debug("Type of Data: " + args.type_of_data)
        logger.debug("Number of Types: " + str(typeOfDataOptions_length))
    typeOfDataOptions[0].click()

    # get number of selections for "Date"
    dateInputSelect.click()
    dateOptions =  driver.find_elements_by_css_selector(".sgx-select-picker-list .sgx-select-picker-option label .sgx-select-picker-label")
    if(args.number_of_dates == -1):
        dateOptions_length = len(dateOptions)
        logger.debug("Number of Dates: " + str(dateOptions_length))
    else:
        dateOptions_length = args.number_of_dates
        logger.debug("Number of Dates: " + str(dateOptions_length))
    dateOptions[0].click()

    driver.implicitly_wait(waitTime)
    time.sleep(1)

    for i in range(typeOfDataOptions_length):

        # get all options and select an option
        typeOfDataInputSelect.click()
        typeOfDataOptions =  driver.find_elements_by_css_selector(".sgx-select-picker-list .sgx-select-picker-option label .sgx-select-picker-label")
        if(args.type_of_data == "All"):
            typeOfDataOptions[i].click()
            logger.debug(typeOfData[i] + " [SET]")
        else:
            index = typeOfData.index(args.type_of_data)
            typeOfDataOptions[index].click()
            logger.debug(typeOfData[index] + " [SET]")

        # always return date selection to default
        dateInputSelect.click()
        dateOptions =  driver.find_elements_by_css_selector(".sgx-select-picker-list .sgx-select-picker-option label .sgx-select-picker-label")
        dateOptions[0].click()
        logger.debug("Date 0 [SET]")

        driver.implicitly_wait(waitTime)
        time.sleep(1)

        for j in range(dateOptions_length):

            # click download button to download file
            download = driver.find_elements_by_css_selector(".sgx-button--primary")
            download[0].click()
            logger.debug("Download Button [CLICKED]")

            driver.implicitly_wait(waitTime)
            time.sleep(1)

            # select next date option
            dateInputSelect.click()
            dateOptions =  driver.find_elements_by_css_selector(".sgx-select-picker-list .sgx-select-picker-option label .sgx-select-picker-label")
            if not (j == (len(dateOptions)-1)):
                dateOptions[j+1].click()
                logger.debug("Date " + str(j+1) + " [SET]")
            else:
                dateOptions[0].click()
            
            driver.implicitly_wait(waitTime)
            time.sleep(1)

    # wait until no more downloads
    driver.get('chrome://downloads/')
    WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body/deep/downloads-manager')))
    logger.info("Chrome Download Page [LOADED]")

    # get downloads-manager element 
    manager = driver.find_element_by_css_selector('body/deep/downloads-manager')
    downloadInProgress = True
    while downloadInProgress:
        for item in manager.find_elements_by_css_selector('body/deep/downloads-item'):
            shadow = driver.execute_script('return arguments[0].shadowRoot;', item)
            text = shadow.find_element_by_css_selector('paper-button').text
            print(text)
            if text == 'PAUSE':
                break
        else:
            downloadInProgress=False
            break
    
    logger.info("Downloading Process [COMPLETED]")

except TimeoutException as e:
    logger.error(e)
    
except NoSuchElementException as e:
    logger.error(e)
    
except Exception as e:
    logger.error(e)

finally:
    checkAllFilesDownloaded()
    driver.quit()
    logger.info("Chrome Driver [END]")
    logger.info("Logging [END]")