import json
from pprint import pprint

import requests

username = "Daeronel"


# получаем информацию о репозиториях пользователя
def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


# сохраняем в отдельном json-файле
def save_repos_info(repos_info, username):
    path = f"{username}.json"
    with open(path, "w") as f:
        json.dump(repos_info, f)


# выполняем обе функции
def main(username):
    repos_info = get_repos(username)
    pprint(repos_info)
    print()
    save_repos_info(repos_info, username)


if __name__ == "__main__":
    main(username)
