from selenium import webdriver
from selenium.webdriver.common.by import By
import time

stUserName = "UnD3RG0n3"
stPassword = "watmm43msog"

driver = webdriver.Chrome()

driver.get("https://iptorrents.com/")
time.sleep(10)

clickUserField = driver.find_element(By.XPATH, "/html/body/div[2]/form/ul/li[1]/input")
time.sleep(2)
clickUserField.click()
clickUserField.send_keys(stUserName)

clickPassField = driver.find_element(By.XPATH, "/html/body/div[2]/form/ul/li[2]/input")
time.sleep(2)
clickPassField.click()
clickPassField.send_keys(stPassword)

time.sleep(3)
driver.quit()