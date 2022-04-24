<p align="center">
  <img width="640" height="360" src="https://github.com/thisisignitedoreo/pyyt/raw/main/pyyt.png">
</p>
# ВНИМАНИЕ
Я мигрирую в связи с недавними событиями с гитхаба на кодберг, [аккаунт](https://codeberg.org/ignitedoreo) и сам [pyyt](https://codeberg.org/ignitedoreo/pyyt)
# О Pyyt
pyyt (пиит) - простой консольный клиент YouTube на питоне, mpv, и youtube-dl<br />Возможно еще будут обновления
# Вдохновление
Взял идею у Черного Треугольника (https://www.youtube.com/c/%D0%A7%D1%91%D1%80%D0%BD%D1%8B%D0%B9%D0%A2%D1%80%D0%B5%D1%83%D0%B3%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D0%BA), он писал то-же самое, только проще. (хотя тут как посмотреть у кого проще)
# Зависимости
Утилиты: fzf, mpv, youtube-dl (ну или yt-dlp)<br />Pip3 модули: pytube, youtube-search-python, pyfzf
# Моддинг
В pyyt есть возможности очень простой модификации!<br />Для добавления своего пункта в меню нужно добавить стороку `channelnames.append("ID. КРАТКОЕ ОПИСАНИЕ")` после строки 36<br />Id это идентификационный номер функции. Советую ставить от 1000. (могут быть проблемы с подписками)<br />Для добавления логики в пункт нужно создать `elif` на подобии этого...
```
elif channelid == "ID":
        # любая логика
```
...после строки 49<br />Пример кастомной функции:
```
37         channelnames.append("1000. Обновить список")
...
50         elif channelid == "1000":
51                 print("Загрузка...")
52                 updatechannels()
```
