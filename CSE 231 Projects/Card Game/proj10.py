"""
CSE Project #10 - Card Game

Description

    This program implements a solitaire card game called 
    "Streets and Alleys" using two classes and a driver (this file).
    The game is played within the Python interpreter.
    The game's rules and a tutorial can be found at
    https://worldofsolitaire.com/
    For a detailed description of the program,
    read "Project10.pdf"

Notable Concepts

    classes, dictionaries, functions, try-except statements

Algorithm

    initialize playing materials
        initialize and shuffle deck
        create tableau as list of lists
            deal 7 cards to even-indexed nested lists
            deal 6 cards to odd-indexed nested lists
        create foundation as list of lists
    
    play game
        display board
        prompt for option and ensure it's valid
        if Mxx s d:
            if MTT:
                move card from tableau pile s to tableau pile d
            if MTF:
                move card from tableau pile s to foundation pile d
            if MFT:
                move card from foundation pile s to tableau pile d
            check if game won
                if game won:
                    start new game
                else:
                    continue current game
        if U:
            undo last valid move if there is one
        if R:
            restart game and display board
        if H:
            display board
        if Q:
            quit game 
        reprompt for option if option wasn't Q
"""



#DO NOT DELETE THESE LINES
import cards, random
random.seed(100) #random number generator will always generate 
                 #the same 'random' number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from Tableau pile s to Tableau pile d.
    MTF s d: Move card from Tableau pile s to Foundation d.
    MFT s d: Move card from Foundation s to Tableau pile d.
    U: Undo the last valid move.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''

# used in get_option()
VALID_COMMANDS = ["MTT", "MTF", "MFT", "U", "R", "H", "Q"]

                
def initialize():
    """
    create tableau and foundation, return them in a tuple
    """
    
    # initialize and shuffle deck
    deck = cards.Deck()
    deck.shuffle()
    
    # create tableau
    tableau = [[], [], [], [], [], [], [], []]
    
    # deal cards to tableau
    for index, tableau_pile in enumerate(tableau):
        
        # left column
        if index % 2 == 0:
            
            for i in range(7):
                
                tableau[index].append(deck.deal())
        
        # right column
        else:
            
            for i in range(6):
                
                tableau[index].append(deck.deal())
    
    # create foundation
    foundation = [[], [], [], []]
    
    return (tableau, foundation)
    

def display(tableau, foundation):
    '''Each row of the display will have
       tableau - foundation - tableau
       Initially, even indexed tableaus have 7 cards; odds 6.
       The challenge is the get the left vertical bars
       to line up no matter the lengths of the even indexed piles.'''
    
    # To get the left bars to line up we need to
    # find the length of the longest even-indexed tableau list,
    #     i.e. those in the first, leftmost column
    # The "4*" accounts for a card plus 1 space having a width of 4
    max_tab = 4*max([len(lst) for i,lst in enumerate(tableau) if i%2==0])
    # display header
    print("{1:>{0}s} | {2} | {3}".format(max_tab+2,"Tableau","Foundation","Tableau"))
    # display tableau | foundation | tableau
    for i in range(4):
        left_lst = tableau[2*i] # even index
        right_lst = tableau[2*i + 1] # odd index
        # first build a string so we can format the even-index pile
        s = ''
        s += "{}: ".format(2*i)  # index
        for c in left_lst:  # cards in even-indexed pile
            s += "{} ".format(c)
        # display the even-indexed cards; the "+3" is for the index, colon and space
        # the "{1:<{0}s}" format allows us to incorporate the max_tab as the width
        # so the first vertical-bar lines up
        print("{1:<{0}s}".format(max_tab+3,s),end='')
        # next print the foundation
        # get foundation value or space if empty
        found = str(foundation[i][-1]) if foundation[i] else ' '
        print("|{:^12s}|".format(found),end="")
        # print the odd-indexed pile
        print("{:d}: ".format(2*i+1),end="") 
        for c in right_lst:
            print("{} ".format(c),end="") 
        print()  # end of line
    print()
    print("-"*80)
          
def valid_tableau_to_tableau(tableau,s,d):
    """
    return Boolean indicating if tableau-to-tableau move is valid

    return True if move valid and False if move invalid
    """
    
    # ensure source card exists
    try:
    
        # create variable for source card
        source_card = tableau[s][-1]
    
    except IndexError:
        
        return False
    
    else:
        
        if len(tableau[d]) != 0:
            
            # create variable for destination card
            dest_card = tableau[d][-1]
            
            # determine if source card's rank is one less than destination card's
            valid_tt_rank_condition_bool = dest_card.rank() == \
                source_card.rank()+1
            
            # ensure tableau-to-tableau rank condition is met
            if not valid_tt_rank_condition_bool:
                
                return False
            
        return True
    
def move_tableau_to_tableau(tableau,s,d):
    """
    if move valid, move source card to destination deck and return True
    
    source: tableau, destination: tableau
    return False if move invalid
    """
    
    # determine if move is valid
    valid_move_bool = valid_tableau_to_tableau(tableau, s, d)

    # ensure move is only executed if valid
    if not valid_move_bool:
        
        return False
    
    else:
        
        # remove source card from source file
        source_card = tableau[s].pop()
        
        # move source card to destination deck
        tableau[d].append(source_card)
        
        return True

def valid_foundation_to_tableau(tableau,foundation,s,d):
    """
    return Boolean indicating if foundation-to-tableau move is valid

    return True if move valid and False if move invalid
    """
    
    # ensure source card exists
    try:
    
        # create variable for source card
        source_card = foundation[s][-1]
    
    except IndexError:
        
        return False
    
    else:
        
        if len(tableau[d]) != 0:
            
            # create variable for destination card
            dest_card = tableau[d][-1]
            
            # determine if source card's rank is one less than destination card's
            valid_ft_rank_condition_bool = dest_card.rank() == \
                source_card.rank()+1
            
            # ensure tableau-to-tableau rank condition is met
            if not valid_ft_rank_condition_bool:
                
                return False
            
        return True

def move_foundation_to_tableau(tableau,foundation,s,d):
    """
    if move valid, move source card to destination deck and return True
    
    source: foundation, destination: tableau
    return False if move invalid
    """
        
    # determine if move is valid
    valid_move_bool = valid_foundation_to_tableau(tableau, foundation, s, d)

    # ensure move is only executed if valid
    if not valid_move_bool:
        
        return False
    
    else:
        
        # remove source card from source file
        source_card = foundation[s].pop()
        
        # move source card to destination deck
        tableau[d].append(source_card)
        
        return True

def valid_tableau_to_foundation(tableau,foundation,s,d):
    """
    return Boolean indicating if tableau-to-foundation move is valid

    return True if move valid and False if move invalid
    """
    
    # ensure source card exists
    try:
    
        # create variable for source card
        source_card = tableau[s][-1]
    
    except IndexError:
        
        return False
    
    else:
        
        # ensure source card is Ace if destination deck is empty
        if len(foundation[d]) == 0:
            
            # ensure source card is ace
            if source_card.rank() != 1:
            
                return False
        elif len(foundation[d]) != 0:
                
            # create variable for destination card
            dest_card = foundation[d][-1]
                
            # determine if source card's rank is one more than destination card's
            valid_tf_rank_condition_bool = dest_card.rank()+1 == \
                source_card.rank()
                
            # determine if source and destination cards have same suit
            valid_tf_suit_condition_bool = dest_card.suit() == \
                source_card.suit()
                
            # ensure tableau-to-tableau rank condition is met
            if not (valid_tf_rank_condition_bool and \
                    valid_tf_suit_condition_bool):
                    
                return False
                
        return True
    
def move_tableau_to_foundation(tableau, foundation, s,d):
    """
    if move valid, move source card to destination deck and return True
    
    source: tableau, destination: foundation
    return False if move invalid
    """
        
    # determine if move is valid
    valid_move_bool = valid_tableau_to_foundation(tableau, foundation, s, d)

    # ensure move is only executed if valid
    if not valid_move_bool:
        
        return False
    
    else:
        
        # remove source card from source file
        source_card = tableau[s].pop()
        
        # move source card to destination deck
        foundation[d].append(source_card)
        
        return True

def check_for_win(foundation):
    """
    return True if foundation piles are full and False otherwise
    """
    
    return len([pile for pile in foundation if len(pile) == 13]) == 4

def get_option():
    """
    prompt for option, ensure it's valid, and return as list
    
    example format: [Mxx (str), s (int), d (int)]
    """
    
    # prompt for option
    option_str = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ")

    # upper and split option into list
    option_list = option_str.upper().split()
    
    # option type (ex. MTF)
    option_type = option_list[0]
    
    # ensure option type is valid
    if not option_type in VALID_COMMANDS:
        
        print("Error in option: " + option_str)
        
        return None

    if option_type == "MTT" or option_type == "MTF" or option_type == "MFT":
    
        # ensure option has two additional values
        if len(option_list) != 3:
            
            print("Error in option: " + option_str)
            
            return None
        
        # option source and destination
        option_source = option_list[1]
        option_dest = option_list[2]
        
        # ensure source and destination are numbers
        if not option_source.isnumeric():
                
                print("Error in Source.")
                
                return None
            
        if not option_dest.isnumeric():
               
               print("Error in Destination")
               
               return None
        
        # convert source and destination to integers
        option_source = int(option_source)
        option_dest = int(option_dest)
        
        # ensure source and destination are valid indices
        if option_type == "MFT":
        
            if not option_source in range(4):
            
                print("Error in Source.")
            
                return None
        
            if not option_dest in range(8):
            
                print("Error in Destination")
            
                return None
        
        # ensure source and destination are valid indices
        elif option_type == "MTF":
            
            if not option_source in range(8):
                
                print("Error in Source.")
                
                return None
            
            if not option_dest in range(4):
                
                print("Error in Destination")
                
                return None
        
        # ensure source and destination are valid indices
        elif option_type == "MTT":
                
            if not option_source in range(8):
                    
                print("Error in Source.")
                    
                return None
                
            if not option_dest in range(8):
                    
                print("Error in Destination")
                    
                return None
        
        # recreate option list with source and destination as integers
        option_list = [option_type, option_source, option_dest]
        
    else:
        
        # ensure option only includes type (U, R, H, or Q)
        if len(option_list) != 1:
            
            print("Error in option: " + option_str)
        
            return None
    
    return option_list

def main():  
    
    print("\nWelcome to Streets and Alleys Solitaire.\n")
    
    # create tableau and foundation
    tableau, foundation = initialize()
    
    # display board
    display(tableau, foundation)
    
    # display menu
    print(MENU)
    
    # initialize move history
    valid_moves_history_list = []
    
    # retrieve option
    option_list = get_option()
    
    # reprompt for option until valid
    while option_list == None:
        
        # retrieve option
        option_list = get_option()
    
    else:
        
        # execute for all non-Q options
        while option_list[0][0] != "Q":
            
            # execute if option Mxx s d
            if option_list[0][0] == "M":
                
                # create option type, source, and destination variables
                option_type, s, d = option_list[0], option_list[1], option_list[2]
                
                # tableau-to-tableau
                if option_type == "MTT":
                    
                    move_bool = move_tableau_to_tableau(tableau, s, d)
                
                # foundation-to-tableau
                elif option_type == "MFT":
                    
                    move_bool = move_foundation_to_tableau(tableau, foundation, s, d)
                
                # tableau-to-foundation
                elif option_type == "MTF":
                    
                    move_bool = move_tableau_to_foundation(tableau, foundation, s, d)
            
                # execute if move successful
                if move_bool:
                    
                    # check if game won
                    won_game_bool = check_for_win(foundation)
                    
                    # execute if game won
                    if won_game_bool:
                        
                        # clear move history
                        valid_moves_history_list = []
                        
                        print("You won!\n")
                        
                        display(tableau, foundation)
                        
                        print("\n- - - - New Game. - - - -\n")
                        
                        # restart game
                        tableau, foundation = initialize()
                        
                        display(tableau, foundation)
                        
                        print(MENU)
                    
                    # execute if game not won
                    else:
                        
                        # record move in move history
                        valid_moves_history_list.append(option_list)
                        
                        display(tableau, foundation)
                        
                
                # execute if move unsuccessful
                else:
                    
                    print("Error in move: {} , {} , {}".format(option_type, s, d))
                    
            # Undo
            if option_list[0] == "U":
                
                # ensure there are moves to undo
                try:
                
                    last_move_list = valid_moves_history_list.pop()
                
                except IndexError:
                    
                    print("No moves to undo.")
                    
                else:
                    
                    # last move type, source, and destination
                    last_move_type = last_move_list[0]
                    last_move_source = last_move_list[1]
                    last_move_dest = last_move_list[2]
                    
                    # tableau-to-tableau
                    if last_move_type == "MTT":
                    
                        # remove card from current pile
                        last_move_card = tableau[last_move_dest].pop()
                        
                        # return card to original pile
                        tableau[last_move_source].append(last_move_card)
                    
                    # foundation-to-tableau
                    elif last_move_type == "MFT":
                    
                        # remove card from current pile
                        last_move_card = tableau[last_move_dest].pop()
                        
                        # return card to original pile
                        foundation[last_move_source].append(last_move_card)
                    
                    # tableau-to-foundation
                    elif last_move_type == "MTF":
                    
                        # remove card from current pile
                        last_move_card = foundation[last_move_dest].pop()
                        
                        # return card to original pile
                        tableau[last_move_source].append(last_move_card)
                    
                    print("Undo: {} {} {}".format(last_move_type, \
                                            last_move_source, last_move_dest))
                    
                    display(tableau, foundation)
            
            # Restart
            if option_list[0] == "R":
                
                tableau, foundation = initialize()
                
                # clear move history
                valid_moves_history_list = []
                 
                display(tableau, foundation)
            
            # diaplay choices
            if option_list[0] == "H":
                
                print(MENU)
            
            # prompt for option
            option_list = get_option()
            
            # reprompt for option until valid, then continue
            while option_list == None:
        
                # retrieve option
                option_list = get_option()
                
            else:
                
                continue
            
        # Quit
        else:
            
            print("Thank you for playing.")

if __name__ == '__main__':
    
    main()