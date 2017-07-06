import sys
import itertools

assert len(sys.argv) > 1

directory = sys.argv[1]
cost_map={
	# category : { cost: set(name, name, ..)}
}

# players that have at least one year of data

qualified_players = {
	# category: set('player names', ...)
}

pc_header = None # generated player combinations file headers
p_headers = None # player cost file headers
#track_unique = set()
unique_score = None
historical_scores = []

def bucket_combo(l, depth=0) :
    ''' return all combinations of items in buckets '''
    for item in l[0] :
        if len(l) > 1 :
            for result in bucket_combo(l[1:], depth+1) :
                yield [item,] + result
        else :
            yield [item,]

def get_team_historical_scores(team, historical_scores):
	scores, player_average_scores = [], {}
	# extrapolate player average from any other available scores
	for player in team:
		total_score, count_scores = 0, 0
		for year in historical_scores:
			if player in year:
				count_scores +=1
				total_score += year[player]
		if count_scores != 0:
			player_average_scores[player] = int(total_score / count_scores)

	for year in historical_scores:
		current_score = 0
		for player in team:
			if player not in year:
				if player in player_average_scores:
					current_score += player_average_scores[player]
				else:
					current_score = ""
					break
			else:
				current_score+=	year[player]
		scores.append(str(current_score))
	return scores

# given a list of players
# and a list of historical scores [{player: score, ..}, {player:score, ..}, ...]
# return a list of players that had the highest score in any year
# in the case of a tie, choose both
# skip players is a list of lists
# each list must contain enough unique items s.t
# by choosing one item from each list, you can create a new list composed of only unique items
def get_best_players(players, skip_players, historical_scores):
	best_players = []
	for year in historical_scores:
		current_score, current_best, current_best_tie = -1, None, []
		for player in players:
			if player not in year:
				continue
			if year[player] > current_score:
				current_best = player
				current_score = year[player]
				current_best_tie = [current_best]
			elif year[player] == current_score:
				current_best_tie.append(player)
		
		best_players = list(set(best_players + current_best_tie))
		
                if best_players in skip_players:
                        current_score, current_best_tie = -1, []
                        for player in players:
                                if player not in year or player in best_players:
                                        continue
                                if year[player] > current_score:
                                        current_best = player
                                        current_score = year[player]
                                        current_best_tie = [current_best]
                                elif year[player] == current_score:
                                        current_best_tie.append(player)
		best_players += current_best_tie
	return list(set(best_players))
		
# given a player cost_combo
# ex 26,16,4,6,4,4,8,8,4,80
# (headers:) All Rounder 1,All Rounder 2,Unclassed Rider 1,Sprinter 1,Unclassed Rider 3,Unclassed Rider 2,Climber 2,Climber 1,Wildcard Rider,TotalPoints
# produce all possible combos of actual players (multiple players can have the same cost)
def get_player_combinations(headers, cost_combo, cost_map, historical_scores):
	global unique_score, track_unique
	i, best_score = 0, -1
	combos = cost_combo.split(',')
	categories = headers.split(',')
	all_avail_players = []
	while i < len(categories):
		cat, cost = categories[i], int(combos[i])
		if cat not in cost_map:
			i+=1
			continue
		if cost not in cost_map[cat]:
			i+=1
			continue
		all_avail_players.append(list(cost_map[cat][cost]))
		i+=1
	
	best_avail_players = []
	for row in all_avail_players:
		best = get_best_players(row, best_avail_players, historical_scores)
		best_avail_players.append(best)

	for combo in bucket_combo(best_avail_players):
		sc = set(combo)
		if len(combo) != len(sc):
			continue
		yield combo

with open(directory+'player_2017.csv') as pl:
	for line in pl:
		if p_headers is None:
			p_headers = line
			continue
		pieces = line.strip('\r\n').split(',')
		if len(pieces) < 3:
			continue	
		category, cost, name = pieces[0], int(pieces[1]), pieces[2]
		if category not in cost_map:
			cost_map[category] = {}
		if cost not in cost_map[category]:
			cost_map[category][cost] = set()
		cost_map[category][cost].add(name)

def get_historical_scores(f):
	scores = {}
	header = None
	for line in f:
		if header is None:
			header = line
			continue	
		if not line:
			continue

		pieces = line.split(',')
		_, total, name = pieces.pop(), int(pieces.pop()), pieces[0]

		if len(pieces) < 4:
			continue
		
		if name not in scores:
			scores[name] = 0
		
		scores[name]+=total

	return scores


with open(directory+'2016.csv') as f, open(directory+'2015.csv') as f2, open(directory+'2014.csv') as f3:
	historical_scores.append(get_historical_scores(f))
	historical_scores.append(get_historical_scores(f2))
	historical_scores.append(get_historical_scores(f3))

	



with open(directory+'cost_combinations.csv') as pc:
	for line in pc:
		line = line.strip('\r\n')
		
		if pc_header is None:
			pc_header = line
			print pc_header, ',2014,', ',2015,', '2016'
			continue
	
		for k in get_player_combinations(pc_header, line, cost_map, historical_scores):
			print ",".join(k)+",", line.split(',').pop(), ',', ",".join(get_team_historical_scores(k, historical_scores))
		





#	
