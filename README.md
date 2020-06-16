### Mission 1
To get all game names I use infinity loop with `zero_update` cumulative counter, which accumulates on consecutive requests with zero new games

##### To use API
Create API instance with your name
```
api = GamesAPI(username='<name>')
```
Get games with use cache or not
```
api.get_all_games()
# or
api.get_all_games(use_cache=True)
```
Than API instance will contain parsed data
```
print(api.games_json)
```

### Mission 2
To run server use command
```
python app.py
```
Server runs on `http://0.0.0.0:8080/`

For the first load it will parse games via API


### Mission 3
For search add query param `search` to your request
```
http://0.0.0.0:8080/?search=<keyword>
```
