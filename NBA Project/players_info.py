from operator import index
from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://basketball.realgm.com/nba/players/'

page = requests.get(url)
bs = BeautifulSoup(page.text, "lxml")

seasons = []
year_index = []
for option in bs.find('select', class_='ddl').find_all('option'):
    seasons.append(option['value'])
    year_index.append(option.text)

dfs_players_by_season = []
for s in seasons[1:]:
    url = 'https://basketball.realgm.com' + s
    df = pd.read_html(url)[0]
    dfs_players_by_season.append(pd.read_html(url)[0])

complete_df = pd.concat(dfs_players_by_season)
complete_df.drop_duplicates(inplace=True)

complete_df.to_csv('AllPlayers_info.csv', index=False)

