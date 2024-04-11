import openai
import pandas as pd

openai.api_key = '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'

def Generate_report():
    df=pd.read_excel("data.xlsx")

    # Convert the DataFrame to a text format suitable for the OpenAI API
    input_text = df.to_markdown(index=False)  # You can use other formats like to_csv, to_json, etc.
    prompt=f"""You are an assistant with expertise in finance and data analysis. A user requires comprehensive financial analysis based on the provided data.

    The data provided in the Excel file contains financial information organized in a structured format. Each column represents a specific financial metric or category, and each row corresponds to a distinct observation or time period.

    Before generating the report, ensure thorough interpretation of the data. Analyze each column to understand the meaning and relevance of the financial metrics it represents. Consider any special instructions or conventions regarding the data presentation.

    Please proceed with the financial analysis using the data provided below, nut read the entire prompt first then start exicution, now analyse the data given between triple backticks:

    {input_text}

    After understanding the data thoroughly, generate a detailed report encompassing key insights, trends, and recommendations based on the analysis.
    
    For example if the user has spent too much on food than suggest him/her to try to reduce their junk food consumption,
    
    or if they have done an investment in that month then mention some tips for investments too, if they are using too much on utility then mention it and ask them to try to use public transport or something to reduce cost.
    
    Also make sure you add your own knowledge too for suggesting and generating report.
    
    If you are giving output in point format then make sure that all points are on different lines and not in same para.
    
    Make a report using your own knowledge and the examples given, but make sure the entire report fits within 500 words(Do Not exceed this limit and Do not give half sentences)
    
    For that you can probably make a detailed report and then return only a summary of it instead of the entire report, make sure you follow the word limit and do not give halfly written sentences.
    
    To avoid halfly written sentences you can first generate the entire thing in keywords and key sentences format then compress, concatinate and summarise all the sentences in one para.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":"You are an assistant who is finance and data analysis expert"},
            {"role":"user","content":prompt}],
        max_tokens=1000,
        n=1,
        temperature=0
    )

    generated_analysis = response.choices[0].message.content
    return generated_analysis
