# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# File containing functions to randomise data
# 1. Randomise team ids
# 2. Randomise player ids
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

import random
import copy

def main():
    pass

# -----------------------------------------------------------------------------
# 1. Randomise team ids
# Returns: a dict of format {match_id}: [[team_ids], [player_ids]] with
# shuffled team_ids
# -----------------------------------------------------------------------------

def randomise_team_ids(team_ids: dict, deep: bool = True) -> dict:
    '''Takes a dict with team_ids (team_ids) and a boolean (deep).
       Shuffles team ids in a given match, for each match.
       Parameter deep decides whether to return a deep copy of the data.
       Returns a (copied) shuffled dict.
    '''
    if deep:
        team_ids = copy.deepcopy(team_ids) 
        
    for team_player in team_ids.values(): 
        random.shuffle(team_player[0])
        
    return team_ids

# -----------------------------------------------------------------------------
# 2. Randomise player ids
# Returns: two lists of killers and victims with swapped IDs
# -----------------------------------------------------------------------------

def randomise_player_ids(killers: list = ['A', 'B', 'B'], 
                         victims:list = ['C', 'A', 'D']):
    '''Takes two lists of killers (killers) and victims (victims).
       Randomly swaps IDs of players but keeps the structure and timing of 
           events.
       Returns two lists of killers and victims with swapped IDs.
       
       To see an example, run the function with default inputs.
    '''
    
    killers_out, victims_out = [], [] 
    
    unique_players = list(set(killers + victims))
    unique_players_swaps = unique_players[:]
    
    random.shuffle(unique_players_swaps)
    
    # Swap players' ids
    for i in range(len(killers)):
        
        killers_out.append(unique_players_swaps[unique_players.index(killers[i])])
        victims_out.append(unique_players[unique_players.index(victims[i])])

    return killers_out, victims_out

if __name__ == '__name__':
    main()