from time import sleep
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


SHORT_DELAY = 0.5
MEDIUM_DELAY = 1
LONG_DELAY = 1.5


class Calendar:
    months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    def __init__(self, driver) -> None:
        self.driver = driver
        
    def open(self):
        self.driver.find_element(By.ID, 'appointments_consulate_appointment_date_input').click()
        sleep(MEDIUM_DELAY)

    def close(self):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        sleep(MEDIUM_DELAY)

    def previous(self):
        self.driver.find_element(By.CLASS_NAME, 'ui-datepicker-prev').click()
        sleep(SHORT_DELAY)

    def next(self):
        self.driver.find_element(By.CLASS_NAME, 'ui-datepicker-next').click()
        sleep(SHORT_DELAY)

    def current_months(self):
        months = []

        elements = self.driver.find_elements(By.CLASS_NAME, 'ui-datepicker-month')

        for element in elements:
            months.append([element.text, Calendar.months.index(element.text) + 1])

        return months

    def current_years(self):
        years = []

        elements = self.driver.find_elements(By.CLASS_NAME, 'ui-datepicker-year')

        for element in elements:
            years.append(int(element.text))

        return years

    def closest_day_available(self):
        current_years = self.current_years()
        current_months = self.current_months()
        
        months = self.driver.find_elements(By.CLASS_NAME, 'ui-datepicker-group')
        
        for month in months:
            days = month.find_elements(By.CLASS_NAME, 'ui-state-default')

            for day in days:
                if day.get_attribute('href') != None:
                    return date(current_years[months.index(month)], current_months[months.index(month)][1], int(day.text))

        return None


class VisaPage:
    def __init__(self, executable_path) -> None:
        self.driver = self.create_driver(executable_path)
        self.calendar = Calendar(self.driver)

    def refresh(self):
        self.driver.refresh()
        sleep(LONG_DELAY)

    def open(self, schedule_url):
        self.driver.get(schedule_url)
        sleep(MEDIUM_DELAY)

    def login(self, email, password):
        self.driver.find_element(By.CLASS_NAME, 'ui-dialog-titlebar-close').click()
        sleep(SHORT_DELAY)

        self.driver.find_element(By.ID, 'user_email').send_keys(email)
        sleep(SHORT_DELAY)

        self.driver.find_element(By.ID, 'user_password').send_keys(password)
        sleep(SHORT_DELAY)
        
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'policy_confirmed'))
        sleep(SHORT_DELAY)

        self.driver.find_element(By.NAME, 'commit').click()
        sleep(LONG_DELAY)

    def select_state(self, state):
        select = Select(self.driver.find_element(By.ID, 'appointments_consulate_appointment_facility_id'))
        select.select_by_visible_text(state)

    def create_driver(self, executable_path):
        options = Options()

        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_argument('--start-maximized')
        options.add_argument("--disable-notifications")

        driver = webdriver.Chrome(options=options, executable_path=executable_path)
        driver.implicitly_wait(1.5)

        return driver
