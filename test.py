from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

city = 'moscow'
day = int(datetime.datetime.today().strftime('%d'))
driver = webdriver.Chrome('C:\\Dev\\TestYWeather\\chromedriver.exe')
driver.get(f'https://yandex.ru/pogoda/{city}/details?via=ms#{day}')
wait = WebDriverWait(driver, 10)


ids = driver.find_elements(By.XPATH,"//*[@class='forecast-fields']")
mag_list = [' '.join(ii2.text.split()[3:]) for ii2 in ids]

ids = driver.find_elements(By.XPATH,"//*[@class='weather-table']/tbody/tr/td")
count, count2, = 0, 0
list2, day_list, mid_time, mid_val_list = [], [], [], []
week = {}

for ii in ids:
    if count == 2:
        list2 = list2 + [' '.join(ii.text.split())]
    else:
        if count < 5:
            list2 = list2 + ii.text.split()
    count+=1
    if count == 7:
        day_list.append(list2)
        list2 = []
        count = 0
    if len(day_list) == 4:
        for time in day_list:
            mid_time = mid_time + time[1].split('…')
            if len(mid_time) == 6:
                mid_tuple = tuple(map(int, mid_time))
                mid_val = round((sum(mid_tuple)/6), 1)
                mid_time = []
                mid_val_list.append(mid_val)
                continue   
        try:
            week[day] = (day_list, mid_val_list[count2], mag_list[count2])
        except IndexError:
            week[day] = (day_list, mid_val_list[count2], None)
        day_list = []
        day+=1
        count2+=1
    if len(week) == 7:
        break


print(week)

