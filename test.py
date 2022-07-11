import datetime
import os
import sqlite3

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

PRESSURE_UP = 'Ожидается резкое увеличение атмосферного давления'
PRESSURE_DOWN = 'Ожидается резкое падение атмосферного давления'
HEAD = ('Время суток', 'Температура', 'Погодное явление',
        'Давление, мм', 'Влажность')

create_db = ("CREATE TABLE IF NOT EXISTS report_dt("
             "id INTEGER PRIMARY KEY,"
             "date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
             "city TEXT,"
             "result TEXT);")
insert_into = ("INSERT INTO report_dt(city, result) "
               "VALUES(?, ?);")

date = datetime.datetime.today().strftime('.%m.%Y')
day = int(datetime.datetime.today().strftime('%d'))
date_sql = str(datetime.datetime.today().strftime('%H/%M - %m/%d/%Y'))
count, count2, count3 = 0, 0, 0
weather_list, day_list, mid_time, = [], [], []
week, pressure_list, mid_val_list = [], [], []


def to_excel(week):
    data = []
    for item in week:
        data += item
    data_table = pd.DataFrame(data, columns=HEAD)
    data_table.to_excel('WeekWeather.xlsx',
                        sheet_name=f'{str(day-7)}-{str(day)}',
                        index=False)
    os.startfile('WeekWeather.xlsx')


def create_report(create_db, city, error_exist, insert_into):
    conn = sqlite3.connect('report.db')
    cur = conn.cursor()
    cur.execute(create_db)
    params = (city, error_exist)
    cur.execute(insert_into, params)
    conn.commit()


if __name__ == "__main__":
    try:
        print('Please specify the city in English:')
        city = str(input())
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(f'https://yandex.ru/pogoda/{city}/details?via=ms#{day}')
        wait = WebDriverWait(driver, 10)
        body = driver.find_elements(By.XPATH, "//*[@class='forecast-fields']")
        mag_list = [' '.join(ii2.text.split()[3:]) for ii2 in body]
        if len(mag_list) == 0:
            raise Exception('Error, check the input data!')
        body = driver.find_elements(By.XPATH,
                                    "//*[@class='weather-table']/tbody/tr/td")
        for item in body:
            if count == 2:
                weather_list += [' '.join(item.text.split())]
            else:
                if count < 5:
                    weather_list += item.text.split()
            if count == 3:
                pressure_list.append(int(item.text))
                if len(pressure_list) == 4:
                    morning_pressure = pressure_list[0]
                    for pressure in pressure_list[1:]:
                        if abs(morning_pressure - pressure) >= 5:
                            if pressure > morning_pressure:
                                str_pressure = PRESSURE_UP
                            else:
                                str_pressure = PRESSURE_DOWN
                        str_pressure = None
                    pressure_list = []
            count += 1
            if count == 7:
                day_list.append(weather_list)
                weather_list = []
                count = 0
            if len(day_list) == 4:
                for time in day_list:
                    mid_time = mid_time + time[1].split('…')
                    if count3 == 2:
                        mid_tuple = tuple(map(int, mid_time))
                        mid_val = round((sum(mid_tuple)/len(mid_tuple)), 1)
                        mid_val_list.append(mid_val)
                        mid_time = []
                        count3 = 0
                        break
                    count3 += 1
                try:
                    day_list.append([f'{day}{date}',
                                     'Средняя дневная t = '
                                     f'{mid_val_list[count2]}',
                                     str_pressure, mag_list[count2], ''])
                except IndexError:
                    day_list.append([f'{day}{date}',
                                     'Средняя дневная t = '
                                     f'{mid_val_list[count2]}',
                                     str_pressure, None, ''])
                week.append(day_list)
                day_list = []
                day += 1
                count2 += 1
            if len(week) == 7:
                break
        to_excel(week)
    except Exception as error:
        error_exist = str(error)
    else:
        error_exist = 'Successful'
    finally:
        create_report(create_db, city, error_exist, insert_into)
        driver.close()
