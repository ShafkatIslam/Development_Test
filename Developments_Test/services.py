import requests


def get_info():
    url = 'https://jsonplaceholder.typicode.com/posts'
    r = requests.get(url)
    info = r.json()
    info_list = {'info': info}
    print(info_list)
    return info_list