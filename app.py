import json
import time

import requests


class API:
    """ API parse games for test """

    url_template: str = 'http://www.magetic.com/c/test?api=1&name={}'
    delimiter: str = ';'
    max_zero_update: int = 50

    def __init__(self, username: str):
        self.games = set()
        self.url = self.url_template.format(username)

    @property
    def games_count(self):
        """ return count of games in instance """
        return len(self.games)

    def get(self):
        """ send get request and validate status code. return response object """
        while True:
            response = requests.get(self.url)
            if response.status_code == 200:
                break
            time.sleep(1)

        return response

    def get_games(self):
        """ get text response, validate for error and parse data. return set of game names """
        while True:
            response = self.get()
            data = response.text
            if 'error' not in data.lower():
                break

        data = data.split(self.delimiter)
        data = set(filter(None, data))

        return data

    def get_all_games(self):
        """ parse all available game names """
        i = 0
        zero_update = 0
        print(f'start. parse all games')
        while True:
            i += 1

            games = self.get_games()

            """ get difference with current games set """
            new_games = games.difference(self.games)
            new_games_count = len(new_games)

            """ if have new games add to current games set """
            if new_games:
                self.games.update(new_games)

            """ check zero updates by cumulative counter """
            if new_games_count == 0:
                zero_update += 1
            else:
                zero_update = 0

            print(f'iteration: {i: <3} | new games: {new_games_count: <2} | zero update: {zero_update: <2}')

            """ if counter reaches a maximum, break loop """
            if zero_update > self.max_zero_update:
                print(f'finish. all games count: {self.games_count}')
                break

    def to_json(self):
        return [dict(
            gamename=gamename,
            number=i
        ) for i, gamename in enumerate(self.games, 1)]


if __name__ == '__main__':
    api = API(username='taras_kolomoets')
    api.get_all_games()

    with open('games.json', 'w') as f:
        json.dump(api.to_json(), f, indent=4)
