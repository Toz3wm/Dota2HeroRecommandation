from test1 import *
import os
import time




def heroVectfromMatch(match):
    players = match['players']
    vect = np.zeros((121))
    for player in players:
        id = player['hero_id']
        res = int(np.sign(4.5 - player['player_slot']))
        vect[id] = res
    return vect.astype('int')

def hero_list_from_vect(hlist, d):
    l = [] 
    for i, v in enumerate(hlist):
        if v == 1:
            l = [i] + l
        elif v == -1:
            l.append(i)
        else:
            pass
    print(readable_herolist(l, d))


def radiant_victory(match):
    return int(match['radiant_win'])

def radiant_victories(list_of_matches):
    return np.asarray([radiant_victory(m) for m in list_of_matches])

def from_dict_to_vect(list_of_matches):
    hero_picks = [heroVectfromMatch(match) for match in list_of_matches]
    victories = radiant_victories(list_of_matches)
    v = np.stack(hero_picks, axis=0)
    return v, victories

def build_hero_dict(hdict):
    l = {}
    for hero in hdict:
        l[int(hero['id'])] = hero['localized_name']
    return l

def readable_herolist(hlist, hdict):
    return [hdict[h] for h in hlist]


list1 = load_object('seq_start_3302283311_seq_end_3302286396_nbhundreds10027_Mar_13:30.pkl')

# print_list_match(list1)

print(list1[0])

heroes = api.get_heroes()
d = build_hero_dict(heroes['heroes'])
print(d)


# v = from_dict_to_vect(list1[:10])

# print(v)
print(d)
# hero_list_from_vect(v[0][0], d)
print(readable_herolist([1, 55, 87], d))
# todo : class match pour stocker les infos

def prune_match_list(match_list):
    res = []
    for match in match_list:
        if match['human_players'] != 10:
            continue
        if match['game_mode'] != 22:
            continue

        res.append(match)
    return res 


def build_numpy_data():
    l = sorted(os.listdir())
    l = [v for v in l if '.pkl' in v]
    res_h, res_v = ([], [])
    for batch in l:
        print('processing batch :', batch)
        match_list = load_object(batch)
        print('batch ranging from : ', time.gmtime(match_list[0]['start_time']))
        pruned_match_list = prune_match_list(match_list)
        print(len(match_list), len(pruned_match_list))
        hero_vect, vict_vect = from_dict_to_vect(pruned_match_list)
        print(hero_vect.shape)
        print(vict_vect.shape)
        res_h.append(hero_vect)
        res_v.append(vict_vect)

    print(len(res_h))
    print(len(res_v))
    heroes = np.concatenate(res_h, axis=0)
    victories = np.concatenate(res_v, axis=0)
    print(heroes.shape)
    print(victories.shape)
    print('total number of matches : ', np.sum(victories))

    np.save('picks', heroes)
    np.save('results', victories)

    print(heroes)
    print(victories)


def get_avg_winrate(hero_id, matches, victories):
    matches = matches[:, hero_id]
    radiant_v = np.sum(victories[matches == 1])
    dire_v = np.sum(1 - victories[matches == -1])
    total = np.sum(np.abs(matches))
    print(radiant_v, dire_v, total)
    return (radiant_v + dire_v) / total, total




def main():
    heroes = np.load('picks.npy')
    victories = np.load('results.npy')
    for i in range(0, 121):
        if i in [0, 24, 115, 116, 117, 118]:
            continue
        z = get_avg_winrate(i, heroes, victories)
        h = readable_herolist([i], d)[0]
        f = h + ' ' * (20-len(h)) + 'Winrate : {:2f}, total number of matches : {}'.format(z[0]*100, z[1])
        print(f)


if __name__ == '__main__':
    build_numpy_data()
    main()  



