# -*- coding: utf-8 -*-
''' Implement Mahjong Judger class
'''
from collections import defaultdict
import numpy as np

class MahjongJudger:
    ''' Determine what cards a player can play
    '''

    def __init__(self, np_random):
        ''' Initilize the Judger class for Mahjong
        '''
        self.np_random = np_random

    @staticmethod
    def judge_pong_gong(dealer, players, last_player):
        ''' Judge which player has pong/gong
        Args:
            dealer (object): The dealer object.
            players (list): List of all players
            last_player (int): The player id of last player

        '''
        last_card = dealer.table[-1]
        last_card_str = last_card.get_str()
        #last_card_value = last_card_str.split("-")[-1]
        #last_card_type = last_card_str.split("-")[0]
        for player in players:
            hand = [card.get_str() for card in player.hand]
            hand_dict = defaultdict(list)
            for card in hand:
                hand_dict[card.split("-")[0]].append(card.split("-")[1])
            #pile = player.pile
            # check gong
            if hand.count(last_card_str) == 3 and last_player != player.player_id:
                return 'gong', player, [last_card]*4
            # check pong
            if hand.count(last_card_str) == 2 and last_player != player.player_id:
                return 'pong', player, [last_card]*3
        return False, None, None

    def judge_game(self, game):
        ''' Judge which player has win the game
        Args:
            dealer (object): The dealer object.
            players (list): List of all players
            last_player (int): The player id of last player
        '''
        players_val = []
        win_player = -1
        for player in game.players:
            win, val = self.judge_hu(player)
            players_val.append(val)
            if win:
                win_player = player.player_id
        if win_player != -1 or len(game.dealer.deck) == 0:
            return True, win_player, players_val
        else:
            #player_id = players_val.index(max(players_val))
            return False, win_player, players_val

    def judge_hu(self, player):
        ''' Judge whether the player has win the game
        Args:
            player (object): Target player

        Return:
            Result (bool): Win or not
            Maximum_score (int): Set count score of the player
        '''
        set_count = 0
        tile_type_dict = {'dots':0, 'bamboo':0, 'characters':0}
        q = []
        for piles in player.pile:
            tile_type_dict[piles[0].type] += 3
        for tile in player.hand:
            tile_type_dict[tile.type] += 1
            if tile.type == 'dots':
                q.append(int(tile.trait))
            elif tile.type == 'bamboo':
                q.append(int(tile.trait) + 9)
            else:
                q.append(int(tile.trait) + 18)
        nothuazhu = tile_type_dict['dots'] == 0 or tile_type_dict['bamboo'] == 0 or tile_type_dict['characters'] == 0
        if not nothuazhu:
            return False, 0
        if tile_type_dict['dots'] == 0:
            base = 0
        elif tile_type_dict['bamboo'] == 0:
            base = 9
        else:
            base = 18
        bin = [0 for i in range(18)]    
        for t in q:
            if t > base:
                bin[t - 10] += 1
            else:
                bin[t - 1] += 1
        sum_1 = self.sum_list(bin[:9])
        sum_2 = self.sum_list(bin[9:])
        if (sum_1 + sum_2) % 3 != 2:
          return False, 0
        if sum_1 + sum_2 == 14:
            qiduizi = True
            for i in range(18):
                if bin[i] % 2 != 0:
                    qiduizi = False
                    break
            if qiduizi:
                return True, 0
        if sum_1 % 3 == 1 or sum_2 % 3 == 1:
            return False, 0
        if sum_1 % 3 == 0:
            if self.check_bin_0(bin[:9]) and self.check_bin_2(bin[9:]):
                return True, 4
        else:
            if self.check_bin_0(bin[9:]) and self.check_bin_2(bin[:9]):
                return True, 4
        return False, 0
    def check_bin_0(self, list):
        assert len(list) == 9
        bin = []
        for i in list:
            bin.append(i)
        for i in range(9):
            if bin[i] >= 3:
                bin[i] -= 3
            if bin[i] != 0:
                if i > 6:
                    return False
                if bin[i + 1] < bin[i] or bin[i + 2] < bin[i]:
                    return False
                bin[i + 1] -= bin[i]
                bin[i + 2] -= bin[i]
                bin[i] = 0
        return True
    def check_bin_2(self, list):
        assert len(list) == 9
        for i in range(9):
            if list[i] >= 2:
                bin = []
                for j in list:
                    bin.append(j)
                bin[i] -= 2
                if self.check_bin_0(bin):
                    return True
        return False
    def sum_list(self, list):
        num = 0
        for i in list:
            num += i
        return num

    @staticmethod
    def check_consecutive(_list):
        ''' Check if list is consecutive
        Args:
            _list (list): The target list

        Return:
            Result (bool): consecutive or not
        '''
        l = list(map(int, _list))
        if sorted(l) == list(range(min(l), max(l)+1)):
            return True
        return False
    def judge_chow(self, dealer, players, last_player):
        ''' Judge which player has chow
        Args:
            dealer (object): The dealer object.
            players (list): List of all players
            last_player (int): The player id of last player
        '''

        last_card = dealer.table[-1]
        last_card_str = last_card.get_str()
        last_card_type = last_card_str.split("-")[0]
        last_card_index = last_card.index_num
        for player in players:
            if last_card_type != "dragons" and last_card_type != "winds" and last_player == player.get_player_id() - 1:
                # Create 9 dimensional vector where each dimension represent a specific card with the type same as last_card_type
                # Numbers in each dimension represent how many of that card the player has it in hand
                # If the last_card_type is 'characters' for example, and the player has cards: characters_3, characters_6, characters_3,
                # The hand_list vector looks like: [0,0,2,0,0,1,0,0,0]
                hand_list = np.zeros(9)

                for card in player.hand:
                    if card.get_str().split("-")[0] == last_card_type:
                        hand_list[card.index_num] = hand_list[card.index_num]+1

                #pile = player.pile
                #check chow
                test_cases = []
                if last_card_index == 0:
                    if hand_list[last_card_index+1] > 0 and hand_list[last_card_index+2] > 0:
                        test_cases.append([last_card_index+1, last_card_index+2])
                elif last_card_index < 9:
                    if hand_list[last_card_index-2] > 0 and hand_list[last_card_index-1] > 0:
                        test_cases.append([last_card_index-2, last_card_index-1])
                else:
                    if hand_list[last_card_index-1] > 0 and hand_list[last_card_index+1] > 0:
                        test_cases.append([last_card_index-1, last_card_index+1])

                if not test_cases:
                    continue        

                for l in test_cases:
                    cards = []
                    for i in l:
                        for card in player.hand:
                            if card.index_num == i and card.get_str().split("-")[0] == last_card_type:
                                cards.append(card)
                                break
                    cards.append(last_card)
                    return 'chow', player, cards
        return False, None, None
    def cal_set(self, cards):
        ''' Calculate the set for given cards
        Args:
            Cards (list): List of cards.

        Return:
            Set_count (int):
            Sets (list): List of cards that has been pop from user's hand
        '''
        tmp_cards = cards.copy()
        sets = []
        set_count = 0
        _dict = {card: tmp_cards.count(card) for card in tmp_cards}
        # check pong/gang
        for each in _dict:
            if _dict[each] == 3 or _dict[each] == 4:
                set_count += 1
                for _ in range(_dict[each]):
                    tmp_cards.pop(tmp_cards.index(each))

        # get all of the traits of each type in hand (except dragons and winds)
        _dict_by_type = defaultdict(list)
        for card in tmp_cards:
            _type = card.split("-")[0]
            _trait = card.split("-")[1]
            if _type == 'dragons' or _type == 'winds':
                continue
            else:
                _dict_by_type[_type].append(_trait)
        for _type in _dict_by_type.keys():
            values = sorted(_dict_by_type[_type])
            if len(values) > 2:
                for index, _ in enumerate(values):
                    if index == 0:
                        test_case = [values[index], values[index+1], values[index+2]]
                    elif index == len(values)-1:
                        test_case = [values[index-2], values[index-1], values[index]]
                    else:
                        test_case = [values[index-1], values[index], values[index+1]]
                    if self.check_consecutive(test_case):
                        set_count += 1
                        for each in test_case:
                            values.pop(values.index(each))
                            c = _type+"-"+str(each)
                            sets.append(c)
                            if c in tmp_cards:
                                tmp_cards.pop(tmp_cards.index(c))
        return set_count, sets
# from card import MahjongCard as Card
# from player import MahjongPlayer as Player
# if __name__ == "__main__":
#    judger = MahjongJudger(0)
#    player = Player(0, 0)
#    card_info = Card.info
#    #print(card_info)
#    #player.pile.append([Card(card_info['type'][0], card_info['trait'][0])]*3)
#    #print([card.get_str() for card in player.pile[0]])
#    #player.hand.extend([Card(card_info['type'][0], card_info['trait'][0])]*2)
#     # player.hand.extend([Card(card_info['type'][0], card_info['trait'][0])]*2)
#     # player.hand.extend([Card(card_info['type'][0], card_info['trait'][1])]*2)
#     # player.hand.extend([Card(card_info['type'][1], card_info['trait'][2])]*2)
#     # player.hand.extend([Card(card_info['type'][1], card_info['trait'][7])]*2)
#     # player.hand.extend([Card(card_info['type'][1], card_info['trait'][8])]*2)
#     # player.hand.extend([Card(card_info['type'][2], card_info['trait'][1])]*2)
#     # player.hand.extend([Card(card_info['type'][2], card_info['trait'][3])]*2)
#    player.hand.extend([Card(card_info['type'][1], card_info['trait'][1])]*1)
#    player.hand.extend([Card(card_info['type'][1], card_info['trait'][2])]*2)
#    player.hand.extend([Card(card_info['type'][1], card_info['trait'][3])]*3)
#    player.hand.extend([Card(card_info['type'][1], card_info['trait'][4])]*2)
#    player.hand.extend([Card(card_info['type'][1], card_info['trait'][5])]*1)
#    player.hand.extend([Card(card_info['type'][2], card_info['trait'][2])]*3)
#    player.hand.extend([Card(card_info['type'][2], card_info['trait'][3])]*2)
#    #player.hand.extend([Card(card_info['type'][2], card_info['trait'][4])]*1)
#    print([card.get_str() for card in player.hand])
#    print(judger.judge_hu(player))
