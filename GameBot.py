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
    response = chatbot.get_response(question).text.lower()

    return response

def daily_conversation(user_input):
    # Function to carry out daily conversations
    response = get_chatbot_response(user_input)
    print("Bot:", response)

def get_game_recommendations():
    # Function to get game recommendations based on genre and platform
    RAWG_API_KEY = "69e524c5cc224ca4a194b46ed4fafedf"

    # Ask the user for the game genre
    genre_response = input("Bot: What genre of game are you interested in? ")
    genre = genre_response.lower()

    # Ask the user for the gaming platform
    platform = input("Bot: Which gaming platform are you using? ")

    print(f"Bot: Great choice! Let me find some {genre} games for you on {platform}...")

    try:
        Rawg_Api_Url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&genres={genre}&platform={platform}"
        response = requests.get(Rawg_Api_Url)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            if results:
                print("\nTop game recommendations:")
                for index, game in enumerate(results[:5], start=1):
                    game_name = game.get("name", "No game name found")
                    print(f"{index}. {game_name}")

                # Allow the user to choose a game from the list
                choice = input("\nEnter the number of the game you want to play (or type 'exit' to quit): ")

                if choice.lower() == 'exit':
                    print("Bot: Goodbye! Have a great day.")
                    return

                try:
                    choice_index = int(choice) - 1
                    chosen_game = results[choice_index].get("name", "No game name found")
                    print(f"Bot: Excellent choice! You've chosen to play: {chosen_game}")
                except (ValueError, IndexError):
                    print("Bot: Invalid choice. Please enter a valid number.")

            else:
                print("Bot: I couldn't find any game recommendations. Sorry about that.")
        else:
            print(f"Bot: Failed to retrieve game recommendations. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"Bot: Error making API request: {e}")

if __name__ == "__main__":
    print("Bot: Hi there! I'm GameRecommendationBot. I can chat with you and even recommend games. If you want game recommendations, just type '/game'. If you need help, type '/help'.")

    while True:
        user_input = input("You: ")

        if user_input == '/help':
            print("Bot: I can chat with you and recommend games. To get game recommendations, type '/game'.")
        elif user_input == '/game':
            get_game_recommendations()
        else:
            daily_conversation(user_input)
