from llm.groq_client import GroqClient


def llm_chat():
    groq_client = GroqClient()
    while True:
        message = input("Me: ")
        if message.lower() in ("exit", "quit"):
            break
        response = groq_client.get_response(message)
        print("Model:", response)
    return groq_client.get_messages()
