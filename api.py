import json
import os
import time

import requests


class GamesAPI:
    """ API parse games for test """

    url_template: str = 'http://www.magetic.com/c/test?api=1&name={}'
    delimiter: str = ';'
    max_zero_update: int = 50
    filename: str = 'games.json'

    def __init__(self, username: str):
        self.games = set()
        self.games_json = dict()
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

    def get_all_games(self, use_cache: bool = False):
        """ get all games with use_cache or not """
        if use_cache and os.path.exists(self.filename):
            self.load_from_file()
        else:
            self.get_from_api()
            self.save_to_file()

    def get_from_api(self):
        """ parse all available game names from api """
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

        self.games_json = self.to_json()

    def to_json(self):
        """ generate games json """
        return [dict(
            gamename=gamename,
            number=i
        ) for i, gamename in enumerate(self.games, 1)]

    def save_to_file(self):
        """ save games to file """
        with open(self.filename, 'w') as f:
            json.dump(api.games_json, f, indent=4)

    def load_from_file(self):
        """ load games from file """
        with open(self.filename, 'r') as f:
            data = json.load(f)
            self.games = {game.get('gamename') for game in data}
            self.games_json = data


if __name__ == '__main__':
    api = GamesAPI(username='taras_kolomoets')
    api.get_all_games(use_cache=False)
    print(api.games_json)
