import traceback

import dota2api
import numpy as np
import time
import pickle
from dota2api.src.exceptions import APIError

api_file = "cle steam api.txt"

api_key = ""
with open(api_file, "r") as f:
    api_key = f.readline()

api = dota2api.Initialise(api_key)
hist = api.get_match_history(account_id=120062110)
hist2 = api.get_match_history()
match = api.get_match_details(match_id=3562464902)
heroes = api.get_heroes()
print(match['radiant_win'])
print(len(hist))
time.sleep(1)
# test
hist3 = api.get_match_history_by_seq_num(start_at_match_id='3562464902')
hist4 = api.get_match_history_by_seq_num()#start_at_match_id='3562464902')


def getValidMatchListId(hist):
    r = []
    for match in hist['matches']:
        r.append(match['match_id'])
    return r


def heroVectfromMatch(match):
    players = match['players']
    vect = np.zeros((120))
    for player in players:
        id = player['hero_id']
        res = np.sign(4 - player['player_slot'])
        vect[id] = res
    return vect


v = heroVectfromMatch(match)


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


# charge les détails des matches à rebours de starting Index
def loading_match_routine(index_list, filename):
    l = []
    for index in index_list:
        try:
            m = api.get_match_details(index)
            l.append(m)
        except APIError:
            traceback.print_exc()
        time.sleep(1)
        print(str(len(l)) + " games downloaded (" + str(index) + ")")
    print('saving file...')
    save_object(l, filename + 'pkl')
    return index_list[-1]


matches = getValidMatchListId(hist2)
nextStart = loading_match_routine(matches, "firstBatch")
hist2 = api.get_match_history_by_seq_num(start_at_match_seq_num=nextStart)
matches2 = getValidMatchListId(hist2)
nextS = loading_match_routine(matches2, "secondBatch")

pass
