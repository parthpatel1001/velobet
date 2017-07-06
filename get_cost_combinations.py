import sys
import itertools



"""
python get_cost_combinations.py ~/velobet/player_2017.csv.bak

gets all the different combinations of teams that add up to 100 or less points

TODO optimize get_combinations
	no need to allocate that list in memory, yield each row and build the sorted list later
"""

assert len(sys.argv) > 1

file_loc = sys.argv[1]
columns = None
# 2 All Rounder
# 2 Climbers
# 1 Sprinter
# 3 Unclassified
# 1 WildCard
cost_map = {
	# category : [cost1, cost2...]
}
cost_counts = { 
	# cost : count
}
max_points = 100

with open(file_loc) as file:
	for line in file:
		if columns is None:
			columns = line
		else:
			pieces = line.strip('\r\n').split(',')
		#	print pieces
			if not pieces or len(pieces) < 4:
				continue
			category, cost = pieces[0], int(pieces[1])

			if category not in cost_map:
				cost_map[category] = []
			cost_map[category].append(cost)

rows_unique = [(key, set(row)) for (key, row) in cost_map.iteritems()]
cost_counts = { cost : row.count(cost) for cost in cost_map['Wildcard Rider']}

#for row in rows_unique:
#	print row


def filter_combination(combination):
	# check if sum of costs is within acceptable range
	if sum(combination) > max_points or sum(combination) < 80:
		return False
	# make sure given combination is valid
	# compare against global cost counts
	# the count of the costs represents how many players are available for the given cost
	c_counts = {cost : combination.count(cost) for cost in combination}
	for (cost, count) in c_counts.iteritems():
		if cost not in cost_counts or count > cost_counts[cost]:
			return False
	return True
def sort_combinations(a, b):
	sa, sb = sum(a), sum(b)
	if sa < sb:
		return -1
	if sa == sb:
		return 0
	return 1
def get_combinations(rows):
	return filter(filter_combination, list(itertools.product(*[row for (_, row) in rows])))

cmbs = get_combinations(rows_unique)
cmbs.sort(sort_combinations, reverse=True)

out = ""
for (label, _) in rows_unique:
	out += label + ","
print out + "TotalPoints"

for r in cmbs:
	out = ""
	for i in r:
		out += str(i) + ","
	out += str(sum(r))
	print out






		
	
	
