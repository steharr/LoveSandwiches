import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales date from today")
    print("Date should be six numbers separated by commas")
    print("Example: 10, 20, 45, 60, 87, 56")

    data_str = input("Enter your data here:\n")

    sales_data = data_str.split(sep=",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values into Integers
    Raises ValueError if strings cannot be converted into int,
    or if there arent exactly six values
    """
    try:
        [int(values) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Expected 6 values, values inputted: {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")


get_sales_data()
