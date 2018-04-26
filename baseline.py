import os
import sys

from test1 import *
from test2 import *


def baseline(heroes_train, victories_train, heroes_val, victories_val, d):   
    winrates = np.zeros(heroes_train.shape[1])

    for i in range(0, 121):
        if i in [0, 24, 115, 116, 117, 118]:
            continue
        z = get_avg_winrate(i, heroes_train, victories_train)
        winrate = z[0]
        nb_gqmes = z[1]
        winrates[i] = winrate
        h = readable_herolist([i], d)[0]
        f = h + ' ' * (20-len(h)) + 'Winrate : {:2f}, total number of matches : {}'.format(z[0]*100, z[1])
        print(f)

    print(winrates)
    winrated_picks = heroes_val * np.asarray(winrates)
    print(winrated_picks[:10])
    winrated_picks = np.sum(winrated_picks, axis=1)
    print(winrated_picks[:10])

    results = np.zeros(heroes_val.shape[0])
    results[winrated_picks > 0] = 1

    avg_precision = np.sum(results == victories_val) / victories_val.shape[0]
    return avg_precision

def main():
    heroes_info = api.get_heroes()
    d = build_hero_dict(heroes_info['heroes'])
    print(d)

    heroes, victories = gather_data_from_npy()

    heroes_train = heroes[:int(heroes.shape[0] * 0.8)]
    victories_train = victories[:int(heroes.shape[0] * 0.8)]
    heroes_val = heroes[int(heroes.shape[0] * 0.8):]
    victories_val = victories[int(heroes.shape[0] * 0.8):]

    avg_precision_train = baseline(heroes_train, victories_train, heroes_train, victories_train, d)
    avg_precision_val = baseline(heroes_train, victories_train, heroes_val, victories_val, d)
    print(heroes.shape, victories.shape)
    print(heroes_train.shape, victories_train.shape)
    print(heroes_val.shape, victories_val.shape)

    print("average precision on training set of baseline on {} games : {:4f}".format(victories_train.shape[0], avg_precision_train))
    print("average precision on testing set of baseline on {} games : {:4f}".format(victories_val.shape[0], avg_precision_val))

if __name__ == '__main__':
    main()  

