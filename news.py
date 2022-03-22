import requests
import configparser
import os

class NewsFeed:
    ###class to get the news items
    # news source = https://newsapi.org/
    # get api_key from above site and supply it in the config file

    def __init__(self, interest, from_date, to_date, language='en'):
        self.interest = interest
        self.from_date = from_date
        self.to_date = to_date
        self.language = language
        self.get_data_from_config()

    def get_data_from_config(self):
        # get parameters from config file
        # first get the current directory
        cur_dir = os.path.dirname(__file__)

        # next generate the absolute filepath of the config file
        config_filename = "newsfeed_config.txt"
        config_filepath = os.path.join(cur_dir, config_filename)

        # now get the data from the config file
        parser = configparser.ConfigParser()
        parser.read_file(open(config_filepath))
        self.base_url = parser.get('Settings', 'url')
        self.api_key = parser.get('Settings', 'api_key')

    def get(self):
        url = self._build_url()
        articles = self._get_articles(url)

        # construct the email body
        email_body = ""
        for article in articles:
            email_body = email_body + article["title"] + "\n" + article["url"] + "\n\n"

        return email_body

    def _get_articles(self, url):
        response = requests.get(url)
        content = response.json()
        articles = content['articles']
        return articles

    def _build_url(self):
        url = f"{self.base_url}" \
              f"qInTitle={self.interest}&" \
              f"from={self.from_date}&" \
              f"to={self.to_date}&" \
              f"language={self.language}&" \
              f"sortBy=popularity&" \
              f"apiKey={self.api_key}"
        return url


# if __name__ =="__main__":
#     feed = NewsFeed(interest='nasa', from_date=str(datetime.date.today()), to_date=str(datetime.date.today()), language="en")
#     print(feed.get())