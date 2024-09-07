from openai import AzureOpenAI
import gradio as gr
client = AzureOpenAI(
  azure_endpoint = "https://aoai-ump-just-eastus.openai.azure.com/", 
  api_key="e25f7e82bb2440e49e183908c3324e8a",  
  api_version="2024-02-01"
)
# store the whole conversation
chat_history=""
diagnose_input=""
def diagnose_message():
    response = client.chat.completions.create(
        model="aoai-gpt-4o",  
        messages=[{"role": "system", "content": "You are playing a role as health helper. What you need to do is diagnosis. You will ask the following question: \
                   What's your age and height? After user ing the question, you should repeat the answer to check the result."}]
                   #1. What's your age? 2.What's your height? 3.What's your weight?"}]
    )
    bot_response = response.choices[0].message.content
    print(bot_response)
    return bot_response
def collect_data():
    datas=""
    user_input = input("You: ")
    datas += chat_with_bot(user_input)
    return datas

def chat_with_bot(user_input):
    # Send a request to the OpenAI API
    response = client.chat.completions.create(
        model="aoai-gpt-4o",  
        messages=[{"role": "user", "content": user_input}]
    )
    # Extract the response message content
    bot_response = response.choices[0].message.content
    return bot_response

# def conversation():
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             break
#         chat_history+=" user:"+user_input
#         if user_input=="diagnose" :
#                 diagnose_message()
                
#         bot_response = chat_with_bot(chat_history)
#         chat_history+=" bot:"+bot_response
#         #print(f"Bot: {bot_response}")
#         return bot_response

# def conversation(user_input):
#     #user_input = input("You: ")
#     #chat_history+=" user:"+user_input
#     if user_input=="diagnose" :
#             diagnose_message()
            
#     bot_response = chat_with_bot(chat_history)
#     #chat_history+=" bot:"+bot_response
#     #print(f"Bot: {bot_response}")
#     return bot_response

# if __name__ == "__main__":
#     conversation()


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        
        return "", history + [[user_message, None]]

    def bot(history):
        conversation = ""
        for message in history:
            conversation += f"User: {message[0]}\n"
            if message[1] is not None:
                conversation += f"Bot: {message[1]}\n"
        #user_message = history[-1][0]

            # Request to Azure OpenAI API
            response = client.chat.completions.create(
            model="aoai-gpt-4o",  
            messages=[{"role": "user", "content": conversation}]
            )

            bot_message = response.choices[0].message.content
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            #time.sleep(0.05)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()