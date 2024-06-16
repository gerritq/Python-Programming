# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# File containing functions to count data
# 1. Counting cheaters per team
# 2. Counting victims becoming cheaters
# 3. Counting observers becoming cheaters
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

import numpy as np
from datetime import datetime
from modules.randomisation import randomise_team_ids, randomise_player_ids

def main():
    pass

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 1. Counting cheaters per team
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------- 

# -----------------------------------------------------------------------------
# Counts the number of cheaters per team size (0-4)
# Returns: dict of cheaters' counts per team
# -----------------------------------------------------------------------------
def count_cheaters(team_ids: dict, dict_cheaters: dict) -> dict:
    '''Takes a dict with team_ids (team_ids) and a dict with cheaters 
           (dict_cheaters).
       Counts cheaters within a match per team.
       Returns a dict of len 4, with the overall counts of cheaters per team 
           size.
    '''
    
    # Initialise counts
    counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    for match, team_player in team_ids.items():
    
        # Initialise dict containing all teams of a match
        helper_dict = {team: 0 for team in team_player[0]}
        
        # For each player. If cheater, add count to helper_dict
        for index in range(len(team_player[1])): # Lists have same len
            if team_player[1][index] in dict_cheaters:
                    helper_dict[team_player[0][index]] += 1
    
        # Assign to counters
        for num_cheater in helper_dict.values():
            counts[num_cheater] += 1
    
    return counts

# -----------------------------------------------------------------------------
# Wrapper for counting cheaters per team
# Runs count_cheaters() and "pretty-prints" output
# Returns: none
# ----------------------------------------------------------------------------- 
def count_cheaters_out(team_ids: dict, dict_cheaters: dict) -> dict:
    '''Wrapper function for count_cheaters().
        Pretty-prints the output for users.
    '''
    
    print('--- Number of cheaters per team ---')
    print('-----------------------------------')
    for team_size, count in count_cheaters(team_ids, dict_cheaters).items():
        
        print(f'--- Team size: {team_size} ---')
        print(f'\tNumber of cheaters: {count}')
        print('')
    print('\t\t')
    
    
# -----------------------------------------------------------------------------
# Expected counts of cheaters per team
# Returns: expected mean and confidence_interval of counts of cheaters per team
# ----------------------------------------------------------------------------- 

def exp_count_cheaters(team_ids: dict, dict_cheaters: dict, 
                       randomiser = randomise_team_ids, reps: int = 20, 
                       z_value: float = 1.96):
    '''Takes two dict with teams data (team_ids) and cheater data 
           (dict_cheaters).
       Takes a function (randomiser), the number of repetitions (reps), and a 
       z-value (z_value).
       Uses a function (randomiser) to randomly shuffle team IDs reps times.
       Calculates the expected mean and confidence interval with given z_value.
       Returns and prints expected mean and CI for each team size.
    '''
    outputs = []
    for _ in range(reps):
        outputs.append(count_cheaters(randomiser(team_ids), dict_cheaters))
        
    final_counts = {0: [], 1: [], 2: [], 3: [], 4: []}
    for counter in outputs:
        for count, count_num in counter.items():
            final_counts[count].append(count_num)
                
    expected_meand_sd = {count: [np.mean(count_num), 
                                 np.mean(count_num) - z_value * np.std(count_num) / np.sqrt(reps),
                                 np.mean(count_num) + z_value * np.std(count_num) / np.sqrt(reps)]
                         for count, count_num in final_counts.items()}

    print('--- Expected number of cheaters per team ---')
    print('--------------------------------------------')
    for count, (mean, lower, upper) in expected_meand_sd.items():
        print(f'--- Number of cheaters: {count} ---')
        print(f'\tExpected mean: {mean}')
        print(f'\t95% confidence interval: [{lower:.2f},  {upper:.2f}]\n')
        
    return expected_meand_sd


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 2. Counting victims becoming cheaters
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------- 

def count_victims_cheaters(dict_kills: dict, dict_cheaters: dict) -> dict:
    '''Takes two dict of kill data (dict_kills) and cheater data 
           (dict_cheaters).
       Counts how many victims started cheating based on belows condition.
       Returns a set with those players.
    '''
    
    # Conditions
    def cheater_active(player_id: str, date_min: datetime) -> bool:
        '''Takes player id (player_id) and game starting time (date_min). 
           Returns bool whether player is actively cheating.
        '''
        
        if player_id in dict_cheaters:
            if dict_cheaters[player_id][0] < date_min:
                return True
            
        return False 
    
    def later_cheater(victim_id: str, date_killing: datetime) -> bool:
        '''Takes victim id (victim_id) and killing date (date_killing). 
           Returns bool if player started cheating after the killing date.
        '''
        
        if victim_id in dict_cheaters:
            if dict_cheaters[victim_id][0] > date_killing:
                return True
        
        return False
    
    # Initialise to count new cheaters
    became_cheater = set()
    
    for match, (killer, victim, kDate) in dict_kills.items():
        for kill_index in range(len(killer)): # All same len
        
            if cheater_active(killer[kill_index], min(kDate)) and  \
                not cheater_active(victim[kill_index], min(kDate)) and \
                later_cheater(victim[kill_index], kDate[kill_index]):
                                         
                    became_cheater.add(victim[kill_index])

    return became_cheater

# -----------------------------------------------------------------------------
# Wrapper for counting victims who became cheaters
# Runs count_victims_cheaters() and "pretty-prints" output
# ----------------------------------------------------------------------------- 

def count_victims_cheaters_out(dict_kills: dict, dict_cheaters: dict) -> dict:
    '''Wrapper function for count_victims_cheaters().
       Pretty-prints the output for users.
    '''
    
    print('--- Victims becoming cheaters ---')
    print('---------------------------------')
    print(f'\tNumber of victims becoming cheaters: {len(count_victims_cheaters(dict_kills, dict_cheaters))}')
    print('\t\t')
    
# -----------------------------------------------------------------------------
# Expected counts of victims who became cheaters
# ----------------------------------------------------------------------------- 
    
def exp_count_victims_cheaters(dict_kills: dict, dict_cheaters: dict,
                               randomiser = randomise_player_ids, 
                               reps: int = 20, z_value: float = 1.96) -> list:
    '''Takes two dict with kills data (dict_kills) and cheater data 
           (dict_cheaters).
       Takes a function (randomiser), the number of repetitions (reps), and a 
       z-value (z_value).
       Uses a function (randomiser) to randomly swap player IDs reps times.
       Calculates the expected mean and confidence interval with given z_value.
       Returns and prints expected mean and CI for victims who became cheaters.
    '''
    
    alternative_dicts_kills = [] # List of alternative dict_kills

    for _ in range(reps):
        alternative_dicts_kills.append({match: [*randomiser(killer, victim), kDate] 
                                       for match, (killer, victim, kDate) 
                                       in dict_kills.items()})
        
    expected_counts = [len(count_victims_cheaters(new_world, dict_cheaters)) 
                       for new_world in alternative_dicts_kills]
    expected_counts = [np.mean(expected_counts), 
                       np.mean(expected_counts) - z_value * np.std(expected_counts) / np.sqrt(reps),
                       np.mean(expected_counts) + z_value * np.std(expected_counts) / np.sqrt(reps)
                       ]
    
    print('--- Expected number of victims becoming cheaters ---')
    print('----------------------------------------------------')
    print(f'\tExpected mean: {expected_counts[0]:.2f}')
    print(f'\t95% confidence interval: [{expected_counts[1]:.2f}, {expected_counts[2]:.2f}]')
    
    return expected_counts

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 3. Counting observers becoming cheaters
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------- 

# -----------------------------------------------------------------------------
# Counts the number of observers who became cheaters
# -----------------------------------------------------------------------------
def count_observers_cheaters(dict_kills: dict, dict_cheaters: dict) -> dict:
    '''Takes two dict of kills data (dict_kills) and cheater data 
           (dict_cheaters).
       Counts how many observers started cheating based on below defined 
           conditions.
       Returns a set with those players.
    '''
    
    observers_cheated = set()

    for match, (killer, victim, date) in dict_kills.items():
        
        helper_dict = {}
        for i in range(len(killer)): # All data of the same len
            
            if killer[i] in dict_cheaters and min(date) > dict_cheaters[killer[i]][0]:
                
                helper_dict.setdefault(killer[i], 0)
                helper_dict[killer[i]] += 1
     
                if helper_dict[killer[i]] == 3:
                    for observer in victim[date.index(date[i]) + 1:]: # observers
                        if observer in dict_cheaters and not  \
                            dict_cheaters[observer][0] < min(date):
                            observers_cheated.add(observer)
                    continue
            
    return observers_cheated

# -----------------------------------------------------------------------------
# Wrapper for counting observers who became cheaters
# Runs count_observers_cheaters() and "pretty-prints" output
# ----------------------------------------------------------------------------- 

def count_observers_cheaters_out(dict_kills: dict, dict_cheaters: dict) -> dict:
    '''Wrapper function for count_observers_cheaters().
        Pretty-prints the output for users.
    '''
    
    print('--- Observers becoming cheaters ---')
    print('-----------------------------------')
    print(f'\tNumber of observers becoming cheaters: {len(count_observers_cheaters(dict_kills, dict_cheaters))}')
    print('\t\t')
    

# -----------------------------------------------------------------------------
# Expected counts of the number of observers who became cheaters
# -----------------------------------------------------------------------------
    
def exp_count_observers_cheaters(dict_kills: dict, dict_cheaters: dict,
                                 randomiser = randomise_player_ids, reps: int = 20, 
                                 z_value: float = 1.96) -> list:
    '''Takes two dict with kills data (dict_kills) and cheater data 
           (dict_cheaters).
       Takes a function (randomiser), the number of repetitions (reps), and a 
       z-value (z_value).
       Uses a function (randomiser) to randomly swap player IDs reps times.
       Calculates the expected mean and confidence interval with given z_value.
       Returns and prints expected mean and CI for observers who became 
           cheaters.
    '''
    
    # Collect all alternative worlds
    alternative_dicts_kills = [] 
    for _ in range(reps):
        alternative_dicts_kills.append({match: [*randomiser(killer, victim), kDate] 
                                       for match, (killer, victim, kDate) 
                                       in dict_kills.items()})
        
    expected_counts = [len(count_observers_cheaters(new_world, dict_cheaters)) 
                       for new_world in alternative_dicts_kills]
    expected_counts = [np.mean(expected_counts), 
                       np.mean(expected_counts) - z_value * np.std(expected_counts) / np.sqrt(reps),
                       np.mean(expected_counts) + z_value * np.std(expected_counts) / np.sqrt(reps)
                       ]
    
    print('--- Expected number of observers becoming cheaters ---')
    print('------------------------------------------------------')
    print(f'\tExpected mean: {expected_counts[0]:.2f}')
    print(f'\t95% confidence interval: [{expected_counts[1]:.2f}, {expected_counts[2]:.2f}]')
    
    return expected_counts
    
if __name__ == '__name__':
    main()
    
    
    
    
    