from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

SCORE_SERVICE_URL = 'http://localhost:5001/'
driver = None

def setup():
    global driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def teardown():
    global driver
    driver.quit()

def test_score_service():
    driver.get(SCORE_SERVICE_URL)
    score_element = driver.find_element(By.ID, 'score')
    score = float(score_element.text)
    return 1 <= score <= 1000

if __name__ == "__main__":
    setup()
    result = test_score_service()
    teardown()

    if result:
        exit(0)
    else:
        exit(-1)


