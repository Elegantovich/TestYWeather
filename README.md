# TestYWeather
get data from yandex weather using selenium


![Status](https://github.com/elegantovich/TestYWeather/actions/workflows/main.yml/badge.svg)
## Description
Скрипт для обработки данных с интерфейса сервиса "Яндекс Погода".

### Tech
Python 3.10, Selenium 4.3, Pandas 1.3


### How to start a project:
Тестирование производилось на браузере Google chrome. Для старта необходимо узнать версию браузера.
```
chrome://settings/help
```
Скачайте и положите в папку с приложением драйвер, с версией поддерживаемой вашим браузером:
```
https://sites.google.com/chromium.org/driver/
```


Clone and move to local repository:
```
git clone https://github.com/Elegantovich/TestYWeather/
```
Create a virtual environment (win):
```
python -m venv venv
```
Activate a virtual environment:
```
source venv/Scripts/activate
```
Install dependencies from file requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Run the script
```
python test.py
```
input city

## Notes
- Расположение драйвера по дефолту настроено в папке с проектом
- Результаты работы в виде ексель документа и БД будут находиться в папке с проектом
- После запуска приложения следуйте инструкциям на терминале

