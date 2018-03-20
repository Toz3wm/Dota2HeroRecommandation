import traceback

import dota2api
import numpy as np
import time
import pickle
from dota2api.src.exceptions import APIError

api_file = "cle_api.txt"

api_key = ""
with open(api_file, "r") as f:
    api_key = f.readline()

print("api initialized")
api = dota2api.Initialise(api_key)


print('get match 3562464902 details')
match = api.get_match_details(match_id=3562464902)

# print(heroes)
time.sleep(1)
hist = api.get_match_history(account_id=120062110)
time.sleep(1)
hist5 = api.get_match_history(matches_requested='1000')

print(match['radiant_win'])
print(len(hist))

# hist3 = api.get_match_history_by_seq_num(start_at_match_id='3562464902')
# hist4 = api.get_match_history_by_seq_num()




def print_list_match(hist):
    list_of_match = list(hist['matches'])
    for m in list_of_match:
        id_ = m['match_id']
        seq_num = m['match_id']
        if 'duration' in m:
            duration = m['duration']
        else:
            duration = 'Not available'
        print(f'match id : {id_}, match seq num : {seq_num}, duration : {duration}')
    print("Total number of matches : ",len(list_of_match))


# print_list_match(hist)
# print_list_match(hist5)
# print_list_match(hist3)
# print_list_match(hist4)

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
            print(str(len(l)) + " games downloaded (" + str(index) + ")")
        except APIError:
            pass
            # traceback.print_exc()
        except APITimeoutError:
            
            traceback.print_exc()
        except Error:
            pass

        time.sleep(1.2)
        
    print('saving file...')
    t = time.strftime("%d_%b_%H:%M", time.gmtime())
    save_object(l, filename + str(t) + '.pkl')
    return index_list[-1]


def undefinite_parse():
    i = 0
    start = 3791610953
    size = 10000
    while True:
        print('Batch n° ', i)

        inde = list(range(start, start-size, -1))
        filename = 'batch_{i}_size{size}'
        loading_match_routine(inde, filename)
        start = start-size
        i += 1

undefinite_parse()



hist2 = api.get_match_history()
matches = getValidMatchListId(hist2)
nextStart = loading_match_routine(matches, "firstBatch")

hist2 = api.get_match_history_by_seq_num(start_at_match_seq_num=nextStart)
matches2 = getValidMatchListId(hist2)
nextS = loading_match_routine(matches2, "secondBatch")

pass
