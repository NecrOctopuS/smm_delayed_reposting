### Delayed reposting in social networks
The program publishes a post (picture and text) in three social networks:
1. [VKontakte](https://vk.com/)
2. [Telegram](https://telegram.org/)
3. [Facebook](https://www.facebook.com/)
Program publishes posts according to the schedule in a Google table of this kind [link](https://docs.google.com/spreadsheets/d/17r4QRW_m0clut772bRnUL-U1-JiazImiZMm43SkgS9Q/edit)

### How to install
To get started, get a token from VK, it can be obtained as follows:

You must follow the link: https://oauth.vk.com/authorize?client_id=`Your_ID_client`&scope=photos,groups,wall,offline&response_type=token
where `Your_ID_ID` is the application ID that can be viewed in the settings of your [application](https://vk.com/apps?act=manage)

Next, you need to get a token from Telegram, you get it automatically by creating a bot.

You also need a key (access token) with the right to `publish_to_groups` from Facebook, you can get it by following the [link](https://developers.facebook.com/tools/explorer/)
 
The following data must be written to the `.env` file:
```text
VK_ACCESS_TOKEN = "Your key to Vkontakte"
VK_CLIENT_ID = 'Your Vkontakte Application ID'
VK_GROUP_ID = 'ID of your VKontakte group'
VK_ALBUM_ID = 'ID of your Vkontakte album'
TELEGRAM_TOKEN = 'Your Telegram Key'
TELEGRAM_CHAT_ID = 'Your Telegram Channel ID'
FB_GROUP_ID = 'Your Facebook Group ID'
FACEBOOK_TOKEN = 'Your Facebook Key'
SPREADSHEET_ID='1bsdfhkHUKsajsdai799SDSA' ID of your Google spreadsheet
```

Python3 should already be installed.
Then use `pip` (or` pip3`, there is a conflict with Python2) to install the dependencies:
```
pip install -r requirements.txt
```


### Objective of the project

The code is written for educational purposes on the online course for web developers [dvmn.org](https://dvmn.org/).