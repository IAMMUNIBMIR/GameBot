import requests
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chat bot
chatbot = ChatBot('GameRecommendationBot')

# Create a new trainer for the chat bot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chat bot on the English language data
trainer.train('chatterbot.corpus.english')

def get_chatbot_response(question):
    # Function to get a valid response from the chatbot
    response = input(question).lower()
    
    # Check if the response contains a valid genre or platform
    while response not in ["action", "adventure", "strategy", "rpg", "sports", "pc", "playstation", "xbox", "nintendo"]:
        print("Bot: I'm sorry, I didn't understand. Please provide a valid response.")
        response = input(question).lower()

    return response

# Ask the user for the game genre
genre_response = get_chatbot_response("Bot: What genre of game are you interested in? ")
genre = genre_response

# Ask the user for the gaming platform
platform_response = get_chatbot_response("Bot: Which gaming platform are you using? ")
platform = platform_response

print(f"Genre: {genre}, Platform: {platform}")

# RAWG API configuration
RAWG_API_KEY = "9b200d234d87425fbe262cc2b1635172"

def get_game_recommendations(genre, platform):
    params = {
        "key": RAWG_API_KEY,
        "genres": genre,
        "platforms": platform,
    }

    try:
        Url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&genres={genre}&platform={platform}"
        response = requests.get(Url)
        print(f"API Response: {response.text}")

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            if results:
                print("Top game recommendations:")
                for index, game in enumerate(results[:5], start=1):
                    game_name = game.get("name", "No game name found")
                    print(f"{index}. {game_name}")

                # Allow the user to choose a game from the list
                choice = input("Enter the number of the game you want to play (or type 'exit' to quit): ")

                if choice.lower() == 'exit':
                    print("Goodbye!")
                    return

                try:
                    choice_index = int(choice) - 1
                    chosen_game = results[choice_index].get("name", "No game name found")
                    print(f"You chose to play: {chosen_game}")
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number.")

            else:
                print("No game recommendations found.")
        else:
            print(f"Failed to retrieve game recommendations. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"Error making API request: {e}")

if __name__ == "__main__":
    get_game_recommendations(genre, platform)
