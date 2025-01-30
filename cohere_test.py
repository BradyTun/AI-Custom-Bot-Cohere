import cohere
import dotenv
import os

dotenv.load_dotenv()
api_key = os.environ.get('COHERE_KEY')
co = cohere.Client(api_key)

def generate_response(name, personality, user_input, history):
    try:
        # Format chat history to be natural without AI context
        formatted_history = "\n".join([
            f"User: {entry.message}\n{name}: {entry.response}"
            for entry in history
        ])  

        # Modify the prompt to remove AI references and focus on roleplaying
        prompt = (
            f"The following is a conversation with {name}, who has the personality: {personality}. "
            f"{name} stays in character and responds naturally based on their personality. "
            f"{name} acts and speaks like an actual human maintaining the conversation natrual. "
            f"They never say they are an AI or mention being a chatbot.\n\n"
            f"A message {name} sends must be short.\n\n"
            f"{formatted_history}\n"
            f"User: {user_input}\n"
            f"{name}:"
        )

        response = co.generate(
            model='command-xlarge-nightly',  
            prompt=prompt,
            max_tokens=100,  
            temperature=0.7,  
            k=0,  
            p=0.9,  
            stop_sequences=["\nUser:", f"{name}:"],  # Stop the bot from adding its name at the start
        )
        
        # Extract response and remove unintended prefixes
        bot_response = response.generations[0].text.strip()

        # Ensure the bot response doesn't start with "{name}:" (Failsafe)
        if bot_response.startswith(f"{name}:"):
            bot_response = bot_response[len(f"{name}:"):].strip()

        return bot_response

    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't process your request."

if __name__ == '__main__':
    # Example test case
    example_name = "Aiden"
    example_personality = "A mysterious and witty wanderer who speaks in riddles."
    example_user_input = "Tell me something interesting."
    example_history = [
        type("HistoryEntry", (object,), {"message": "Hello!", "response": "Ah, greetings, traveler. What brings you here?"})(),
        type("HistoryEntry", (object,), {"message": "Can you share a secret?", "response": "Secrets are whispers of the past, only known by the wind."})()
    ]

    response = generate_response(example_name, example_personality, example_user_input, example_history)
    print("Bot Response:", response)
