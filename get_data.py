import mechanize
from bs4 import BeautifulSoup
import sys

assert len(sys.argv) > 1
year = sys.argv[1]

base_url = 'https://www.velogames.com/tour-de-france/'
all_players = base_url + year + '/ridescore.php'
player_base = base_url + year + '/'

columns = [
	'PlayerName',
	'Year',
	'Stage',
	'STG',
	'GC',
	'PC',
	'KOM',
	'SPR',
	'SUM',
	'BKY',
	'ASS',
	'Total'
] # in order player stat columns


br = mechanize.Browser()
# ignore robots.txt
br.set_handle_robots(False)
# pretend to be mozilla
br.addheaders = [("User-agent","Mozilla/5.0")] 

# get the markup for the all players page
response = br.open(all_players)

assert response.code == 200

# get all the links for each players page
soup = BeautifulSoup(response.read(), 'html.parser')
player_links = [(link.get('href'),link.getText()) for link in soup.find_all('a') if 'riderprofile.php' in link.get('href')]

# go to each players page and retreive all the stage stats
for (player_link, player_name) in player_links:
	response = br.open(player_base + player_link)
	soup = BeautifulSoup(response.read(), 'html.parser')
	for tr in soup.find_all('tr'):
		row = player_name + ',' + year + ','
		for td in tr.find_all('td'):
			row += td.getText().strip('\r\n') + ','
		print row.encode('ascii', 'ignore')




