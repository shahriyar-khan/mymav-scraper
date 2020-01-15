import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

path = "\\mymav_scraper\\chromedriver.exe"


def main():

    # Initialize Driver (Headless)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(path, options=options)
    actions = ActionChains(driver)
    scraper(driver, actions)
    driver.quit()


def scraper(driver, actions):

    # Splash Page
    driver.get("https://www.uta.edu/mymav/")
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "studentBtn"))).click()
    except TimeoutException:
        driver.quit()
        print("Failed: MyMav is under maintenance!")
        exit()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "login-btn"))).click()

    # 2FA Login
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "i0116"))).send_keys("email")
    driver.find_element(By.ID, "idSIButton9").click()
    driver.find_element(By.ID, "i0118").send_keys("pw")
    time.sleep(2)
    actions.send_keys(Keys.ENTER).perform()
    code = int(input("Enter 2FA Code: "))
    print("2FA Sent!")
    print("Scraping...")
    driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC").send_keys(code)
    time.sleep(2)
    actions.send_keys(Keys.ENTER).perform()

    # Shopping Cart Text Scrape
    time.sleep(2)
    driver.get("https://mymav.utshare.utsystem.edu"
               "/psc/ARCSPRD_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL")
    a = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "DERIVED_SSR_FL_SSR_DESCR50$0"))).text  # INSY 3303-001
    b = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_DESCR50$1").text  # INSY 3303-003
    c = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_DESCR50$2").text  # INSY 3330-001
    d = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_DESCR50$3").text  # INSY 4305-002
    e = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_DESCR50$4").text  # INSY 4305-001

    # Search Scrape
    driver.get("https://mymav.utshare.utsystem.edu/psc/"
               "ARCSPRD_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "SSR_CSTRMCUR_VW_DESCR$0"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "PTS_KEYWORDS3"))).send_keys("INSY 3304")
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(2)
    actions.send_keys(Keys.TAB).perform()
    time.sleep(2)
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(4)
    f = driver.find_element(By.ID, "SSR_CLSRCH_F_WK_SSR_DESCR50_1$2").text  # INSY 3304-003
    print_table(a, b, c, d, e, f)


def print_table(a, b, c, d, e, f):
    print()
    print("[Results]")
    lists = [a, b, c, d, e, f]
    if any("Open" in x for x in lists):
        print("OPEN: There's a class in this list that is open right now, check manually!")
    elif any("Waitlist" in x for x in lists):
        print("3303-001 (Networks): {}".format(int(a[32:34]) - int(a[25:28])), "people waitlisted")
        print("3303-003 (Networks): {}".format(int(b[32:34]) - int(b[25:28])), "people waitlisted")
        print("3330-001 (E-Commerce): {}".format(int(c[32:34]) - int(c[25:28])), "people waitlisted")
        print("4305-002 (Java I): {}".format(int(d[32:34]) - int(d[25:28])), "people waitlisted")
        print("4305-001 (Java I): {}".format(int(e[32:34]) - int(e[25:28])), "people waitlisted")
        print("3304-003 (Database): {}".format(int(f[27:29]) - int(f[33:35])), "people waitlisted")


if __name__ == "__main__":
    main()
