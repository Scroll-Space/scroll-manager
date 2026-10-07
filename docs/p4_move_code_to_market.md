# 4. Перенос кодовой базы в официальный репозиторий ONLYOFFICE

В корне проекта выполните python3 скрипт, который сам определит в какое место копировать файлы плагина среди всех плагинов:
```bash
python3 ./dev/move_code.py <PATH_TO_ROOT_onlyoffice.github.io>
```

В моем случае если форк репозитория onlyoffice расположен на том же уровне что каталог плагина:
```bash
python3 ./dev/move_code.py ../onlyoffice.github.io/
```