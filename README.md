Скрипты для ноучного поиска династических параллелизмов в рамках теории Новой Хренологии.

Запуск:

```
virtualenv -p python3
. env/bin/activate
pip install -r requirements.txt
python load.py
python analyze.py
```

Скрипт load.py загружает данные из [Wikidata](https://www.wikidata.org/) в файл data.csv.

Скрипт analyze.py берёт данные из файла data.csv и пытается найти параллелизмы. Результаты записывает в файл output.csv.
