from dotenv import load_dotenv
from datetime import date
from time import sleep
import os

import telegram

from visa_page import VisaPage


class TelegramBot:
    def __init__(self, token, chat_id) -> None:
        self.token = token
        self.chat_id = chat_id

    def send_alert(self, msg):
        try:
            telegram_bot = telegram.Bot(self.token)
            telegram_bot.send_message(chat_id=self.chat_id, text=msg, parse_mode='html')
            return

        except Exception as error:
            print(error)


class VisaBot:
    def __init__(self) -> None:
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.schedule_url = os.getenv('SCHEDULE_URL')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.alert_chat_id = os.getenv('ALERT_CHAT_ID')

        self.telegram_bot = TelegramBot(self.telegram_bot_token, self.alert_chat_id)
        self.visa_page = VisaPage(executable_path='.\\chromedriver.exe')
        
        input('\n > Press enter to start.\n')
        
        self.visa_page.open(self.schedule_url)
        self.visa_page.login(self.email, self.password)
        
        self.verification_delay = 30
        self.verification()

    def verification(self):
        while True:
            try:
                self.visa_page.select_state('Sao Paulo')
                self.visa_page.calendar.open()

                while True:
                    closest_day_available = self.visa_page.calendar.closest_day_available()
                    current_months = self.visa_page.calendar.current_months()

                    if closest_day_available != None and closest_day_available < date(2023, 3, 20):
                        msg = f'🔔 [<strong>Alerta</strong>] Dia disponível em São Paulo: {closest_day_available.strftime("%d %B %Y")}'
                        
                        print(f'\n{msg}')
                        self.telegram_bot.send_alert(msg)
                        input(' > Press enter to continue.')

                    if current_months[0][0] == 'May' or current_months[1][0] == 'May':
                        break

                    self.visa_page.calendar.next()

                print(f' > Waiting {self.verification_delay} seconds...')
                sleep(self.verification_delay)
                self.visa_page.refresh()

            except:
                sleep(5)
                self.visa_page.open(self.schedule_url)
                self.visa_page.login(self.email, self.password)
                sleep(5)


if __name__ == '__main__':
    load_dotenv()
    VisaBot()
