from riotwatcher import RiotWatcher, NORTH_AMERICA
import Queue
from collections import defaultdict
import pdb
import time

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
	values: dict(keys:int(teamid 100 or 200), values: list of summoner ids for that team)
	'''



	key = '9213b085-ed48-4bf0-af91-d8fa519e3b35'
	w = RiotWatcher(key)

	sid_queue = Queue.Queue()

	num_matchIds = 20
	count = 0

	matches_summoners = {}
	seen_summoners = set()
	seen_summoners.add(seedid)

	while(count < num_matchIds):
		if (w.can_make_request()):

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

						matches_summoners[matchid] = team_summonerids

						count += 1

		# an exception will be thrown if the queue is empty haha
		seedid = sid_queue.get()

	# print matches_summoners

	return matches_summoners


if __name__ == "__main__":
	grab_matches()