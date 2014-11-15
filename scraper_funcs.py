from riotwatcher import RiotWatcher, NORTH_AMERICA
import Queue
from collections import defaultdict
import pdb
import time
import json
import numpy as np

key = '9213b085-ed48-4bf0-af91-d8fa519e3b35'

def wait(w):
    while not w.can_make_request():
        time.sleep(1)



def grab_matches(seedid=43731318, num_matches=100):

	'''
	arguments:
	seedid: a summoner_id from which to find games from
	num_matches: number of matches to return

	returns:
	A dictionary with 
	keys: matchid(int) 
	values: tuple[0] dict(keys:int(teamid 100 or 200), values: list of summoner ids for that team)
			tuple[1] teamid of winning team
	'''	




	w = RiotWatcher(key)

	sid_queue = Queue.Queue()
	count = 0

	matches_summoners = {}
	seen_summoners = set()
	seen_summoners.add(seedid)

	while(count < num_matches):

		wait(w)
		m_hist_dict = w.get_match_history(summoner_id=seedid, ranked_queues='RANKED_SOLO_5x5')
		match_list = m_hist_dict['matches']

		# pdb.set_trace()
		for match_record in match_list:
			if match_record['matchMode'] == 'CLASSIC' and match_record['matchType'] == 'MATCHED_GAME':
				matchid = match_record['matchId']
				if matchid not in matches_summoners:
				# use the other API call to get the participants..
					wait(w)
					match = w.get_match(matchid)
					team_summonerids = defaultdict(list)
					ptp_teamId = {}
					for participant in match['participants']:
						ptp_teamId[participant['participantId']] = participant['teamId']

					for ptp_idents in match['participantIdentities']:
						team = ptp_teamId[ptp_idents['participantId']]
						summoner_id = ptp_idents['player']['summonerId']
						team_summonerids[team].append(summoner_id)

						if summoner_id not in seen_summoners:
							sid_queue.put(summoner_id)
							seen_summoners.add(summoner_id)

					for team in match['teams']:
						if team['winner'] is True:
							winning_team = team['teamId']
							break

					matches_summoners[matchid] = (team_summonerids,winning_team)
					print matchid

					count += 1

		# an exception will be thrown if the queue is empty haha
		seedid = sid_queue.get()

	# print matches_summoners

	return matches_summoners

def include_stats(matches_summoners):
	'''
	Replaces list of summonerids (in the returned dictionary from get_matches) 
	with a list of player_stat_summaries as defined in the riot API 
	'''

	w = RiotWatcher(key)

	for matchid, (team_lists,_) in matches_summoners.items():
		print matchid
		for teamid, teamlist in team_lists.items():
			for index, summoner_id in enumerate(teamlist):
				# replace the summonerid with player stat summary
				wait(w)
				wait(w)
				teamlist[index] = w.get_ranked_stats(summoner_id)

	return matches_summoners

def calculate_features(matches_summoners):

	label_mat = []
	feature_mat = []

	for matchid, (team_dict, winner) in matches_summoners.items():

		team100 = team_dict['100']
		feat_100 = featurize_team(team100)
		team200 = team_dict['200']
		feat_200 = featurize_team(team200)

		feat_vect = feat_100 + feat_200

		feature_mat.append(feat_vect)
		if winner == '100':
			label_mat.append(0)
		else:
			label_mat.append(1)

	return (feature_mat, label_mat)

def dump_data(feature_mat, label_mat, seedid=43731318):

	feature_mat = np.array(feature_mat)
	label_mat = np.array(label_mat)

	np.savetxt('X' + str(seedid) +'.csv', feature_mat, delimiter=',')
	np.savetxt('y' + str(seedid) + '.csv', label_mat, delimiter=',')

def featurize_team(team):

	
	features =[ 'totalPhysicalDamageDealt','totalTurretsKilled','totalSessionsPlayed','totalAssists','totalDamageDealt',
				'mostChampionKillsPerSession','totalPentaKills','mostSpellsCast','totalDoubleKills','maxChampionsKilled',
				'totalDeathsPerSession','totalSessionsWon','totalGoldEarned','totalTripleKills','totalChampionKills',
				'maxNumDeaths','totalMinionKills','totalMagicDamageDealt','totalQuadraKills','totalUnrealKills',
				'totalDamageTaken','totalSessionsLost','totalFirstBlood' ]

	feature_set = set(features)

	totals_dict = defaultdict(list)

	for player in team:
		champions_features = defaultdict(list)
		for champion_summary in player['champions']:
			# grab all features
			for feature, value in champion_summary['stats'].items():
				if feature in feature_set:
					champions_features[feature].append(value)

				
		# do some processing
		player_features = {}
		for feature, lest in champions_features.items():

			if feature != 'totalSessionsPlayed' or feature != 'mostChampionKillsPerSession' or \
				feature != 'maxNumDeaths':
				#aggregate over champions, divide by number of sessions
				player_features[feature] = float(sum(lest)) / sum(champions_features['totalSessionsPlayed'])
			elif feature == 'totalSessionsPlayed':
				#simply store
				player_features[feature] = sum(champions_features['totalSessionsPlayed'])
			else:
				#divide by the number of champions
				player_features[feature] = float(sum(lest)) / len(lest)

		for feature, value in player_features.items():

			totals_dict[feature].append(value)

	# now average the list for each feature in totals_dict

	for feature, lest in totals_dict.items():
		totals_dict[feature] = float(sum(lest)) / len(lest)


	feature_list = [x[1] for x in sorted(totals_dict.items())]
	# pdb.set_trace()

	return feature_list


if __name__ == "__main__":
	seedid = 43731318
	matches = grab_matches(seedid=seedid, num_matches=100)

	matches = include_stats(matches)

	with open('data' + str(seedid) + '.json','w') as fp:
		json.dump(matches,fp)

	feat,label calculate_features(matches)
	dump_data(feat,label,seedid=seedid)
	

















