import time
import pickle
import json
import sys
import os
import traceback
from sys import getsizeof


import dota2api
import numpy as np
from dota2api.src.exceptions import APIError

api_file = "cle_api.txt"

api_key = ""
with open(api_file, "r") as f:
    api_key = f.readline()

print("api initialized")
api = dota2api.Initialise(api_key, logging=False)




def gather_data_from_npy():
    l = sorted(os.listdir('data/'))
    l_h = ['data/' + f for f in l if 'picks' in f]
    l_r = ['data/' + f for f in l if 'results' in f]
    heroes = [np.load(l) for l in l_h]
    victories = [np.load(l) for l in l_r]

    heroes = np.concatenate(heroes)    
    victories = np.concatenate(victories)    
    return heroes, victories



def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    print("saved to " + filename)

def load_object(filename):
    with open(filename, 'rb') as the_file:
        data = pickle.load(the_file)
        return data 


def print_hist_match(hist):
    list_of_match = list(hist['matches'])
    print_list_match(list_of_match)


def print_list_match(list_of_match):
    for m in list_of_match:
        match_seq_num = m['match_seq_num']
        match_id = m['match_id']
        if 'duration' in m:
            duration = m['duration']
        else:
            duration = 'Not available'
        print(f'match id : {match_id}, match seq num : {match_seq_num}, duration : {duration}')
    print("Total number of matches : ",len(list_of_match))


# charge les détails des matches à rebours de starting Index
def loading_match_routine(index_list, filename):
    l = []
    for index in index_list:
        try:
            m = api.get_match_details(index)
            l.append(m)
            if 'duration' in m:
                duration = m['duration']
            else:
                duration = 'Not available'
            print(str(len(l)) + " games downloaded (" + str(index) + ", duration {})".format(duration))
        except APIError:
            pass
            # traceback.print_exc()
        except APITimeoutError:
            
            traceback.print_exc()
        except Error:
            pass

        time.sleep(0.01)
        
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

