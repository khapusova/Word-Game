# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#I wrote function play_game(word_list) better of all in my opinion
# Name          : Diana Khapusova
# Collaborators : none
# Time spent    : 5-6 hours
import copy
import math
import re
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    word_length = len(word.lower())
    x1 = 0
    for i in word.lower():
        if i =='*':
            x1+=0

        else:
            x1+= SCRABBLE_LETTER_VALUES[i]
    x2 = max(1,7 * word_length - 3  * (n - word_length))
    return x1*x2




#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    for i in hand.keys():
        if ord(i) == 97 or ord(i) == 101 or ord(i) == 105 or ord(i) == 111 or ord(i) == 117:
            if hand[i]<2:
                s1 = "'" + str(i) + "'" + ": " + str(hand[i])
                s2 = "'*'" + ': ' + '1'
                # print(s1)
                hand = str(hand)
                hand = hand.replace(s1, s2)
                hand = eval(hand)
            else:
                s1 = "'" + str(i) + "'" + ": " + str(hand[i])
                s12 = "'" + str(i) + "'" + ": " + str(hand[i]-1)
                hand = str(hand)
                hand = hand.replace(s1, s12)
                hand = eval(hand)
                hand.update({'*': 1})
            break

    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    dictionary = copy.copy(hand)
    for i in word.lower():
        if i in dictionary.keys():
            if  dictionary[i]!=0:
                dictionary[i] = dictionary[i]-1
    #print(display_hand(dictionary))
    return dictionary

    pass  # TO DO... Remove this line when you implement this function


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    if '*' in word:

        word1 = word.replace('*', 'a')
        if word1 not in word_list:
            word1 = word.replace('*', 'i')
            if word1 not in word_list:
                word1 = word.replace('*', 'e')
                if word1 not in word_list:
                    word1 = word.replace('*', 'o')
                    if word1 not in word_list:
                        word1 = word.replace('*', 'u')
                        if word1 not in word_list:
                            return False

        # TRY!!!!!!!!!
    elif not word.lower() in word_list:
        return False
    for i in word.lower():
        if not i in hand.keys() or hand[i]==0:
            return False
        else:
            hand = update_hand(hand, i)

    return True
pass  # TO DO... Remove this line when you implement this function


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    k = 0
    for i in hand.keys():
        k+=hand[i]
    return k


    pass  # TO DO... Remove this line when you implement this function


def play_hand(hand, word_list):
    total=0

    while True:
        k = 0
        for i in hand.keys():
            if hand[i]!=0:
                k+=1
        if k==0:
            print(f'Ran out of letters. Total score: {total} points')
            break
        display_hand(hand)
        word = input('Enter word, or “!!” to indicate that you are finished:')
        if word == '!!':
            print(f'Total score:{total}')
            break
        elif is_valid_word(word, hand, word_list)==True:
            total+=get_word_score(word,len(hand))
            print(f'“{word}” earned {get_word_score(word,len(hand))} points. Total score:{total}')

        else:
            print('This is not a valid word. Please choose another word.')
        hand = update_hand(hand,word)
    return int(total)


    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score

    # As long as there are still letters left in the hand:

    # Display the hand

    # Ask user for input

    # If the input is two exclamation points:

    # End the game (break out of the loop)

    # Otherwise (the input is not two exclamation points):

    # If the word is valid:

    # Tell the user how many points the word earned,
    # and the updated total score

    # Otherwise (the word is not valid):
    # Reject invalid word (print a message)

    # update the user's hand by removing the letters of their inputted word

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function


#
# Problem #6: Playing a game
#


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    vovels = VOWELS+CONSONANTS
    hand1 = copy.copy(hand)
    for i in hand1.keys():
        vovels = vovels.replace(i, '')
        if i == letter:
            hand[random.choice(vovels)] = hand.pop(i)
            break
    return hand

def algorithmyes(hand, word='',total=0):
        while True:
            k = 0
            for i in hand.keys():
                if hand[i] != 0:
                    k += 1
            if k == 0:
                print(f'Ran out of letters. Total score: {total} points')
                break
            letter = input('Which letter would you like to replace:')
            try:
                if letter not in hand.keys():
                    raise Exception
                hand = substitute_hand(hand, letter)
                total=play_hand(hand, word_list)

                break
            except Exception:
                print('uncorrect data!')
                continue
            print(f'Total score for this hand:{total}')
        return int(total)


def play_game(word_list):
    def intf():
        kolvo =input('Enter total number of hands:')
        try:
            kolvo=int(kolvo)
            if kolvo<1:
                raise Exception
            return int(kolvo)
        except Exception:
            print('uncorrect data!')
            return intf()
    def provyesno(a,b,quest):
        k = input(quest)
        if k == a or k==b:
            return k
        else:
            print('uncorrect data!')
            return provyesno(a, b, quest)

    ttotal = 0
    kolvo = intf()
    for i in range(0, kolvo):

        total = 0
        hand = deal_hand(HAND_SIZE)
        display_hand(hand)
        zap1 = provyesno('yes','no', 'Would you like to substitute a letter?')
        if zap1=='yes':
             ttotal+=algorithmyes(hand)
        else:
            ttotal+=play_hand(hand, word_list)
        zap2 = provyesno('yes','no', 'Would you like to replay the hand?')


        if zap2 == 'yes':


            '''zap1 = provyesno('yes', 'no', 'Would you like to substitute a letter?')
            if zap1 == 'yes':
                ttotal+=algorithmyes(hand)
            else:'''
            ttotal+=play_hand(hand, word_list)
        print('---------------------------------------------------------------------------')

    print(
f'Total score over all hands:{ttotal} '
)







#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':

    word_list = load_words()
    play_game( word_list)

