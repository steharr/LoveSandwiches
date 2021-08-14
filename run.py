import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("Please enter sales date from today")
        print("Date should be six numbers separated by commas")
        print("Example: 10, 20, 45, 60, 87, 56")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(sep=",")

        if validate_data(sales_data):
            print('Data is valid!')
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into Integers
    Raises ValueError if strings cannot be converted into int,
    or if there arent exactly six values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Expected 6 values, values inputted: {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True


def update_worksheet(row_data, worksheet_name):
    """
    Update a specified worksheet, add new row with the list data provided.
    """
    print('updating sales worksheet...\n')
    worksheet = SHEET.worksheet(worksheet_name)
    worksheet.append_row(row_data, value_input_option='USER_ENTERED')
    print(f'{worksheet_name} worksheet updated successfully\n')


def calculate_surplus_data(sales_row):
    """
    Caculates the surplus between the stock available before a sales day
    and the number of items sold.
    """
    print("Calculating surplus\n")
    stocks = SHEET.worksheet('stock').get_all_values()
    stock_row = [int(num) for num in stocks[-1]]
    surplus_row = []

    # Calculate surplus: method 1 - (my own approach)
    # for sale_index, sale_val in enumerate(sales_row):
    #     surplus = stock_row[sale_index] - int(sale_val)
    #     surplus_row.append(surplus)

    # Calculate surplus: method 2 - (tutorial approach)
    for sale, stock in zip(sales_row, stock_row):
        surplus = stock - sale
        surplus_row.append(surplus)

    return surplus_row


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus, 'surplus')


print("Welcome to Love Sandwiches Data Automation")
main()
