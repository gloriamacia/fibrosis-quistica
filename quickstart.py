# importing the required libraries
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from os.path import join, dirname, realpath

def get_gspread(sheet_name):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    UPLOADS_PATH = join(dirname(realpath(__file__)), 'gsheet-db-315813-460e33e04984.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(UPLOADS_PATH, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1tp7IHOsGXQTsgIZIXj-Q_YI6A6EfUk-_A0U5tzzRkCM/edit#gid=2128225903')

    # get the first sheet of the Spreadsheet
    worksheet = sheet.worksheet(sheet_name)

    return pd.DataFrame(worksheet.get_all_records())
