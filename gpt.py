from openai import AzureOpenAI
import gradio as gr
import json
import os

client = AzureOpenAI(
  azure_endpoint = "https://aoai-ump-just-eastus.openai.azure.com/", 
  api_key="XX",  
  api_version="2024-06-01"
)

initial_prompt="You are a health helper. The first question you should ask is \"Hi, I'm your AI medicine notebook. How can I help you today? I can be your medicine notebook or I can provide diagnose and health suggestion for you.\" \
                If the user says medicine notebook, you will have some prescription data of this user, _base on the prescription data, answer the question from the user.\
                If the user says diagnose, you will do a stimulating diagonse for him. You will ask the basic health information about the user in several continuous questions, including age, height, gender and symptoms. \
                User will provide all the information, do not create conversation by yourself.\
                After you get all the information. You should ask the user \"Thanks for providing the information, have you told me all the symptoms?\
                If the user says suggestion,You will ask the basic health information about the user in several continuous questions, including age, height and gender,\
                User will provide all the information, do not create conversation by yourself.\
                After you get all the information. You should make some suggestion base on the information."

if_diagnose=False
if_suggestion=False
if_note=False
data_prompt=""

def add_prescription(prescription_text):
    """Add a prescription to an existing file or create a new one."""
    data = read_prescriptions()
    
    # Add a new prescription
    
    data["prescriptions"].append(prescription_text)

    save_data(data, "Prescriptions.json")
    #print("Prescription added successfully.")

def load_data(filename):
    """Load the prescription data from a JSON file."""
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def save_data(data, filename):
    """Save the prescription data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def read_prescriptions():
    """Read all prescriptions for a patient."""
    data = json.dumps(load_data("Prescriptions.json"))
    return data


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
    with gr.Row():
        gr.Markdown("# AI お薬手帳")  # Title at the top
        gr.Markdown(value='<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg6JktpLgrL79uphgxp_cu5IbWYiZXXHXxen1HuP1I1gMRDy9W6a6tPMRvSJ7OkNEoHCaASLl1u-aXDZm2oXUeeqFtDnlN5H-7qn9ClkwG2ZZsKv1cpREuRA9_wp13YdVMUTwT8SLwW3qou/s1600/kenkoushindan_hana_taisougi_boy.png" width="100" height="100">', 
                    elem_id="logo")


    chatbot = gr.Chatbot(show_label=False)
    msg = gr.Textbox()

    def user(user_message, history):
        global if_diagnose,if_note, data_insert_index,data_prompt

        if user_message.find("medicine notebook")!=-1:
            if_note=True

        if user_message.find("diagnose")!=-1:
            if_diagnose=True

        if user_message.find("suggestion")!=-1:
            if_suggestion=True


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
        global data_prompt,if_diagnose,if_note
        # Combine history conversation
        conversation = initial_prompt + " "
        for message in history:
            conversation += f"User: {message[0]}\n"
            if message[1] is not None:
                conversation += f"Bot: {message[1]}\n"
        #user_message = history[-1][0]
        if if_diagnose:
            conversation=insert_string(conversation,"User: yes",data_prompt)
        if if_note:
            prescription_data="Here are the prescriptions:"+read_prescriptions()+"."
            conversation=insert_string(conversation,"_base",prescription_data)
            
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




