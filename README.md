# Запуск
## 1. Установите python
## 2. Создайте виртуальную среду
```
python -m venv venv
```
На linux
```
python3 -m venv venv
```
Чтобы войти в нее
```
venv\Scripts\activate
```
На linux
```
source venv/bin/activate
```
## 3. Установите зависимости
```
pip install -r requirements.txt
```
## 4. Содайте файл .env и укажите API_KEY
```
API_KEY=<>
```
## 5. Запустите main.py
```
python main.py
```
