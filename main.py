import os
from tqdm import trange
from pathlib import Path

if not Path(f'{os.path.expanduser("~")}\\Documents\\Rockstar Games\\GTA V\\User Music').exists():
    print('GTA V не найдена!')
    input()
    exit(0)
print('Привет! Это программа, скачивающая твою любиму музыку с ВК или Яндекс Музыки в радио GTA V!')
while True:
    platform = input('Выбери платформу: vk, ya: ')
    if platform == 'vk' or platform == 'ya':
        print()
        break
    else:
        print('Вы выбрали некорректную платформу, попробуйте еще раз')
if platform == 'ya':
    from yandex_music import Client
    import yandex_music

    print('Требуется получить токен аккаунта. Как это сделать, написано здесь: '
          'https://github.com/MarshalX/yandex-music-api/discussions/513')
    print()
    while True:
        TOKEN = input('Введите токен аккаунта: ')

        # noinspection PyUnresolvedReferences
        try:
            client = Client(TOKEN).init()
            break
        except yandex_music.exceptions.UnauthorizedError:
            print('Неверный токен! Попробуйте еще раз')

    album = client.users_likes_tracks()
    for i in trange(len(album)):
        try:
            track = album[i]
            name = track.fetch_track().filename
            home_directory = os.path.expanduser("~")
            try:
                track.fetch_track().download(name)
                os.replace(name,
                           r'{}\Documents\Rockstar Games\GTA V\User Music\{}'.format(home_directory, name))
            except TypeError:
                name = track.fetch_track().id
                track.fetch_track().download(str(name) + '.mp3')
                os.replace(str(name) + '.mp3',
                           r'{}\Documents\Rockstar Games\GTA V\User Music\{}'.format(home_directory,
                                                                                     str(name) + '.mp3'))
        except:
            pass
    print('''Треки установлены! Чтобы их использовать, нужно: Запустить ГТА, далее зайти в меню “Настройки” (
    Settings). В разделе Audio вы найдете опции “выполнить быстрый поиск музыки” (Perform Quick Scan for Music) и 
    “выполнить расширенный поиск музыки” (Perform Full Scan for Music). После выбора любой из опций в игре появится 
    новая радиостанция.''')
    input()

elif platform == 'vk':
    from vkpymusic import TokenReceiver, Service

    try:
        Service.parse_config()
    except:
        login = input("Введите логин (номер телефона): ")
        password = input("Введите пароль: ")

        tokenReceiver = TokenReceiver(login, password)

        if tokenReceiver.auth():
            tokenReceiver.get_token()
            tokenReceiver.save_to_config()

    service = Service.parse_config()
    while True:
        # TODO сделать получение ID через код в test.py
        print('Чтобы узнать ID аккаунта, зайдите на любую Вашу фотку на странице, и скопируйте число в адресной '
              'строке браузера между «photo» и «_».')
        user_id = input('Введите ваш ID аккаунта: ')
        count = input('Введите желаемое кол-во песен: ')  # TODO Это нахера вообще??
        try:
            user_songs = service.get_songs_by_userid(user_id, count)
            break
        except:
            print('Неверный ID или пароль от аккаунта, попробуйте еще раз')
    for i in trange(len(user_songs)):
        track = user_songs[i]
        Service.save_music(track)
    root, _, files = tuple(os.walk('./Music'))[0]
    home_directory = os.path.expanduser("~")
    for name in files:
        path = os.path.join(root, name)
        os.replace(path, r'{}\Documents\Rockstar Games\GTA V\User Music\{}'.format(home_directory, name))
    print()
    print('''Треки установлены! Чтобы их использовать, нужно: Запустить ГТА, далее зайти в меню “Настройки” (
Settings). В разделе Audio вы найдете опции “выполнить быстрый поиск музыки” (Perform Quick Scan for Music) и 
“выполнить расширенный поиск музыки” (Perform Full Scan for Music). После выбора любой из опций в игре появится 
новая радиостанция.''')
    input()
