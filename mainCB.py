from chatbot.response import predict_class, get_response
from tensorflow.keras.models import load_model

def main():
    model = load_model('chatbot/chatbot_model.keras')
    
    print("Chatbot running...")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        
        prediction = predict_class(user_input, model)
        response = get_response(prediction)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
