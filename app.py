import json
from flask import Flask, request
import pandas as pd
import datetime
from spreadsheet import *
from recommend import *

weekday = datetime.datetime.today().weekday()
crosstab = pd.read_csv(r"E:\Projects\Burito Recommendation\crosstab.csv")

app = Flask(__name__)

def multiplyList(myList) :
     
    # Multiply elements one by one
    result = 1
    for x in myList:
         result = result * x 
    return result 


@app.route('/webhook', methods = ['POST'])
def webhook():
    #get request
    """
    req = request.get_json(silent=True,force=True)
    req = req.get('queryResult')
    nums = req.get("parameters").get("number")
    """

    req = request.get_json(silent=True,force=True)
    foodtype_json = req.get("queryResult").get("outputContexts")[0]
    foodtype = foodtype_json.get("parameters").get("foodtype")
    

    query = req.get('query')
    
    # Google API
    client = getClient()
    sheet_instance = getInstance('Last7Orders',client)
    records_data = fetchRecords(sheet_instance)
    df = pd.DataFrame(records_data)
    # Google API
    
    if foodtype !="":
        yesterday = df["Orders"].iloc[-1]
        yesterday = ">>".join(yesterday.split("&&"))
        lastWeek = df["Orders"].iloc[weekday]
        lastWeek = ">>".join(lastWeek.split("&&"))
        fulfillmentText =  "Yestreday you had " +str(yesterday) +" and last week same day " +str(lastWeek) + "\n What should I use as refrence?"
        return {"fulfillmentText":fulfillmentText,
                "displayText":25,
                "source":"webhookdata"}

    if query == "yesterday":
        a = df["Orders"].iloc[-1]
        return ">>".join(a.split("&&"))

    if query == "last week":
        a = df["Orders"].iloc[weekday]
        return ">>".join(a.split("&&"))
    
    if intent == "yesterday similar":
        recommendations = find_match(crosstab,df["Orders"].iloc[-1])
        a = SuggestSmilar(recommendations)

        return list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
    
    if intent == "yesterday opposite":
        recommendations = find_match(crosstab,df["Orders"].iloc[-1])
        a = SuggestDifferent(recommendations)
        return list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
    
    if intent == "last week similar":
        recommendations = find_match(crosstab,df["Orders"].iloc[weekday])
        a = SuggestSmilar(recommendations)
        return list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
    
    if intent == "last week opposite":
        recommendations = find_match(crosstab,df["Orders"].iloc[weekday])
        a = SuggestDifferent(recommendations)
        return list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
"""
    if req.get("parameters").get("operations") == "add":
        ad = sum(nums)
        fulfillmentText = "adiition is {}".format(ad)

    if req.get("parameters").get("operations") == "multiply":
            mul = multiplyList(nums)
            fulfillmentText = "product is {}".format(mul)
    else:
        fulfillmentText = "NONE"
        
    return {
        "fulfillmentText":fulfillmentText,
        "displayText":25,
        "source":"webhookdata"
    }
"""

if __name__ == '__main__':
    app.run()
