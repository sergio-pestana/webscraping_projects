import enum
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://basketball.realgm.com/nba/players/'

page = requests.get(url)
bs = BeautifulSoup(page.text, "lxml")

seasons = []
year_index = []
for option in bs.find('select', class_='ddl').find_all('option'):
    seasons.append(option['value'][-4:])
    year_index.append(option.text)


def get_stats(season, season_type):
    print(f'{season}')
    
    stats_by_pages = []
    for i in range(1, 10):
        url = f'https://basketball.realgm.com/nba/stats/{season}/Totals/Qualified/points/All/desc/{i}/{season_type}'
        
        try:
            stats_by_pages.append(pd.read_html(url)[0])
            print(f'page {i}')
        except ValueError:
            break

    df = pd.concat(stats_by_pages)
    return df 


########### REGULAR SEASON STATS #############

df_list = []
for s, y in zip(seasons[1:], year_index[1:]):
    df = get_stats(s, 'Regular_Season')
    df['Season'] = y
    df_list.append(df)
    print(f"{y} - Finalizado")

regular_season_stats = pd.concat(df_list)
regular_season_stats.to_csv('AllRegularSeasons_stats.csv', index=False)

########### PLAYOFFS STATS #############

df_list = []
for s, y in zip(seasons[1:], year_index[1:]):
    df = get_stats(s, 'Playoffs')
    df['Season'] = y
    df_list.append(df)
    print(f"---- {y} - Finalizado ----")

playoffs_stats = pd.concat(df_list)
playoffs_stats.to_csv('AllPlayoffs_stats.csv', index=False)