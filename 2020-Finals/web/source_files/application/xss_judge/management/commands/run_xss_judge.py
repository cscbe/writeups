import time

from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from tweets.models import Tweet
from os import getenv

class Command(BaseCommand):
    help = "Start the XSS judge"
    baseUrl = getenv("BASE_URL", "http://localhost:8000/")
    password = getenv("ADMIN_PASSWORD")
    username = "admin"

    def handle(self, *args, **options):
        while True:
            time.sleep(5)
            try:
                self.run_xss_judge()
            except Exception as e:
                print(e)

    def run_xss_judge(self):
        print("Polling tweets")

        try:
            tweets = Tweet.objects.filter(admin_verified=False)
            for tweet in tweets:
                print(tweet)

                try:
                    requests.post(
                        self.baseUrl + "accounts/login"
                    )
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    chrome_options.add_argument("--no-sandbox")
                    with webdriver.Chrome(chrome_options=chrome_options) as driver:
                        driver.get(self.baseUrl + "accounts/login")

                        driver.find_element_by_id("id_username").send_keys(self.username)
                        driver.find_element_by_id("id_password").send_keys(self.password)

                        driver.find_element_by_id("submit-button").click()

                        driver.get(self.baseUrl + "tweets/show/"+str(tweet.pk))
                        try:
                            link = driver.find_element_by_id("tweet-link")
                            link.click()
                        except Exception as e:
                            # Link not found
                            print(e)

                        time.sleep(10)
                    tweet.admin_verified = True
                    tweet.save()
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)
        finally:
            # Do not throw exceptions, that will stop future executions
            return True


