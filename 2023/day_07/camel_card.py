""" https://adventofcode.com/2023/day/7 """

class CamelCard():
    """
    The class containing the information and ranking functions for
    the camel card game
    """
    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input text file that contains the 5 card hands and the
        bets for each hand

        Args:
            input_file (str, optional): The text file containing the hands
            and the bets for each hand. Defaults to "input.txt".
        """

        # Map the face cards to other characters for sorting
        face_cards = {'T': 'B', 'J': '.', 'Q': 'D', 'K': 'E', 'A': 'F'}

        # initialize the lists
        hands = []
        bets = []
        rounds = []

        # read in the data
        for line in open(input_file, 'r', encoding="utf-8"):
            hand, bet = line.split()
            hands.append(hand)
            bets.append(int(bet))

            rounds.append((hand, int(bet)))

        # store the data
        self.face_cards = face_cards

        self.hands = hands
        self.bets = bets

        self.rounds = rounds

    def _hand_strength(self, hand:str) -> int:
        """       
        This function determines the strength of a given hand of cards.
        Every hand is exactly one type. From strongest to weakest, they are:

        Five of a kind (6)
            all five cards have the same label:
            AAAAA

        Four of a kind (5)
            four cards have the same label and one card has a different label:
            AA8AA
        
        Full house (4)
            three cards have the same label, and the remaining two cards
            share a different label:
            23332
        
        Three of a kind (3)
            three cards have the same label, and the remaining two cards are each
            different from any other card in the hand:
            TTT98
        
        Two pair (2)
            two cards share one label, two other cards share a second label,
            and the remaining card has a third label:
            23432
        
        One pair (1)
            two cards share one label, and the other three cards have a different
            label from the pair and each other:
            A23A4
        
        High card (0)
            where all cards' labels are distinct:
            23456

        Args:
            hand (str): a 5 character string denoting a hand of cards
        """

        # count the number of each card in the hand
        card_counts = [hand.count(card) for card in hand]

        hand_strength = 0

        # pair
        if 2 in card_counts:
            # 2 pair
            if card_counts.count(2) == 4:
                hand_strength = 2
            else:
                hand_strength = 1

        # 3 of a kind
        if 3 in card_counts:
            # full house
            if 2 in card_counts:
                hand_strength = 4

            # just 3 of a kind
            else:
                hand_strength = 3

        # 4 of a kind
        if 4 in card_counts:
            hand_strength = 5

        # 5 of a kind
        if 5 in card_counts:
            hand_strength = 6

        return hand_strength

    def _hand_ranker(self, hand:str, wildcard:bool=False) -> tuple:
        """
        Determines the overall rank of each hand by the hand strength
        and the cards in hand

        Args:
            hand (str): a 5 character string denoting a hand of cards
            wildcard (bool): a boolean to determine if we're using a wildcard

        Returns:
            tuple: A tuple containing the hand and card strength of the hand
        """

        # load in data
        face_cards = self.face_cards

        # determine the hand strength
        if wildcard:
            hand_strength = max(map(self._hand_strength, self._wildcard(hand)))
        else:
            hand_strength = self._hand_strength(hand)

        # if there are face cards then convert the face cards to different
        # characters so it can be sorted with the numbers
        card_strength = [
            face_cards.get(card, card) for card in hand
        ]

        return (hand_strength, card_strength)

    def _wildcard(self, hand:str) -> list:
        """
        Generates a new hand if it contains a J which is a wildcard

        Args:
            hand (str): The 5 card hand we might change

        Returns:
            list: The updated 5 card hand
        """

        # convert it to a list
        if hand == "":
            return [""]

        # recursive wildcard swap
        return[
            old + new
            for old in ("23456789TQKA" if hand[0] == "J" else hand[0])
            for new in self._wildcard(hand[1:])
        ]

    def calculate_winnings(self, wildcard:bool=False) -> int:
        """
        Calculates the total winnings through the formula
        SUM(bet * ranking)

        Args:
            wildcard (bool): a boolean to determine if we're using a wildcard

        Returns:
            int: The total winnings
        """

        # load in values
        rounds = self.rounds

        # sort the hands and bets
        rounds.sort(key=lambda val: self._hand_ranker(val[0], wildcard))

        # total up the winnings
        winnings = 0

        for rank, (_, bet) in enumerate(rounds, 1):
            winnings += rank * bet

        return winnings

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = CamelCard('input.txt').calculate_winnings()
    pt2_sol = CamelCard('input.txt').calculate_winnings(wildcard=True)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
