from util import *
from gensim.models import Doc2Vec, Word2Vec
from first_model import *
from gensim.models.doc2vec import LabeledSentence

import itertools




def to_gensim_usage(heroes, hero_dict):

    res = []

    for i in range(heroes.shape[0]):
        if i % 10000 == 0:
            print(f'{i} out of ' + str(heroes.shape[0]))
        h = heroes[i]

        a = - h[h < 122] + 122 
        b = h[h > 122] - 122 
        l = list(a) + list(b)

        # r = LabeledSentence(words=[str(pick) for pick in l])
        r = []
        try:
            for p in l:
                if p < 122:
                    r.append(hero_dict[p])
                else:
                    r.append('_' + hero_dict[p - 121])
        except KeyError:
            print(l)
            assert False

        res.append(r)

    return res


#tests : 

def get_heroes_similarities(hero_repr, hero_dict):

    aa = np.zeros(shape=(len(hero_dict.keys()), len(hero_dict.keys())))
    for i, k1 in enumerate(hero_dict.keys()):
        for j, k2 in enumerate(hero_dict.keys()):
            aa[i, j] = hero_repr.similarity(hero_dict[k1], hero_dict[k2])

    return aa

def all_heroes_most_similar(hero_repr, hero_dict):
    for h in hero_dict.values():
        print('========', h, '============')
        print([z[0] for z in hero_repr.most_similar(positive=[h])])


def preprocess_for_keras(heroes, victories):

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


def main():        

    hero_dict = get_hero_dict()

    print('preprocessing data...')  
    heroes, victories = preprocess_data()
    print('numpy array of size : ', heroes.shape)
    print('augmentation...')
    heroes = heroes[:1000]
    victories = victories[:100]
    heroes, victories = to_hero_index_and_augmentation(heroes, victories)
    print('cast to gensim...')
    sentences = to_gensim_usage(heroes, hero_dict)

    print('training w2vec model !')
    model = Word2Vec(sentences, size=1000, window=250, min_count=1, workers=12, iter=10)

    hero_wv = model.wv

    aa = get_heroes_similarities(hero_wv, hero_dict)

    print(aa)
    print(hero_dict)

    all_heroes_most_similar(hero_wv, hero_dict)



    ##======== Anti-Mage ============

    ##['Spectre', 'Weaver', 'Gyrocopter', 'Lifestealer', 'Ursa', 'Chaos Knight', 'Lycan', 'Centaur Warrunner', 'Slark', 'Troll Warlord']
    

if __name__=='__main__':
    # main()
    heroes, victories = preprocess_data()
    preprocess_for_keras(heroes[:1000], victories[:1000])