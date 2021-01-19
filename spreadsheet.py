
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import pprint
import json



def getClient():
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_key.json', scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)
    return client



def getInstance(x,client,sheetNo):
    # get the instance of the Spreadsheet
    sheet = client.open(x)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(sheetNo)
    return sheet_instance



def fetchRecords(sheet_instance):
    # get all the records of the data
    records_data = sheet_instance.get_all_records()
    # view the data
    return records_data



def clearSheet(sheet_instance):
    #Delete All Instances
    sheet_instance.delete_columns(2)
    sheet_instance.delete_columns(1)
    return True 



def insertDF(df,sheet_instance):
    set_with_dataframe(sheet_instance, df)
    return True

def insertDFs(df,sheet_instance):
    set_with_dataframe(sheet_instance, df)
    return True

if __name__ == "main":
    client = getClient()
    sheet_instance = getInstance('Last7Orders')
    records_data = fetchRecords(sheet_instance)
    #clearSheet(sheet_instance)
    #insertDF(df)






