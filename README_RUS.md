# Отложенный репостинг в соцсетях
Программа публикует пост(картинку и текст) в трех соцсетях:
1. [ВКонтакте](https://vk.com/)
2. [Telegram](https://telegram.org/)
3. [Facebook](https://www.facebook.com/)
При этом программа публикует посты согласно расписанию в гугл таблице такого вида [ссылка](https://docs.google.com/spreadsheets/d/17r4QRW_m0clut772bRnUL-U1-JiazImiZMm43SkgS9Q/edit)

### Как установить
Для начала получите токен от VK, его можно получить следующим образом:

необходимо перейти по ссылке: https://oauth.vk.com/authorize?client_id=`Ваш_клиент_ID`&scope=photos,groups,wall,offline&response_type=token
где `Ваш_клиент_ID` это ID приложения которое можно посмотреть в настройках вашего [приложения](https://vk.com/apps?act=manage)
 
Далее необходимо получить токен от Телеграм, его вы получаете автоматически создавая бота.

Также нужен ключ(маркер доступа) с правом `publish_to_groups` от Фейсбук, его можно получить пройдя по [ссылке](https://developers.facebook.com/tools/explorer/) 
 
В файл `.env` необходимо записать следующие данные:
```text
VK_ACCESS_TOKEN="Ваш ключ от Вконтакте"
VK_CLIENT_ID='Ваш ID приложения Вконтакте'
VK_GROUP_ID='ID вашей группы Вконтакте'
VK_ALBUM_ID='ID вашего альбома Вконтакте'
TELEGRAM_TOKEN='Ваш ключ от Телеграм'
TELEGRAM_CHAT_ID='Ваш ID канала Телеграм'
FB_GROUP_ID='ID вашей группы Фейсбук'
FACEBOOK_TOKEN='Ваш ключ от Фейсбук'
SPREADSHEET_ID='1bsdfhkHUKsajsdai799SDSA' ID вашей Google таблицы
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).