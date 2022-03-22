import yagmail
import os
import pandas
from news import NewsFeed
import datetime
import configparser


def get_config_data():
    global sender_email, sender_pwd

    config_filename = "newsfeed_config.txt"
    config_filepath = os.path.join(path_cur_dir, config_filename)
    parser = configparser.ConfigParser()
    parser.read_file(open(config_filepath))

    # enter email account to use to send the email message from
    # (supply the parameters in the config file)
    sender_email = parser.get('Settings', 'sender_email')
    sender_pwd = parser.get('Settings', 'sender_pwd')

def send_email():
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    # news_feed = NewsFeed(interest=row['interest'], from_date=datetime.date.today(), to_date=datetime.date.today())
    news_feed = NewsFeed(interest=row['interest'],
                         from_date=yesterday,
                         to_date=today)
    email = yagmail.SMTP(user=sender_email, password=sender_pwd)
    email.send(to=row["email"],
               subject=f"Your {row['interest']} news for today",
               contents=f"Hi {row['name']}\n Here's the latest {row['interest']} news: \n\n{news_feed.get()}\n")


# get recipient emails and interests from file
path_cur_dir = os.path.abspath(os.getcwd())
print(path_cur_dir)
df = pandas.read_excel(os.path.join(path_cur_dir, 'email_list.xlsx'), engine='openpyxl')

# get data from config file
get_config_data()

for index, row in df.iterrows():
    send_email()

