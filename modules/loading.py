# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# File containing functions to load data
# 1. Load cheater data
# 2. Load teams data
# 3. Load kills data
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

from datetime import datetime

def main():
    pass

# -----------------------------------------------------------------------------
# 1. Load cheater data
# Format: {cheater_id}: [start_date, banned_date]
# -----------------------------------------------------------------------------

def load_cheaters(path: str) -> dict:
    '''Takes path as string.
       Streams the cheaters.txt file in to the following dict structure:
           {cheater_id}: [start_date, banned_date]
       Returns the dict.
    '''
    
    dict_cheaters = {}
    for line in open(path, 'r'):
        
        data = line.rstrip().split('\t')
        data[-1] = datetime.strptime(data[-1], '%Y-%m-%d')
        data[-2] = datetime.strptime(data[-2], '%Y-%m-%d')
    
        dict_cheaters.setdefault(data[0], data[1:])
    
    return dict_cheaters

# -----------------------------------------------------------------------------
# 2. Load teams data
# Format: {match_id}: [[team_ids], [player_ids]]
# -----------------------------------------------------------------------------

def load_teams(path: str) -> dict:
    '''Takes path as string.
       Streams the team_ids.txt file in to the following dict structure:
           {match_id}: [[team_ids], [player_ids]]
       Exploits the fact that indices of both lists within a match correspond.
       Returns the dict.
    '''
    dict_ids = {}
    for line in open(path, 'r'):
        data = line.rstrip().split('\t')
        data[-1] = int(data[-1])
        
        dict_ids.setdefault(data[0], [[], []])
        dict_ids[data[0]][0].append(data[2]) # team_ids
        dict_ids[data[0]][1].append(data[1]) # player_ids
        
    return dict_ids

# -----------------------------------------------------------------------------
# 3. Load kills data
# Format: {match_id}: [[killer_ids], [victim_ids], [killing_dates]]
# -----------------------------------------------------------------------------

def load_kills(path: str, sort = True) -> dict:
    '''Takes path as string and boolean (sort) to indicate whether data should 
       be sorted.
       Streams the kills.txt file in to the following dict structure:
           {match_id}: [[killer_ids], [victim_ids], [killing_dates]]
       Exploits the fact that indices of all lists within a match correspond.
       If sort is True, data is sorted before it is returned.
       Returns the dict.
    '''
    dict_kills = {}
    for line in open(path, 'r'):
        data = line.rstrip().split('\t')
        data[-1] = datetime.strptime(data[-1], '%Y-%m-%d %H:%M:%S.%f')
        
        dict_kills.setdefault(data[0], [[], [], []])
        dict_kills[data[0]][0].append(data[1]) # killer
        dict_kills[data[0]][1].append(data[2]) # victim
        dict_kills[data[0]][2].append(data[3]) # time
        
    if sort:
        for match, (killer, victim, kDate) in dict_kills.items():
            sortd = list(sorted(zip(kDate, killer, victim), key=lambda triple: triple[0]))
            dict_kills[match] = [[x[1] for x in sortd], [x[2] for x in sortd], [x[0] for x in sortd]]
        
    return dict_kills

if __name__ == '__name__':
    main()
    
