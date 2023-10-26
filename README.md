# Сравниваем вакансии программистов

Этот проект показывает 2 статистики по зарплатам программистов с API SJ и HH

### Как установить
Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

### Цель проекта

Перед запуском программы не забудьте склонировать проект или скачать его архив.В папке с проектом не забудьте содать .env файл, где вы укажите ваш собственный секретный ключ SJ(При регистрации приложения от вас потребуют указать сайт. Введите любой, они не проверяют.[Зарегистрироваться и создать токен.](https://api.superjob.ru/))
```
SJ_SECRET_KEY=ваш ключ с SJ
```

### Как запустить файл main.py
Для вывода в консоль таблиц необходимо запустить файл
```
python main.py
```