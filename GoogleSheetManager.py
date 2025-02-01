import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsManager:
    def __init__(self, credentials_file, spreadsheet_id):
        """Initialize Google Sheets API client."""
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(spreadsheet_id).sheet1

    def add_ingredient(self, name, expiry_date="Unknown", quantity=1):
        """Adds or updates an ingredient in Google Sheets."""
        data = self.sheet.get_all_records()

        for i, row in enumerate(data):
            if row["Item Name"].lower() == name.lower():
                self.sheet.update_cell(i+2, 2, row["Quantity"] + quantity)
                self.sheet.update_cell(i+2, 3, expiry_date)
                return

        # If item not found, append a new row
        self.sheet.append_row([name, quantity, expiry_date])

    def get_inventory(self):
        """Fetches all stored ingredients from Google Sheets."""
        return self.sheet.get_all_records()
