# Written for Python Version 3.5 by Marat Purnyn

import random  # used for random shuffeling & drawing
import os  # used for clearing the screen


class Card:
    def __init__(self, s, r):
        self.suit = s
        self.rank = r

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit


class Deck:
    def __init__(self):
        # using a dictionaries for easily converting from number representation to label
        self.suit_dict = {1: 'Clubs', 2: 'Diamonds', 3: 'Hearts', 4: 'Spades'}
        self.rank_dict = {1: 'Penalty', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
                       11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
        self.contents = []
        for s in range(1, 5):
            for r in range(1, 15):
                self.contents.append(Card(s,r))
        self.shuffle()

    def draw(self):
        drawn_card = self.contents.pop()
        return drawn_card

    def shuffle(self):
        random.shuffle(self.contents)

    def reshuffle(self):
        self.contents = []
        for s in range(1, 5):
            for r in range(1, 15):
                self.contents.append(Card(s, r))
        self.shuffle()

    def get_card_str(self, Card):
        card_str = str(self.rank_dict[Card.rank]) + " of " + str(self.suit_dict[Card.suit])
        return card_str


class Player:
    def __init__(self, id, card, points):
        self.id = id
        self.hand = card
        self.points = points

    def win(self):
        self.points += 2

    def penalty(self):
        if self.points > 0:
            self.points -= 1

    def add_hand(self, card):
        self.hand = card

    def get_id(self):
        return self.id

    def get_hand(self):
        return self.hand

    def get_points(self):
        return self.points

class Game:
    def __init__(self,player_count):
        self.player_count = player_count
        self.player_list = []
        self.deck = Deck()
        self.game_over = 0
        for player_id in range(0, self.player_count):
            new_player = Player(player_id, 0, 0)
            self.player_list.append(new_player)

    def start_game(self):
        while self.game_over == 0:
            for player in self.player_list:
                _=os.system('cls')  # Clears the screen in Windows
                print("\nPlayer {}".format(player.get_id()))
                input("Press enter to draw a card...")
                player_drawn = self.deck.draw()  # Deal Card to Player
                player.add_hand(player_drawn)  # Save Player ID and Card
                print("\nYou drew...")
                print(self.deck.get_card_str(player.get_hand()))
                input("\n\nPress enter for end of turn...")
            self.decide_round_winner()
            self.scoreboard()
            input("\n\nPress enter for next round...")
            self.deck.reshuffle()

    def scoreboard(self):
        print("\n********SCOREBOARD**********")
        print('{}\t{}'.format("PlayerID", "Score"))
        reached_21 = 0
        winner = 0
        for player in self.player_list:
            if player.get_points() >= 21:
                reached_21 = 1
                winner = player
            print('{0:2d}\t\t\t{1:3d}'.format(int(player.get_id()),int(player.get_points())))
        if reached_21 == 1:
            self.game_over = 1
            for player in self.player_list:
                if player.get_points() == winner.get_points()-1:
                    self.game_over = 0
            if self.game_over == 1:
                print("The winner of the game is Player {}".format(int(winner.get_id())))
                exit()

    def decide_round_winner(self):
        _ = os.system('cls')  # Clears the screen in Windows
        winner = self.player_list[0]  # Choose Player 0 as Potential Winner
        for player in self.player_list:
            if self.deck.rank_dict[player.hand.rank] == 'Penalty':
                player.penalty()
                print("Player {} had a penalty card. -1 point".format(player.id))
            else: # only compare if the card is not a penalty card
                if player.hand.get_rank() > winner.hand.get_rank():
                    winner = player  # Find the Player with Highest Card
                elif player.hand.get_rank() == winner.hand.get_rank():
                    if player.hand.get_suit() > winner.hand.get_suit():
                        winner = player
        if self.deck.rank_dict[winner.hand.rank] != 'Penalty':
            print("Round winner was Player {} +2 Points".format(winner.get_id()))
            print("Their card was "+self.deck.get_card_str(winner.get_hand()))
            winner.win()
            return winner.get_id()
        else:  # if the winning card is a penalty card then it means all the other cards were penalty cards
            print("No winner this round!")
            return -1


if __name__=="__main__":
    print("Game Start")
    players = int(input("Please enter how many players?: "))
    new_game = Game(players)
    new_game.start_game()