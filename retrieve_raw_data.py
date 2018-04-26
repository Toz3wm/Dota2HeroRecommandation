import sys
import util
import json
import time


from dota2api.src.exceptions import APIError


def createMatchList(init_seq_num, nb_of_hundreds, verbose=True):
    current_seq_num = init_seq_num
    res = []
    for hundred in range(nb_of_hundreds):
        print(f'{hundred} hundreds out of {nb_of_hundreds} : {current_seq_num}')
        try:
            time.sleep(1)
            hist = util.api.get_match_history_by_seq_num(start_at_match_seq_num=current_seq_num)
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
                s = sys.getsizeof(res)
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



def main(dirname, starting_seq_num, nb_of_seq):

    nb_of_hundreds_by_seq = 200

    current_seq_num = starting_seq_num
    #those are currents limits parsed (up to for the first, end of last batch for second)
    # current_seq_num = 3302933279
    # current_seq_num = 3251588525

    for i in range(nb_of_seq):
        try:
            a = current_seq_num
            batch, current_seq_num = createMatchList(current_seq_num, nb_of_hundreds_by_seq, False)
            print(current_seq_num)
            t = time.strftime("%d_%b_%H:%M", time.gmtime())
            filename = dirname + f'/seq_start_{a}_seq_end_{current_seq_num}_nbhundreds{nb_of_hundreds_by_seq}' + t + '.pkl'
            util.save_object(batch, filename)
        except APIError:
            traceback.print_exc()
            print(f'Something went wrong on {i}')
            pass



if __name__ == '__main__':
    dirname = sys.argv[1]
    starting_seq_num = int(sys.argv[2])
    nb_of_seq = int(sys.argv[3])
    main(dirname, starting_seq_num, nb_of_seq)