
from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from Update_excel import add_spending
import openai
import gradio
openai.api_key='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'
from Analyst import Generate_report

app = Flask(__name__)

expenses = {'Food': 0, 'Transportation': 0, 'Utilities': 0, 'Entertainment': 0, 'Other': 0}

message=[{"role":"system","content":"You are an assistant who is finance expert"}]
def ChatGPT(user_input):
    message.append({"role":"user","content":user_input})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=50,
        n=1,
        temperature=0
    )
    ChatGPT_reply=response["choices"][0]["message"]["content"]
    message.append({"role":"assistant","content":ChatGPT_reply})
    return response
@app.route("/generate_report")
def ger():
    return Generate_report()
@app.route('/introvid')
def introvid():
    return render_template('https://youtu.be/2LECa5COVqY')
@app.route('/login_verify.php',methods=['POST'])
def login_v():
    return render_template('postjoin.html',expenses=expenses)
@app.route('/home_frame.html')
def homez():
    return render_template("home_frame.html",expenses=expenses)
@app.route('/chatbot.html')
def chatbot():
    demo=gradio.Interface(fn=ChatGPT, inputs="text", outputs="text", title="Your finance assistant")
    demo.launch(server_port=10000)
    return render_template("127.0.0.1:7860")
@app.route('/')
def index():    
    return render_template('1_newindex.html', expenses=expenses)
@app.route('/index.html')
def index2():
    return render_template('postjoin.html', expenses=expenses)

@app.route('/aboutus.html')
def aboutus():
    return render_template('1_newaboutus.html', expenses=expenses)
@app.route('/contactus.html')
def contactus():
    return render_template('1_newcontact.html') 
@app.route('/home.html')
def home():
    return render_template('1_newhome.html',expenses=expenses)

@app.route('/postjoin.html')
def postjoin():
    return render_template('postjoin.html',expenses=expenses)

@app.route('/joinus.html')
def joinus():   
    return render_template('1_newjoinus.html',expenses=expenses)

@app.route('/login.html',methods=['GET'])
def login():
    return render_template('login.html')

global df
global date
@app.route('/submit_expense', methods=['POST'])
def submit_expense():   
    category = request.form.get('category')
    amount = float(request.form.get('amount'))
    global df
    if category in expenses:
        expenses[category] += amount
    df=add_spending(category,amount)

    return render_template('1_newhome.html', expenses=expenses)

@app.route('/generate_graph')
def generate_graph():
    labels = list(expenses.keys())
    values = list(expenses.values())   #kaggle for ideas 
    plt.figure(figsize=(8, 6))
    df.plot(kind='bar',x='Date',stacked=True)
    # plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution')
    plt.xlabel("Date")
    plt.ylabel("Amoount of money")
    plt.xticks(rotation=0)
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    graph_url = base64.b64encode(img.getvalue()).decode()
    return f'<img src="data:image/png;base64,{graph_url}">'
    
if __name__ == '__main__':
    app.run(debug=True)