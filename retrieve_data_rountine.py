import util
import sys

from dota2api.src.exceptions import APIError


def createMatchList(init_seq_num, nb_of_hundreds, verbose=True):
    current_seq_num = init_seq_num
    res = []
    for hundred in range(nb_of_hundreds):
        print(f'{hundred} hundreds out of {nb_of_hundreds} : {current_seq_num}')
        try:
            time.sleep(1)
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
                current_seq_num = res[-1]['match_seq_num'] + 1

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

def main(dirname):

    nb_of_hundreds = 200
    current_seq_num = 3302933279
    current_seq_num = 3251588525
    for i in range(2000):
        try:
            a = current_seq_num
            batch, current_seq_num = createMatchList(current_seq_num, nb_of_hundreds, False)
            print(current_seq_num)
            t = time.strftime("%d_%b_%H:%M", time.gmtime())
            filename = dirname + f'seq_start_{a}_seq_end_{current_seq_num}_nbhundreds{nb_of_hundreds}' + t + '.pkl'
            save_object(batch, filename)
        except APIError:
            traceback.print_exc()
            print(f'Something went wrong on {i}')
            pass


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

if __name__ == '__main__':
    dirname = sys.argv[1]
    main(dirname)