from openai import AzureOpenAI
import gradio as gr
client = AzureOpenAI(
  azure_endpoint = "https://aoai-ump-just-eastus.openai.azure.com/", 
  api_key="XX",  
  api_version="2024-06-01"
)

initial_prompt="You are a health helper. You should ask\"How can I help you today? If you need diagnose, please say \"diagnose\".\""

initial_prompt="You are a health helper. The first question you should ask is \"Hi, I'm your health helper. How can I help you today?\" \
                Then the user will ask you to do a stimulating diagonse for him. You will ask the basic health information about the user in several continuous questions, including age, height, gender and symptoms. \
                User will provide all the information, do not create conversation by yourself.\
                After you get all the information. You should ask the user \"Thanks for providing the information, have you told me all the symptoms?\""

if_diagnose=False
data_prompt=""

def ai_search(search_content):
    # TODO
    return "** This is the search result **"

def insert_string(original_string,search_string,new_string):
    index = original_string.find(search_string)

    # Check if the search_string is found
    if index != -1:
        # Insert the new string at the found position
        updated_string = original_string[:index] + new_string + original_string[index:]
        return updated_string
    else:
        # Return the original string if the search_string is not found
        return original_string

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()

    def user(user_message, history):
        global if_diagnose, data_insert_index,data_prompt
        # Diagnose mode
        if user_message.lower()=="yes":
            if_diagnose=True
            # Combine history conversation
            conversation = initial_prompt + " "
            for message in history:
                conversation += f"User: {message[0]}\n"
                if message[1] is not None:
                    conversation += f"Bot: {message[1]}\n"
            # Extract the search content
            extract_prompt="Here is a conversation between a user and a chatbot. The user has provided some basic health information and described some symptoms. \
                            Please summarize the basic health informations and the symptoms. You should only reply the summary. \
                            In a format like: \"basic informations: height is 170cm, weight is 70kg, gender is male. The symptoms are coughing, headache and fever.\" The conversation is:"
            response = client.chat.completions.create(
            model="aoai-gpt-4o",  
            messages=[{"role": "user", "content": extract_prompt+conversation}]
            )
            bot_message = response.choices[0].message.content
            # AI Search
            search_result=ai_search(bot_message)
            # Add the search result in conversation history
            data_prompt="Here are some disease records that we had, please based on these data and the personal information I provided, give me a diagnose to my symptoms.\
                        The diagnose should include something like: \"Based on your information and symptoms, Your diagnosis is:...\"\
                        You should mention you are not a real doctor, so this diagosis may not be true, please consult a real doctor.  "+search_result
            #user_message=data_prompt+search_result
            # # Shift history
            # history + [[user_message, None]]
            # history[-1][1] = ""
            # return "",history


        # Normal conversation flow
        return "", history + [[user_message, None]]

    def bot(history):
        global data_prompt,if_diagnose
        # Combine history conversation
        conversation = initial_prompt + " "
        for message in history:
            conversation += f"User: {message[0]}\n"
            if message[1] is not None:
                conversation += f"Bot: {message[1]}\n"
        #user_message = history[-1][0]
        if if_diagnose:
            insert_string(conversation,"User: yes",data_prompt)

        # Request to Azure OpenAI API
        response = client.chat.completions.create(
        model="aoai-gpt-4o",  
        messages=[{"role": "user", "content": conversation}]
        )

        bot_message = response.choices[0].message.content

        # Update the history
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            #time.sleep(0.05)
            yield history
    

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

demo.launch()

# store the whole conversation
# chat_history=""
# diagnose_input=""
# def diagnose_message():
#     response = client.chat.completions.create(
#         model="aoai-gpt-4o",  
#         messages=[{"role": "system", "content": "You are playing a role as health helper. What you need to do is diagnosis. You will ask the following question: \
#                    What's your age and height? After user ing the question, you should repeat the answer to check the result."}]
#                    #1. What's your age? 2.What's your height? 3.What's your weight?"}]
#     )
#     bot_response = response.choices[0].message.content
#     print(bot_response)
#     return bot_response
# def collect_data():
#     datas=""
#     user_input = input("You: ")
#     datas += chat_with_bot(user_input)
#     return datas

# def chat_with_bot(user_input):
#     # Send a request to the OpenAI API
#     response = client.chat.completions.create(
#         model="aoai-gpt-4o",  
#         messages=[{"role": "user", "content": user_input}]
#     )
#     # Extract the response message content
#     bot_response = response.choices[0].message.content
#     return bot_response

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