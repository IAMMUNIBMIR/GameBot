import requests
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chat bot
chatbot = ChatBot('GameRecommendationBot')

# Create a new trainer for the chat bot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chat bot on the English language data
trainer.train('chatterbot.corpus.english')

# Game Recommendations
def game_recommendation(user_input):
    # Assuming the user input follows a format like "Recommend a [genre] game for [platform]."
    chatbot_response = chatbot.get_response(user_input)

    # Extract genre and platform from user input
    # Implement logic to fetch game recommendations using the RAWG API
    genre = "action"  # Extracted from user input or use a default
    platform = "pc"   # Extracted from user input or use a default


    rawg_api_key = "ae0b6ed4860f4e04ae2e3e91a422962b"
    rawg_api_url = f"https://api.rawg.io/api/games?key={rawg_api_key}&genres={genre}&platforms={platform}"

    try:
        response = requests.get(rawg_api_url)
        data = response.json()

        if response.status_code == 200 and 'results' in data:
            # Assume results contain a list of game recommendations
            recommendations = [game['name'] for game in data['results']]
            return f"I recommend these games: {', '.join(recommendations)}"
        else:
            return "Sorry, I couldn't fetch game recommendations at the moment."

    except Exception as e:
        print(f"Error fetching game recommendations: {e}")
        return "Sorry, an error occurred while fetching game recommendations."

# Example usage
user_input = input("You: ")
while user_input.lower() != 'exit':
    response = game_recommendation(user_input)
    print("Bot:", response)
    user_input = input("You: ")

print("Goodbye!")
