from riotwatcher import RiotWatcher, NORTH_AMERICA
import Queue
from collections import defaultdict
import pdb
import time
import json

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
		for teamid, teamlist in team_lists.items():
			for index, summoner_id in enumerate(teamlist):
				# replace the summonerid with player stat summary
				wait(w)
				teamlist[index] = w.get_ranked_stats(summoner_id)

	return matches_summoners

def calculate_features(matches_summoners):

	for matchid, (team_list, winner) in matches_summoners.items():

		for teamid, team in team_list.items():
			stat_list = featurize_team(team):





def featurize_team(team):

	features =[ 'botGamesPlayed', 'killingSpree', 'normalGamesPlayed','rankedPremadeGamesPlayed','rankedSoloGamesPlayed',
			   'totalAssists','totalChampionKills','totalDamageDealt','totalDamageTaken','totalGoldEarned',
			   'totalHeal''totalFirstBlood','totalMinionKills','totalNeutralMinionsKilled','totalPhysicalDamageDealt',
			   'totalMagicDamageDealt','totalPentaKills','totalTurretsKilled', 'totalSessionsPlayed','totalSessionsWon',
			   'totalSessionsLost' ]

	totals_dict = defaultdict(list)

	for player in team:
		player_features = defaultdict(int)
		for champion_summary in stat_summary['champions']:
			# grab all features
			for feature, value in champion_summary.items():
				player_features[feature] += value
				totals_dict[feature] += value

	# now average the list for each feature in totals_dict

	for feature, lest in totals_dict:
		totals_dict[feature] = float(sum(lest)) / len(lest)

	







if __name__ == "__main__":

	matches = grab_matches(num_matches=10)

	matches = include_stats(matches)

	with open('data.json','w') as fp:
		json.dump(matches,fp)

















