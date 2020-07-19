import requests, re, datetime
from bs4 import BeautifulSoup
import time

def user_input():
    #gets user input on loop and provides simple check for its validity
    dates = []
    #regex = r"2020-[0-3][0-9]-(0[1-9]|1[1-2])"

    while True:
        user_input = input("Wpisz date w formacie rr-mm-dd i kliknij Enter:\n By zakonczyc kliknij Enter bez wpisywania")
        if user_input == '':
            return dates
        year,month,day = user_input.split('-')
        #if re.findall(regex,user_input):
        #   dates.append(re.findall(regex,user_input))
        if datetime.datetime(year=int(year), month=int(month), day=int(day)):
            dates.append(user_input) #Im unsure about this line, maybe will try other method
        else:
            print('Wpisz date poprawnie')


def get_lottery_data(date):

    base_url = 'https://www.lotto.pl/eurojackpot/wyniki-i-wygrane/wyszukaj'
    #base_url = 'https://www.lotto.pl/lotto/wyniki-i-wygrane/wyszukaj'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/54.0.2810.1 Safari/537.36'
               }
    session = requests.session()

    root_page = session.get(base_url, headers=headers)
    soup = BeautifulSoup(root_page.text, 'html.parser')
    form_build_id = soup.find("input", {"name": "form_build_id"})['value']
    form_id = 'eurojackpot_wyszukaj_form'

    results = session.post(base_url, {'data_losowania[date]': date,
                                      'form_build_id': form_build_id,
                                      'form_id': form_id
                                      }, headers=headers)

    soup = BeautifulSoup(results.content, 'html.parser')


    numbers = soup.select("div.resultsItem.euroJackpot.sortrosnaco")[0]
    #numbers = soup.select("div.resultsItem.lotto.sortrosnaco")[0]  # .find("div", {'class':'resultsItem lotto sortrosnaco'})
    output = numbers.find_all(string=re.compile("[0-9]?[0-9]+"))  # findChild("div").

    # output = soup.find("table", {'class':'ostatnie-wyniki-table hidden-lg-down'})
    return output


def main():
    dates = user_input()  # ['2020-05-14','2020-05-02']
    for date in dates:
        print('Wyniki z dnia ', date, "=>", get_lottery_data(date))


#main()

def multiple_searches():
    date = '2020-05-22'
    #date = datetime.datetime.strptime(date, '%Y-%m-%d')
    #stuff = date - datetime.timedelta(weeks=1)
    #print('{:%Y-%m-%d}'.format(date), '->', '{:%Y-%m-%d}'.format(stuff))

    handle = open('results_sleep.csv', 'a')

    for week in range(141):
        #print('Wyniki z dnia ', date, "=>", get_lottery_data(date))
        try:
            numbers = ','.join(get_lottery_data(date))
        except IndexError:
            numbers = 'brak_wyniku'
        handle.write(date + ',' + numbers + '\n')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        next_week = date - datetime.timedelta(weeks=1)
        date = '{:%Y-%m-%d}'.format(next_week)
        time.sleep(3)


multiple_searches()