from rlcard.games.mahjong.utils import init_deck
from rlcard.utils.utils import change_to_china

class MahjongDealer:
    ''' Initialize a mahjong dealer class
    '''
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_deck()
        self.shuffle()
        self.table = []

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player, num):
        ''' Deal some cards from deck to one player

        Args:
            player (object): The object of DoudizhuPlayer
            num (int): The number of cards to be dealed
        '''
        for _ in range(num):
            cur_pai = self.deck.pop()
            player.hand.append(cur_pai)
            if num == 1:
                print("进张 {}".format(change_to_china(cur_pai.trait) + change_to_china(cur_pai.type)))



## For test
#if __name__ == '__main__':
#    dealer = MahjongDealer()
#    for card in dealer.deck:
#        print(card.get_str())
#    print(len(dealer.deck))
