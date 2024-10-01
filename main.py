import csv
import requests
from bs4 import BeautifulSoup


def get_top_100_player_ranks(url: str = ""):
    url = url or "https://www.fifaratings.com/players"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_players = soup.find("div", class_="table-responsive")
    player_data = []

    if all_players:
        player_names = [span.a.get_text() for span in
                        all_players.find_all("span", class_='entry-font entry-font-narrow')]
        player_ratings = [span.get_text() for span in all_players.find_all("span", class_='attribute-box')]

        for name, rating in zip(player_names, player_ratings):
            player_data.append({'name': name, 'rating': rating})

    return player_data


def write_player_data(filename: str = "Top_100_Player_Ranking.csv") -> None:
    players = get_top_100_player_ranks()
    print("Player name and FIFA Rating\n")
    with open(filename, "w", newline="") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Player Name", "FIFA Rating"])

        # Iterate through the list of player data dictionaries
        for player in players:
            name = player['name']
            rating = player['rating']
            print(name, " ", rating)
            writer.writerow([name, rating])


if __name__ == "__main__":
    write_player_data()
