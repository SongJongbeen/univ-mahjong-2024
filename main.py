import csv
import random
import pandas as pd
from collections import defaultdict

def main(is_seoul = True):
    if is_seoul:
        file_path = "participants-seoul.csv"
        output_path = "results-seoul.csv"
    else:
        file_path = "participants-non-seoul.csv"
        output_path = "results-non-seoul.csv"

    df = pd.read_csv(file_path)

    # Expand the DataFrame by separating leader and member into individual entries
    expanded_df = pd.DataFrame({
        'univ': df['univ'].repeat(2).reset_index(drop=True),
        'club': df['club'].repeat(2).reset_index(drop=True),
        'player': pd.concat([df['leader'], df['member']]).reset_index(drop=True)
    })

    round_1_rooms = assign_rooms(expanded_df)
    round_2_rooms = assign_rooms(expanded_df)
    round_3_rooms = assign_rooms(expanded_df)
    round_4_rooms = assign_rooms(expanded_df)

    # write the results to a csv file
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Room', 'Player', 'University', 'Club'])
        for room, players in round_1_rooms.items():
            for player in players:
                writer.writerow([room, player['player'], player['univ'], player['club']])

        for room, players in round_2_rooms.items():
            for player in players:
                writer.writerow([room, player['player'], player['univ'], player['club']])
        
        for room, players in round_3_rooms.items():
            for player in players:
                writer.writerow([room, player['player'], player['univ'], player['club']])

        for room, players in round_4_rooms.items():
            for player in players:
                writer.writerow([room, player['player'], player['univ'], player['club']])

        print('done')

# Function to assign players to rooms for one round
def assign_rooms(players, num_rooms=8, players_per_room=4):
    rooms = defaultdict(list)
    univ_count = defaultdict(lambda: defaultdict(int))  # Count of players from each university in each room

    # Shuffle players to randomize assignment
    shuffled_players = players.sample(frac=1).reset_index(drop=True)

    for univ, club, player in shuffled_players.itertuples(index=False):
        assigned = False
        # Try to assign to a room where the club is not present and minimize university repetition
        for room in range(1, num_rooms + 1):
            if club not in [p['club'] for p in rooms[room]] and len(rooms[room]) < players_per_room:
                # Assign to this room if it has the least number of players from the same university
                if len(rooms[room]) == 0 or univ_count[room][univ] < players_per_room - 1:
                    rooms[room].append({'player': player, 'univ': univ, 'club': club})
                    univ_count[room][univ] += 1
                    assigned = True
                    break

        # If no room met the criteria, force assign to any room with space
        if not assigned:
            for room in range(1, num_rooms + 1):
                if len(rooms[room]) < players_per_room:
                    rooms[room].append({'player': player, 'univ': univ, 'club': club})
                    univ_count[room][univ] += 1
                    print('Forced assignment:', player, 'to room', room)
                    break

    return rooms

if __name__ == "__main__":
    main(False)
