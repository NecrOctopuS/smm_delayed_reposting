from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import re
from dotenv import load_dotenv
import requests
import reposting
import datetime
import time
import os


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
RANGE_NAME = 'Лист1!A3:H'
WEEKDAYS = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]


def string_to_bool(string):
    return string.lower() == 'да'


def string_to_int(string):
    for index, weekday in enumerate(WEEKDAYS):
        if string == weekday:
            return index


def get_schedule_from_values(values):
    publication_schedule = []
    for row in values:
        text_id = re.search(r'id=(.*?)(\"|$).*?', row[5])
        if text_id:
            text_id = text_id.group(1)
        photo_id = re.search(r'id=(.*?)(\"|$).*?', row[6])
        if photo_id:
            photo_id = photo_id.group(1)
        publication = {
            'VK': string_to_bool(row[0]),
            'Telegram': string_to_bool(row[1]),
            'Facebook': string_to_bool(row[2]),
            'public_day': string_to_int(row[3]),
            'public_time': row[4],
            'text_id': text_id,
            'photo_id': photo_id,
            'was_published': string_to_bool(row[7])
        }
        publication_schedule.append(publication)
    return publication_schedule


def get_publication_schedule(spreadsheet_id):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=RANGE_NAME, valueRenderOption='FORMULA').execute()
    values = result.get('values', [])
    return get_schedule_from_values(values)


def update_schedule(index, spreadsheet_id):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    values = [
        [
            'да'
        ],
    ]
    body = {
        'values': values
    }
    range = f'Лист1!H{index + 3}'
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range,
        valueInputOption='RAW', body=body).execute()


def can_post(publication):
    now = datetime.datetime.now()
    return not publication['was_published'] and \
           publication['public_day'] == now.weekday() and \
           publication['public_time'] == now.hour


def get_text(publication, drive):
    file = drive.CreateFile(({'id': publication['text_id']}))
    file.FetchMetadata(fetch_all=True)
    text_path = f'{file["title"]}.txt'
    file.GetContentFile(text_path, 'text/plain')
    return text_path


def get_image(publication, drive):
    file = drive.CreateFile({'id': publication['photo_id']})
    file.FetchMetadata(fetch_all=True)
    image_path = file['originalFilename']
    file.GetContentFile(image_path)
    return image_path


def publish_post(publication, drive):
    if publication['text_id'] and publication['photo_id']:
        image_path = get_image(publication, drive)
        text_path = get_text(publication, drive)
    elif publication['text_id']:
        image_path = ''
        text_path = get_text(publication, drive)
    elif publication['photo_id']:
        image_path = get_image(publication, drive)
        text_path = ''
    if publication['VK']:
        reposting.post_vkontakte(image_path, text_path)
    if publication['Telegram']:
        reposting.post_telegram(image_path, text_path)
    if publication['Facebook']:
        reposting.post_facebook(image_path, text_path)
    if image_path:
        os.remove(image_path)
    if text_path:
        os.remove(text_path)


def main():
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    load_dotenv()
    while True:
        publication_schedule = get_publication_schedule(spreadsheet_id)
        for index, publication in enumerate(publication_schedule):
            if can_post(publication):
                try:
                    gauth = GoogleAuth()
                    drive = GoogleDrive(gauth)
                    publish_post(publication, drive)
                except requests.exceptions.HTTPError as error:
                    print(error.response.json()['error']['error_user_msg'])
                update_schedule(index, spreadsheet_id)
        time.sleep(300)


if __name__ == '__main__':
    main()
