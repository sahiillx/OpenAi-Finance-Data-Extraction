import openai
from dotenv import load_dotenv
import os
import json
import pandas as pd   #Used to analyze data.


load_dotenv()
openai.api_key = os.getenv("api_key")

def extract_financial_data(text):
    promt = get_promt_financial() + text
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
        { "role": "user", "content": promt}
        ]    
    )
    content = response['choices'][0]['message']['content']

    # (Loads) string will convert that string into Dictionary Format
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])
    except(json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
    "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
    "Value": [" ", " ", " ", " ", " "]
    })


def get_promt_financial():
    return ''' Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============

    '''
    

if __name__ == '__main__':
    text = '''
            Apple today announced financial results for its fiscal 2023 third quarter ended July 1, 2023. The Company posted quarterly revenue of $81.8 billion, down 1 percent year over year, and quarterly earnings per diluted share of $1.26, up 5 percent year over year. 
            “We are happy to report that we had an all-time revenue record in Services during the June quarter, driven by over 1 billion paid subscriptions, and we saw continued strength in emerging markets thanks to robust sales of iPhone,” said Tim Cook, Apple’s CEO. “From education to the environment, we are continuing to advance our values, while championing innovation that enriches the lives of our customers and leaves the world better than we found it.”
            “Our June quarter year-over-year business performance improved from the March quarter, and our installed base of active devices reached an all-time high in every geographic segment,” said Luca Maestri, Apple’s CFO. “During the quarter, we generated very strong operating cash flow of $26 billion, returned over $24 billion to our shareholders, and continued to invest in our long-term growth plans.”
            Apple’s board of directors has declared a cash dividend of $0.24 per share of the Company’s common stock. The dividend is payable on August 17, 2023 to shareholders of record as of the close of business on August 14, 2023.
            Apple will provide live streaming of its Q3 2023 financial results conference call beginning at 2:00 p.m. PT on August 3, 2023 at apple.com/investor/earnings-call. The webcast will be available for replay for approximately two weeks thereafter.
            '''

    df = extract_financial_data(text)
    print(df.to_string())

