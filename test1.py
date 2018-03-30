import traceback
from sys import getsizeof
import dota2api
import numpy as np
import time
import pickle
import json
from dota2api.src.exceptions import APIError

api_file = "cle_api.txt"

api_key = ""
with open(api_file, "r") as f:
    api_key = f.readline()

print("api initialized")
api = dota2api.Initialise(api_key, logging=False)


# print('get match 3562464902 details')
# match = api.get_match_details(match_id=3562464902)

# l =  3801842558
# match = api.get_match_details(match_id=3801842558)
# print(match)

# print('==========')
# hist = api.get_match_history(account_id=120062110)
# print(match['radiant_win'])
# print(len(hist))


# hist3 = api.get_match_history_by_seq_num(start_at_match_seq_num=3562464902)
# hist4 = api.get_match_history_by_seq_num(start_at_match_seq_num=3791610951)
# hist5 = api.get_match_history_by_seq_num(start_at_match_seq_num=3301896950)
# print(list(hist5))
# exit()
# print(type(hist5))
# print('=============')
# print(list(hist5['matches']))
# print('==== ==== === ==')
# ll = list(hist5['matches'])
# print(ll[2])
# print(len(ll))
# hist5 = api.get_match_history_by_seq_num(start_at_match_seq_num=3791610751)

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    print("saved to " + filename)


current_seq_num = 3300000000
nb_of_hundreds = 100

def createMatchList(init_seq_num, nb_of_hundreds, verbose=True):
    current_seq_num = init_seq_num
    res = []
    for hundred in range(nb_of_hundreds):
        print(f'{hundred} hundreds out of {nb_of_hundreds} : {current_seq_num}')
        try:
            time.sleep(0.1)
            hist = api.get_match_history_by_seq_num(start_at_match_seq_num=current_seq_num)
            status = hist['status']
            if int(status) == 1:
                l = list(hist['matches'])
                if verbose:
                    for m in l:
                        match_id = m['match_id']
                        match_seq_num = m['match_seq_num']
                        duration = m['duration']
                        print(f'match id : {match_id}, match seq num : {match_seq_num}, duration : {duration}')
                res += l
                s = getsizeof(res)
                print(f'Size : {s} bytes')
                current_seq_num = l[-1]['match_seq_num'] + 1

            else:
                current_seq_num += 100
                print(f'\b   something went wrong ({status})')
        except json.decoder.JSONDecodeError:
            print("something went horribly wrong")
            # traceback.print_exc()
            if len(res) == 0:
                current_seq_num += 101
            else:
                current_seq_num = res[-1]['match_seq_num'] + 101
    return res, current_seq_num

for i in range(50):
    try:
        a = current_seq_num
        batch, current_seq_num = createMatchList(current_seq_num, nb_of_hundreds, False)
        print(current_seq_num)
        t = time.strftime("%d_%b_%H:%M", time.gmtime())
        filename = f'seq_start_{a}_seq_end_{current_seq_num}_nbhundreds{nb_of_hundreds}' + t + '.pkl'
        save_object(batch, filename)
    except APIError:
        traceback.print_exc()
        print(f'Something went wrong on {i}')
        pass



def print_list_match(hist):
    list_of_match = list(hist['matches'])
    for m in list_of_match:
        print('====================')
        print(m)
        match_seq_num = m['match_seq_num']
        match_id = m['match_id']
        if 'duration' in m:
            duration = m['duration']
        else:
            duration = 'Not available'
        print(f'match id : {match_id}, match seq num : {match_seq_num}, duration : {duration}')
    print("Total number of matches : ",len(list_of_match))


# print_list_match(hist)
# print_list_match(hist3)
# print('\n'*5)
# print_list_match(hist4)
print('\n'*5)
print_list_match(hist5)

exit()

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

undefinite_parse()



hist2 = api.get_match_history()
matches = getValidMatchListId(hist2)
nextStart = loading_match_routine(matches, "firstBatch")

hist2 = api.get_match_history_by_seq_num(start_at_match_seq_num=nextStart)
matches2 = getValidMatchListId(hist2)
nextS = loading_match_routine(matches2, "secondBatch")

pass
