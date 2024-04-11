import openai
import gradio as gr

openai.api_key='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'

message=[{"role":"system","content":"You are an assistant who is finance expert"},
         {"role":"user","content":"don't try to answer in a hurry, just read the entire prompt i provide first then understand my querry and then give an output. Also, remember to look for possible clues for my questions in some of the previous conversations with you."},
         {"role":"user","content":"I sometimes ask questions that are unrelated to finance, in that case kindly reply with something like \"i am a financial expert and such a doubt is beyond my field of experties\", just remember to be true and kind instead of feeding me lies."},
         {"role":"user","content":"Now i will start asking questions, and if there are more inputs after this you can reffer to them as examples to answer my next question. "}]
def ChatGPT(user_input):
    message.append({"role":"user","content":user_input})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=200,
        n=1,
        temperature=0
    )
    ChatGPT_reply=response.choices[0].message.content
    message.append({"role":"assistant","content":ChatGPT_reply})
    return ChatGPT_reply

with gr.Blocks() as block:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        bot_message = ChatGPT(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

block.launch(debug=True,server_port=7860)