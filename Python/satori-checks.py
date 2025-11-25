from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# credentials
# consider storing these in an external file and importing them
stTsUser = "admin"
stTsPw = "SnitMern6"

stGpfsUser = "admin"
stGpfsPw = "Q0DhR2RaKO9QU5"

# sites
siteCheckMk = "https://admin:SnitMern6@omd.techsquare.com/satori/check_mk/index.py?start_url=%2Fsatori%2Fcheck_mk%2Fdashboard.py"
siteNoc = "http://172.30.100.217/satori/"
siteGPFS = "https://@172.16.100.113/"

# chrome instance
# adjust size, ignore ssl & certificate errors
options = Options()
options.add_argument("--window-size=1700,900")
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")     
# these options disable the chrome automated message
# formerly: options.add_argument("--disable-infobars")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

# open window and load checkmk
driver.get(siteCheckMk)
driver.implicitly_wait(2)
driver.execute_script("window.open('');")
driver.implicitly_wait(2)

# open new tab and load NOC
driver.switch_to.window(driver.window_handles[1])
driver.implicitly_wait(2)
driver.get(siteNoc)
driver.implicitly_wait(2)
# find "Username" field
clickUserField = driver.find_element(By.ID, "input_user")
clickUserField.click()
clickUserField.send_keys(stTsUser)
driver.implicitly_wait(2)
# find "Password" field
clickPassField = driver.find_element(By.ID, "input_pass")
clickPassField.click()
clickPassField.send_keys(stTsPw)
# find "Sign In" button
findButton = driver.find_element(By.ID, "_login")
findButton.click()
driver.implicitly_wait(2)

# open new tab and load GPFS GUI
driver.execute_script("window.open('')")
driver.implicitly_wait(2)
driver.switch_to.window(driver.window_handles[2])
driver.implicitly_wait(2)
driver.get(siteGPFS)
driver.implicitly_wait(2)
# find "Name" field
clickGpfsUser = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/form/div[1]/div[2]/input")
driver.implicitly_wait(2)
clickGpfsUser.send_keys(stGpfsUser)
driver.implicitly_wait(2)
# find "Password" field
clickGpfsPass = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/form/div[2]/div[2]/input")
clickGpfsPass.send_keys(stGpfsPw)
# find "Sign In" button
findGpfsButton = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/span/span")
findGpfsButton.click()


