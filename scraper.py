import time
import logging
import os
from datetime import datetime, timedelta
import traceback
import pandas as pd
import copy
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


username_id = "your_user_name"
psswd = "your_password"
file_name = r'data_' + datetime.now().strftime("%b_%d_%Y") + '_helium_pressure' + '.xlsx'
file_loc = r'C:\Helium Data\location' + file_name
log_file = r'C:\Helium Data\scraper.log'

logging.basicConfig(filename=log_file,
                            filemode='a',
                            format='%(levelname)s %(asctime)s :: %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Scraping Helium")

logger = logging.getLogger('urbanGUI')

#os.chdir('C://Users/shiva/OneDrive/Documents/pandas_file')
into = pd.read_csv('default_data.csv')
system_ids = into['SYSTEM ID'].values.tolist()

into.drop(['SYS_VERSION'], axis=1, inplace=True)

into['PRESSURE'] = 0.0
into['LEVEL'] = '0'
into['LAST UPLOAD (IST)'] = '0'


def scrape_func(driver, no, df):
    driver.refresh()
    logger.critical("Commencing Function!")
    for a3 in range(20):
        try:
            driver.get(main_url) 
            print("Processing this sytem_id:", df.loc[no, 'SYSTEM ID'])
            logger.critical("Entering System ID input step, a4")
            for a4 in range(20):
                try:
                    system_id = driver.find_element_by_id("ID_HP_SystemID_InputBox")
                    system_id.clear()
                    system_id.send_keys(df.loc[no, 'SYSTEM ID'])
                    driver.find_element_by_xpath('//*[@type="submit"]').click() # Type is submit
                    logger.critical("Entering Research tab finder/data scraper step, a5")
                    for a5 in range(20):
                        try:
                            logger.critical("Currently trying to find 'RESEARCH', in a5: " + str(a5))
                            print("Currently trying to find 'RESEARCH', in a5: " + str(a5))
                            fastrack = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "RESEARCH")))
                            fastrack.click()

                            # driver.find_element_by_id("RESEARCH").click() # id RESEARCH
                            for a6 in range(20):
                                try:
                                    logger.critical("Currently trying to find 'Parameters', in a6: " + str(a6))
                                    print("Currently trying to find 'Parameters', in a6: " + str(a6))

                                    #driver.find_element_by_xpath('//*[@id="magmonReletedWidgets"]/div/div[2]/ul/li[2]/a').click()
                                    fastrack = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Parameters")))
                                    ActionChains(driver).move_to_element(fastrack).click().perform()
                                    #fastrack.click()
                                    # driver.find_element_by_link_text("").click()
                                    for a7 in range(20):
                                        try:
                                            logger.critical("Currently trying to find values, in a7: " + str(a7))
                                            print("Currently trying to find values, in a7: " + str(a7))
                                            fastrack = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='A13ReportedDataId']")))
                                            he_pressure = driver.find_element_by_xpath("//span[@id='A13ReportedDataId']").text
                                            he_pressure = float(he_pressure)
                                            he_level = driver.find_element_by_xpath("//span[@id='A2ReportedDataId']").text
                                            last_updated = driver.find_element_by_xpath("//span[@id='parametersLastUpdatedDateId']").text
                                            last_updated = (datetime.strptime(last_updated, '%d-%b-%Y %H:%M:%S GMT') + timedelta(hours=5, minutes=30)).strftime('%I:%M %p,  %b %d %Y')
                                            df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'PRESSURE'] = he_pressure
                                            df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'LEVEL'] = he_level
                                            df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'LAST UPLOAD (IST)'] = last_updated
                                            print("Exiting a7 successfully")
                                            break
                                        except:
                                            print("Couldn't find values, in a7: " + str(a7) + " trying again")
                                            logger.critical("Couldn't find values, in a7: " + str(a7) + " trying again")
                                            time.sleep(0.5)
                                    if no == 0 and df.loc[no, 'PRESSURE'] != 0.0:
                                        logger.critical("In a6, no == 0, got pressure" + str(he_pressure) + " level: " + str(he_level) + "breaking")
                                        print("In a6, no == 0, got pressure: " + str(he_pressure) + " level: " + str(he_level) + ", breaking")
                                        break
                                    elif df.loc[no, 'PRESSURE'] == 0.0 or df.loc[no, 'PRESSURE'] is None:
                                        logger.critical("In a6, pressure equal to 0 or None, pass")
                                        print("In a6, pressure equal to 0, pass")
                                        pass
                                    # elif df.loc[no-1, 'PRESSURE'] != None or df.loc[no-1, 'PRESSURE'] != 0.0:
                                    #     if df.loc[no-1, 'PRESSURE'] == df.loc[no, 'PRESSURE']:
                                    #         logger.critical("In a6, pressure for last item equal to current item, pass")
                                    #         print("In a6, pressure for last item equal to current item, pass", df.loc[no-1, 'PRESSURE'], df.loc[no, 'PRESSURE'])
                                    #         pass
                                    #     else:
                                    #         print("In a6, pressure for last item isn't None or last pressure isn't 0, ", df.loc[no-1, 'PRESSURE'], " ", df.loc[no, 'PRESSURE'], " break")
                                    #         break
                                    else:
                                        logger.critical("In a6, all good, pressure:" + str(he_pressure) + " level: " + str(he_level) + " break")
                                        print("In a6, all good, pressure:" + str(he_pressure) + " level: " + str(he_level) + " break")
                                        break
                                except Exception as e:
                                    logger.critical("In a6, got except: " + str(e) + " for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", sleeping for 1 second")
                                    print("In a6, got except: " + str(e) + " for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", sleeping for 1 second")

                                    # try:
                                    #     print("I see following values: ", df.loc[df['SYSTEM ID'] == system_ids[no - 1], 'PRESSURE'], df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'PRESSURE'])
                                    # except:
                                    #     print("Tried printing pressure")
                                    if a6 == 5 or a6 == 10 or a6 == 15:
                                        try:
                                            driver.find_element_by_xpath('//*[@id="magmonReletedWidgets"]/div/div[2]/ul/li[2]/a').click()
                                            if a6 == 5:
                                                logger.critical("In a6, and a6 is 5, clicking again on Parameters")
                                            elif a6 == 10:
                                                logger.critical("In a6, and a6 is 10, clicking again on Parameters")
                                            elif a6 == 15:
                                                logger.critical("In a6, and a6 is 15, clicking again on Parameters")
                                        except Exception as e:
                                            print("Got exception: " + str(e) + " Couldn't click on Parameters")
                                            if a6 == 5:
                                                logger.critical("In a6, and a6 is 5, tried clicking on Parameters, couldn't click")
                                            elif a6 == 10:
                                                logger.critical("In a6, and a6 is 10, tried clicking on Parameters, couldn't click")
                                            elif a6 == 15:
                                                logger.critical("In a6, and a6 is 15, tried clicking on Parameters, couldn't click")
                                    if a6 == 19:
                                        logger.critical("In a6, a6 == 19, setting to None values")
                                        df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'PRESSURE'] = None
                                        df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'LEVEL'] = None
                                        df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'LAST UPLOAD (IST)'] = None
                                    print("Stack Trace: ", traceback.format_exc())
                                    print("Sleeping inner loop 1 sec")
                                    time.sleep(1)
                            break
                        except Exception as e:
                            logger.critical("In a5, got except: " + str(e) + " for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", sleeping for 1 second")
                            # try:
                            #     print("I see following values: ", df.loc[df['SYSTEM ID'] == system_ids[no - 1], 'PRESSURE'], df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'PRESSURE'])
                            # except:
                            #     print("Tried printing pressure")
                            if a5 == 5 or a5 == 10 or a5 == 15:
                                try:
                                    driver.find_element_by_id("RESEARCH").click()
                                    if a5 == 5:
                                        logger.critical("In a5, and a5 is 5, clicking again on research")
                                    elif a5 == 10:
                                        logger.critical("In a5, and a5 is 10, clicking again on research")
                                    elif a5 == 15:
                                        logger.critical("In a5, and a5 is 15, clicking again on research")
                                except Exception as e:
                                    print("Got exception: " + str(e) + " Couldn't click on research")
                                    if a5 == 5:
                                        logger.critical("In a5, and a5 is 5, tried clicking on research, couldn't click")
                                    elif a5 == 10:
                                        logger.critical("In a5, and a5 is 10, tried clicking on research, couldn't click")
                                    elif a5 == 15:
                                        logger.critical("In a5, and a5 is 15, tried clicking on research, couldn't click")
                            if a5 == 19:
                                logger.critical("In a5, a5 == 19, setting to None values")
                                df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'PRESSURE'] = None
                                df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'LEVEL'] = None
                                df.loc[df['SYSTEM ID'] == df.loc[no, 'SYSTEM ID'], 'LAST UPLOAD (IST)'] = None
                            print("Stack Trace: ", traceback.format_exc())
                            print("Sleeping inner loop 1 sec")
                            time.sleep(1)
                    if a5 == 19:
                        logger.critical("In a5, couldn't scrape for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", break")
                        print("In a5, couldn't scrape for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", break")
                    else:
                        logger.critical("In a5, all good for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", break")
                        print("In a5, all good for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", break")
                    break
                except Exception as e:
                    logger.critical("In a4, got except: " + str(e) + "  for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", sleeping for 1 second")
                    print("In a4, got except: " + str(e) + "  for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", sleeping for 1 second")
                    print("Sleeping outer loop 1 sec")
                    time.sleep(1)
            logger.critical("In a4, all good for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", break")
            print("In a4, all good for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", break")
            break
        except Exception as e:
            logger.critical("In a3, got except: " + str(e) + "  for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", sleeping for 1 second")
            print("In a3, got except: " + str(e) + "  for sytem_id " + df.loc[no, 'SYSTEM ID'] + ", sleeping for 1 second")
            print("Sleeping v.outer loop 1 sec")
            time.sleep(1)
# Starting Execution

browser = webdriver.Chrome('chromedriver.exe')
browser.get('https://ffa.health.ge.com/#/rfs')

logger.critical("Starting scraper for " + datetime.now().strftime('%b_%d_%Y'))

try:
    print("Opened website")
    logger.critical("Opened website, entering username")

    # First level, is entering the username 
    for a1 in range(20): 
        try:
            username = browser.find_element_by_id("identifierInput")
            username.clear
            username.send_keys(username_id)
            logger.critical("Successfully sent username, moving on")
            break
        except:
            logger.critical("Got Except in a1, sleeping for 1 second")
            time.sleep(1)
        

    browser.find_element_by_xpath('//*[@type="button"]').click()

    # Second level, is entering the password
    logger.critical("Entered username, Entering password")
    for a2 in range(20): 
        try:
            password = browser.find_element_by_id("password")
            password.clear()
            password.send_keys(psswd)
            logger.critical("Successfully sent password, moving on")
            break
        except:
            logger.critical("Got Except in a2(password entering sectionn), sleeping for 1 second")
            time.sleep(1)

    browser.find_element_by_xpath('//*[@type="button"]').click()

    current_url = browser.current_url
    while browser.current_url != 'https://ffa.health.ge.com/#/di/home' or not browser.current_url.startswith('https://ffa.health.ge'):
        time.sleep(1)
    
    time.sleep(5)

    main_url = 'https://ffa.health.ge.com/#/di/home'
    print("Shape of csv file: ", into.shape[0])
    for no in range(into.shape[0]):
        browser_copy = copy.copy(browser)
        # browser_copy = deepcopy(browser)
        scrape_func(browser_copy, no, into)
    browser.quit()

except (BaseException, Exception) as e:
    logger.critical("In outermost loop, got except: " + str(e) + "   Quitting")
    print(f"Exception: {e}")
    print("Stack Trace: ", traceback.format_exc())
    browser.quit()

    
try:
    browser.quit()
except:
    pass

def color_red_or_green(val):
    color = 'red' if val > 2.5 or val < 0.9  else 'green'
    return 'color: %s' % color

def color_level_black(val):
    color = 'black'
    return 'color: %s' % color

def date_color_red_or_green(val):
    try:
        color = 'red' if (datetime.today() - datetime.strptime(val, '%I:%M %p,  %b %d %Y')).total_seconds()/86400 > 3 else 'black'
    except:
        color = 'red'
    return 'color: %s' % color

into = into.style.applymap(color_red_or_green, subset=pd.IndexSlice[:, ['PRESSURE']])
into = into.applymap(color_level_black, subset=pd.IndexSlice[:, ['LEVEL']])
into = into.applymap(date_color_red_or_green, subset=pd.IndexSlice[:, ['LAST UPLOAD (IST)']])

file_location = file_loc

if os.path.isfile(file_location):
    os.remove(file_location)

into.to_excel(file_location)

#into.to_csv(r'C:\Helium Data\data_' + datetime.now().strftime("%b_%d_%Y") + '_helium_pressure' + '.csv', index=False)
