import json
from flask import Flask, request
import pandas as pd
import datetime
from spreadsheet import *
from recommend import *

weekday = datetime.datetime.today().weekday()
crosstab = pd.read_csv("crosstab.csv")

app = Flask(__name__)

def find_j(outputContexts,context):
    a = []
    for i in outputContexts:
        a.append(i.get("name").split("/")[-1])
    ind = a.index(context)
    return outputContexts[ind]


@app.route('/webhook', methods = ['POST'])
def webhook():
    #get request
    """
    req = request.get_json(silent=True,force=True)
    req = req.get('queryResult')
    nums = req.get("parameters").get("number")
    """

    req = request.get_json(silent=True,force=True)
    outputContexts = req.get("queryResult").get("outputContexts")
    req_j = find_j(outputContexts,"request-followup")
    foodtype = req_j.get("parameters").get("foodtype")
    
    #refrence
    try:
        req_j = find_j(outputContexts,"refrence")
        refrence = req_j.get("parameters").get("date-time.original")
        print("*****************")
        print(refrence)
        print("*****************")
    
    except:
        print(1)
        refrence =""
    try:
        #prefrence
        req_j = find_j(outputContexts,"request-refrence-prefrence-followup")
        prefrence = req_j.get("parameters").get("prefrence")
        print(prefrence)
    except:
        print(2)
        prefrence =""
    try:
        req_j = find_j(outputContexts,"faccapetance")
        acceptance = req_j.get("parameters").get("acceptance")
        print(acceptance)
    except:
        print(3)
        acceptance = ""

    # Google API
    client = getClient()
    sheet_instance = getInstance('Last7Orders',client,0)
    records_data = fetchRecords(sheet_instance)
    df = pd.DataFrame(records_data)

    sheet_instance_suggestion = getInstance('Last7Orders',client,1)
    suggestionData = fetchRecords(sheet_instance_suggestion)
    df_s = pd.DataFrame(suggestionData)
    # Google API

    if acceptance == "yes":
        df.iloc[6,1] = df_s.iloc[0].values[0]
        insertDFs(df,sheet_instance)
        fulfillmentText = "Then " + str(df_s.iloc[0].values[0])+ " it is! Your record has been updated too!" 
        return {"fulfillmentText":fulfillmentText,
                "displayText":25,
                "source":"webhookdata"}

    if refrence.strip() == "yesterday": 
        if prefrence.strip() == "similar":
            recommendations = find_match(crosstab,df["Orders"].iloc[-1])
            a = SuggestSmilar(recommendations)
            suggestion = list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
            
            df_s.iloc[0] = list(a.index)[0]
            print(df_s)
            clearSheet(sheet_instance_suggestion)
            insertDFs(df_s,sheet_instance_suggestion)
            fulfillmentText = "I would suggest you to have " + suggestion +"/nIs it ok?"
            return {"fulfillmentText":fulfillmentText,
                    "displayText":25,
                    "source":"webhookdata"}
    
    if refrence.strip() == "yesterday":
        if prefrence.strip() == "different":
            recommendations = find_match(crosstab,df["Orders"].iloc[-1])
            a = SuggestDifferent(recommendations)
            suggestion = list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
            df_s.iloc[0] = list(a.index)[0]
            clearSheet(sheet_instance_suggestion)
            insertDFs(df_s,sheet_instance_suggestion)
            fulfillmentText = "I would suggest you to have " + suggestion +"/nIs it ok?"
            return {"fulfillmentText":fulfillmentText,
                    "displayText":25,
                    "source":"webhookdata"}
    
    if refrence.strip() == "last week":
        if prefrence.strip() == "similar":
            recommendations = find_match(crosstab,df["Orders"].iloc[weekday])
            a = SuggestSmilar(recommendations)
            suggestion = list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
            df_s.iloc[0] = list(a.index)[0]
            clearSheet(sheet_instance_suggestion)
            insertDFs(df_s,sheet_instance_suggestion)
            fulfillmentText = "I would suggest you to have " + suggestion + "/nIs it ok?"
            return {"fulfillmentText":fulfillmentText,
                    "displayText":25,
                    "source":"webhookdata"}
    
    if refrence.strip() == "last week" :
        if prefrence.strip() == "different":
            recommendations = find_match(crosstab,df["Orders"].iloc[weekday])
            a = SuggestDifferent(recommendations)
            df_s.iloc[0] = list(a.index)[0]
            clearSheet(sheet_instance_suggestion)
            insertDFs(df_s,sheet_instance_suggestion)
            suggestion = list(a.index)[0] + "Similarity Score: "+ str(a.iloc[0])
            fulfillmentText = "I would suggest you to have " + suggestion + "/nIs it ok?"
            return {"fulfillmentText":fulfillmentText,
                    "displayText":25,
                    "source":"webhookdata"}
    
    if refrence == "yesterday":
        a = df["Orders"].iloc[-1]
        refrence = ">>".join(a.split("&&"))
        fulfillmentText = "Your prefrence has been set as "+ str(refrence) + "." +"\n Would you like to have something similar or different?"
        return {"fulfillmentText":fulfillmentText,
                "displayText":25,
                "source":"webhookdata"} 


    if refrence == "last week":
        a = df["Orders"].iloc[weekday]
        refrence = ">>".join(a.split("&&"))
        fulfillmentText = "Your prefrence has been set as "+ str(refrence) + "." +"\n Would you like to have something similar or different?"
        return {"fulfillmentText":fulfillmentText,
                "displayText":25,
                "source":"webhookdata"} 



    if foodtype !="":
        yesterday = df["Orders"].iloc[-1]
        yesterday = ">>".join(yesterday.split("&&"))
        lastWeek = df["Orders"].iloc[weekday]
        lastWeek = ">>".join(lastWeek.split("&&"))
        fulfillmentText =  "Yestreday you had " +str(yesterday) +" and last week same day " +str(lastWeek) + "\n What should I use as refrence?"
        return {"fulfillmentText":fulfillmentText,
                "displayText":25,
                "source":"webhookdata"}

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
