1) python3 manage.py test - запуск всех тестов проекта
2) python3 manage.py test {test.name} - запуск выбранного теста, где test.name ссылка на тест
3) coverage run --source='.' manage.py test - запуск подсчёта покрытия тестами
4) coverage report > coverage_report.txt - получение отсчёта о покрытии тестами и его запись в текстовый файл
5) http://127.0.0.1:8000/api/docs/ - визуализация эндпоинтов