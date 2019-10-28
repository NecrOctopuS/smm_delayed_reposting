import os
from dotenv import load_dotenv
import vk_api
import requests
import telegram
import argparse


def post_telegram(image_path, text_path):
    with open(text_path, 'rt', encoding='utf-8') as file:
        text = file.read()
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    token = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=token)
    if image_path:
        bot.send_message(chat_id=chat_id, text=text)
    if text_path:
        bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'))


def post_facebook(image_path, text_path):
    if text_path:
        with open(text_path, 'rt', encoding='utf-8') as file:
            text = file.read()
    else:
        text = ''
    group_id = os.getenv('FB_GROUP_ID')
    facebook_token = os.getenv('FACEBOOK_TOKEN')
    if image_path:
        upload_url = f'https://graph.facebook.com/{group_id}/photos'
        params_upload = {
            "caption": text,
            'access_token': facebook_token
        }
        with open(image_path, 'rb') as file:
            files = {
                'photo': file,
            }
            response = requests.post(upload_url, files=files, params=params_upload)
            response.raise_for_status()
    else:
        upload_url = f'https://graph.facebook.com/{group_id}/feed'
        params_upload = {
            "message": text,
            'access_token': facebook_token
        }
        response = requests.post(upload_url, params=params_upload)
        response.raise_for_status()


def post_vkontakte(image_path, text_path):
    if text_path:
        with open(text_path, 'rt', encoding='utf-8') as file:
            text = file.read()
    else:
        text = ''
    access_vk_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = int(os.getenv('VK_GROUP_ID'))
    album_id = os.getenv('VK_ALBUM_ID')
    vk_session = vk_api.VkApi(login=None, password=None, token=access_vk_token)
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    if image_path:
        photo = upload.photo(
            image_path,
            album_id=album_id,
            group_id=group_id
        )
        vk_photo = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    if image_path:
        vk.wall.post(owner_id=f'-{group_id}', message=text, attachments=vk_photo)
    else:
        vk.wall.post(owner_id=f'-{group_id}', message=text)


def create_parser():
    parser = argparse.ArgumentParser(description='Публикация постов в Вконтакте, Фейсбук и Телеграм')
    parser.add_argument('image_path', help='путь до файла')
    parser.add_argument('text_path', help='путь до текста')
    return parser


def main():
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()
    post_vkontakte(args.image_path, args.text_path)
    post_telegram(args.image_path, args.text_path)
    post_facebook(args.image_path, args.text_path)
    try:
        post_facebook(args.image_path, args.text_path)
    except requests.exceptions.HTTPError as error:
        print(error.response.json()['error']['error_user_msg'])


if __name__ == '__main__':
    main()
