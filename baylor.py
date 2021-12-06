import csv
import requests
from bs4 import BeautifulSoup

team_image_ids = [
  {'team': 'Baylor', 'value': '239'},
  {'team': 'Arkansas PB', 'value': '2029'}
]


def get_teamname_by_image_url(url):
  id = url.split('https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/')[1].split('.png')[0]
  if id == team_image_ids[0]['value']:
    return team_image_ids[0]['team']
  return team_image_ids[1]['team']


def main(gameID, file_name):
  html = requests.get(f'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/{gameID}')
  soup = BeautifulSoup(html.text, 'html.parser')
  half_num = 1
  pbp = []
  for half in soup.findAll('div', {'class': 'accordion-content'}):
    pbp_table = half.find('table')
    # If the accordion div has a nested table
    if pbp_table:
      # Skip the header row
      for row in pbp_table.findAll('tr')[1:]:
        columns = row.findAll('td')
        
        # COLUMNS: time, team, event, score (away - home)
        timestamp = columns[0].get_text()
        team = get_teamname_by_image_url(columns[1].img.get('src'))
        event = columns[2].get_text()
        score = columns[3].get_text().split(' - ')
        away_score = score[0]
        home_score = score[1]
        pbp.append({
          'half': half_num,
          'time': timestamp,
          'team': team,
          'event': event,
          'away_score': away_score,
          'home_score': home_score
        })
      half_num += 1
  keys = pbp[0].keys()

  with open(file_name, 'w', newline='') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(pbp)


if __name__ == '__main__':
  main(401371981, '20211204-UAPBatBAY.csv')