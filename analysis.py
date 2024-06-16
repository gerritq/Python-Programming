# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# File conducts the analysis using loading, randomisation, and counting modules
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

from modules.loading import *
from modules.counting import *
from modules.randomisation import *
import os
        
def main():
    # Load data
    dict_teams = load_teams('assignment-final-data/team_ids.txt')
    dict_cheaters = load_cheaters('assignment-final-data/cheaters.txt')
    dict_kills = load_kills('assignment-final-data/kills.txt', dict_cheaters)
    
    #---- Task 1: Counting cheaters and expectation
    count_cheaters(dict_teams, dict_cheaters)
    print('\n-------------\n-------------\n-------------\n')

    #---- Task 2: Counting victims and expectation
    count_victims(dict_kills, dict_cheaters)
    print('\n-------------\n-------------\n-------------\n')
        
    #---- Task 3: Counting observers and expectation
    count_observers(dict_kills, dict_cheaters)


# -----------------------------------------------------------------------------
# Functions for counting and calculating expected values for number of cheaters
# victims who became cheaters, and observers who became cheaters
# -----------------------------------------------------------------------------

def count_cheaters(dict_teams:dict, dict_cheaters: dict):
    ''' Takes team data (dict_teams) and cheaters data (dict_cheaters).
        Calls count_cheaters_out() to output counts of cheaters per 
        team size.
        Calls exp_count_cheaters() to output the expected counts of 
        cheaters per team size.
        Returns none.
    '''
    count_cheaters_out(dict_teams, dict_cheaters)
    exp_count_cheaters(dict_teams, dict_cheaters)
    
def count_victims(dict_kills:dict, dict_cheaters: dict):
    ''' Takes kills data (dict_kills) and cheaters data (dict_cheaters).
        Calls count_victims_cheaters_out() to output counts of victims who
        became cheaters.
        Calls exp_count_victims_cheaters() to output the expected counts of 
        victims who became cheaters.
        Returns none.
    '''
    count_victims_cheaters_out(dict_kills, dict_cheaters)
    exp_count_victims_cheaters(dict_kills, dict_cheaters)
    
def count_observers(dict_kills:dict, dict_cheaters: dict):
    ''' Takes kills data (dict_teams) and cheaters data (dict_cheaters).
        Calls count_observers_cheaters_out() to output counts of observers who
        became cheaters.
        Calls exp_count_observers_cheaters() to output the expected counts of 
        observers who became cheaters.
        Returns none.
    '''
    count_observers_cheaters_out(dict_kills, dict_cheaters)
    exp_count_observers_cheaters(dict_kills, dict_cheaters)
    
if __name__ == '__main__':
    main()
    
    