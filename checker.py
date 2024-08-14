import pandas as pd

# 1. read results-seoul.csv
# 2. count the number of players from the same club in the same round and the same room
# 3. print the number of players from the same club in the same round and the same room
# 4. count the number of players from the same university in the same round and the same room
# 5. print the number of players from the same university in the same round and the same room
# 6. count the number of players who met the same person in the previous round
# 7. print the number of players who met the same person in the previous round

def check_results(file_path):
    # 1. read results-seoul.csv
    # 2. count the number of players from the same club in the same round and the same room
    # 3. print the number of players from the same club in the same round and the same room
    # 4. count the number of players from the same university in the same round and the same room
    # 5. print the number of players from the same university in the same round and the same room
    # 6. count the number of players who met the same person in the previous round
    # 7. print the number of players who met the same person in the previous round
    df = pd.read_csv(file_path)
    round_1_rooms = {}
    round_2_rooms = {}
    round_3_rooms = {}
    round_4_rooms = {}

    for i in range(1, 5):
        round_rooms = locals()[f'round_{i}_rooms']
        for index, row in df[df['Room'].str.startswith(f'Round {i}')].iterrows():
            if row['Room'] not in round_rooms:
                round_rooms[row['Room']] = []
            round_rooms[row['Room']].append(row)

        club_count = {}
        univ_count = {}
        prev_player = {}

        for room, players in round_rooms.items():
            for player in players:
                club = player['Club']
                univ = player['University']
                name = player['Player']

                if club not in club_count:
                    club_count[club] = 0
                club_count[club] += 1

                if univ not in univ_count:
                    univ_count[univ] = 0
                univ_count[univ] += 1

                if name in prev_player:
                    prev_player[name] += 1
                else:
                    prev_player[name] = 0

        print(f'Round {i}')
        print('Club count:')
        for club, count in club_count.items():
            print(f'{club}: {count}')
        
        print('University count:')
        for univ, count in univ_count.items():
            print(f'{univ}: {count}')

        print('Previous player count:')
        for name, count in prev_player.items():
            print(f'{name}: {count}')

check_results('results-seoul.csv')