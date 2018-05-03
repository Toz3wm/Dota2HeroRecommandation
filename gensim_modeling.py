from util import *
from gensim.models import Doc2Vec, Word2Vec
from first_model import *
from gensim.models.doc2vec import LabeledSentence

import itertools
import matplotlib.pyplot as plt


def to_gensim_usage(heroes, hero_dict):

    res = []

    for i in range(heroes.shape[0]):
        if i % 10000 == 0:
            print(f'{i} out of ' + str(heroes.shape[0]))
        h = heroes[i]
        # print(h)
        a = h[0 < h]
        b = h[h < 0]
        l = list(a) + list(b)
        # print('============ h=============', h,)
        # print('============ a=============', a,)
        # print('============ b=============', b,)
        # print('============ l=============', l)
        # r = LabeledSentence(words=[str(pick) for pick in l])
        r = []
        try:
            for p in l:
                if p < 122 and p > 0:
                    r.append(hero_dict[p])
                else:
                    r.append('_' + hero_dict[-p])
        except KeyError:
            print(l)
            assert False

        # print(r)
        res.append(r)

    return res



def to_gensim_usage_with_victories_only(heroes, victories, hero_dict):

    res = []

    for i in range(heroes.shape[0]):
        if i % 10000 == 0:
            print(f'{i} out of ' + str(heroes.shape[0]))
        if not victories[i]:
            continue
        h = heroes[i]
        # print(h)
        a = h[0 < h]
        b = h[h < 0]
        l = list(a) + list(b)
        # print('============ h=============', h,)
        # print('============ a=============', a,)
        # print('============ b=============', b,)
        # print('============ l=============', l)
        # r = LabeledSentence(words=[str(pick) for pick in l])
        r = []
        try:
            for p in l:
                if p < 122 and p > 0:
                    r.append(hero_dict[p])
                else:
                    r.append('_' + hero_dict[-p])
        except KeyError:
            print(l)
            assert False

        # print(r)
        res.append(r)

    return res


#tests : 

def get_heroes_similarities(hero_repr, hero_dict):
    print(hero_dict.keys())
    aa = np.zeros(shape=(len(hero_dict.keys()), len(hero_dict.keys())))
    for i, k1 in enumerate(hero_dict.keys()):
        for j, k2 in enumerate(hero_dict.keys()):
            aa[i, j] = hero_repr.similarity(hero_dict[k1], hero_dict[k2])

    return aa


def all_heroesDIRE_most_similar(hero_repr, hero_dict):
    for h in hero_dict.values():
        h = '_' + h
        print('========', h, '============')
        print([z[0] for z in hero_repr.most_similar(positive=[h], topn=121)])



def all_heroes_most_similar(hero_repr, hero_dict):
    for h in hero_dict.values():
        print('========', h, '============')
        print([z[0] for z in hero_repr.most_similar(positive=[h], topn=121)])


def heroesDIRE_most_similar(hero_repr, hero_dict):
    for h in hero_dict.values():
        if h == 'Anti-Mage':
            h = '_' + h
            print('========', h, '============')
            print([z[0] for z in hero_repr.most_similar(positive=[h], topn=121)])



def heroes_most_similar(hero_repr, hero_dict):
    for h in hero_dict.values():
        if h == 'Anti-Mage':
            print('========', h, '============')
            print([z[0] for z in hero_repr.most_similar(positive=[h], topn=121)])



def get_heroes_representation(heroes, victories):

    hero_dict = get_hero_dict()
    heroes, victories = to_hero_index_and_augmentation(heroes, victories)
    print('cast to gensim...')
    sentences = to_gensim_usage(heroes, hero_dict)

    print('training w2vec model !')
    model = Word2Vec(sentences, size=1000, window=250, min_count=1, workers=12, iter=2)

    hero_wv = model.wv

    heroes_representation = [model.wv[hero_dict[i]] for i in hero_dict.keys()]
    heroes_index = [i for i in hero_dict.keys()]
    return heroes_index, heroes_representation



def preprocess_for_keras(heroes, victories):

    hero_dict = get_hero_dict()
    heroes, victories = to_hero_index_and_augmentation(heroes, victories)
    print('cast to gensim...')
    sentences = to_gensim_usage(heroes, hero_dict)

    print('training w2vec model !')
    model = Word2Vec(sentences, size=1000, window=250, min_count=1, workers=12, iter=2)

    return model, sentences



#the first voc_dim values are for radiant team representation
#the second voc_dim value are for dire team representation
def add_heroes_to_get_team(model, sentences, victories):
    res = []    
    for s in sentences:
        match_representation = np.zeros(2000)
        for h in s:
            if h[0] == '_':
                a = np.concatenate([np.asarray([0] * 1000), model[h]])
            else:
                a = np.concatenate([model[h], np.asarray([0] * 1000)])

            # print(a.shape, match_representation.shape, len(model[h]), len([0]*1000), len([0]*1000 + model[h]))
            # print(type(model[h]))
            match_representation += a
        res.append(match_representation)

    return np.stack(res, axis=0), victories


def get_hero_dict():
    heroes_info = api.get_heroes()['heroes']
    
    print('formating heroes names ... ')
    heroes_names = [h['localized_name'] for h in heroes_info]
    print('formating heroes ids ... ')
    heroes_id = [h['id'] for h in heroes_info]

    hero_dict = {}
    for name, id in zip(heroes_names, heroes_id):
        hero_dict[id] = name
        print(id, name )

    return hero_dict


def get_AM_neighbors():        

    hero_dict = get_hero_dict()

    print('preprocessing data...')  
    heroes, victories = preprocess_data(200000)
    print('numpy array of size : ', heroes.shape)
    print('augmentation...')
    heroes = heroes
    victories = victories

    heroes, victories = to_hero_index_and_augmentation(heroes, victories)
    print('cast to gensim...')
    # sentences = to_gensim_usage(heroes, hero_dict)
    sentences = to_gensim_usage_with_victories_only(heroes, victories, hero_dict)

    print('training w2vec model !')
    model = Word2Vec(sentences, size=1000, window=250, min_count=1, workers=12, iter=10)

    hero_wv = model.wv

    aa = get_heroes_similarities(hero_wv, hero_dict)

    # print(aa)
    # print(hero_dict)

    heroes_most_similar(hero_wv, hero_dict)
    # all_heroesDIRE_most_similar(hero_wv, hero_dict)
    sentences = to_gensim_usage(heroes, hero_dict)

    print('training w2vec model !')
    model = Word2Vec(sentences, size=1000, window=250, min_count=1, workers=12, iter=10)

    hero_wv = model.wv

    aa = get_heroes_similarities(hero_wv, hero_dict)

    # print(aa)
    # print(hero_dict)

    heroes_most_similar(hero_wv, hero_dict)
    # all_heroesDIRE_most_similar(hero_wv, hero_dict)


    ##======== Anti-Mage ============

    ##['Spectre', 'Sven', 'Weaver', 'Gyrocopter', 'Lifestealer', 'Ursa', 'Chaos Knight', 'Lycan', 'Centaur Warrunner', 'Slark']
    

def plot_neighbors_distance(distances):
    print('ploting')
    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    ax1.set_xlabel('neighbor index')
    ax1.set_ylabel('similarity to hero')

    plt.plot(range(len(distances), 0, -1), sorted(distances), 'ro')

    plt.show()

def main():        

    hero_dict = get_hero_dict()

    print('preprocessing data...')  
    heroes, victories = preprocess_data(100000)
    print('numpy array of size : ', heroes.shape)
    print('augmentation...')
    heroes = heroes
    victories = victories

    heroes, victories = to_hero_index_and_augmentation(heroes, victories)
    print('cast to gensim...')
    # sentences = to_gensim_usage(heroes, hero_dict)
    sentences = to_gensim_usage_with_victories_only(heroes, victories, hero_dict)

    print('training w2vec model !')
    model = Word2Vec(sentences, size=1000, window=250, min_count=1, workers=12, iter=10)

    hero_wv = model.wv

    aa = get_heroes_similarities(hero_wv, hero_dict)

    plot_neighbors_distance(aa[0])


if __name__=='__main__':
    main()
    # heroes, victories = preprocess_data()
    # preprocess_for_keras(heroes[:1000], victories[:1000])