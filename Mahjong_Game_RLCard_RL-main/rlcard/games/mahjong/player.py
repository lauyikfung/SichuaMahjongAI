import copy
from rlcard.utils.utils import change_to_china

class MahjongPlayer:

    def __init__(self, player_id, np_random):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.pile = []

    def get_player_id(self):
        ''' Return the id of the player
        '''

        return self.player_id

    def print_hand(self):
        ''' Print the cards in hand in string.
        '''
        def cmp(x, y):
            return true
        hand_after_sort = copy.deepcopy(self.hand)
        hand_after_sort.sort(key=lambda x:(x.type, x.trait))
        print("{}, at all he has {} cards".format([c.print_current_card() for c in hand_after_sort], len(self.hand)))

    def print_pile(self):
        ''' Print the cards in pile of the player in string.
        '''
        print([[c.print_current_card() for c in s]for s in self.pile])

    def play_card(self, dealer, card):
        ''' Play one card
        Args:
            dealer (object): Dealer
            Card (object): The card to be play.
        '''
        card = self.hand.pop(self.hand.index(card))
        dealer.table.append(card)

    def gong(self, dealer, cards):
        ''' Perform Gong
        Args:
            dealer (object): Dealer
            Cards (object): The cards to be Gong.
        '''
        for card in cards:
            if card in self.hand:
                self.hand.pop(self.hand.index(card))
        self.pile.append(cards)

    def pong(self, dealer, cards):
        ''' Perform Pong
        Args:
            dealer (object): Dealer
            Cards (object): The cards to be Pong.
        '''
        cnt = 0
        for card in cards:
            if card in self.hand:
                self.hand.pop(self.hand.index(card))
                cnt += 1
                if cnt == 2:
                    break
        self.pile.append(cards)
