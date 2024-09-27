import pytest
import os
import csv
from datetime import datetime
from unittest.mock import patch, MagicMock
from app import (loaddata, csv_datasave, user_authenticity as login, monthly_sales_analysis,
                 price_analysis, weekly_sales_analysis, total_sales_amt as total_sales_amount_analysis,
                 all_branches_monthsales as all_branches_monthly_sales_analysis, AddBranchCommand, AddSaleCommand,
                 MonthlySalesAnalysisCommand, PriceAnalysisCommand, WeeklySalesAnalysisCommand,
                 TotalSalesAmountAnalysisCommand, AllBranchesMonthlySalesAnalysisCommand)

# Constants for test files
TEST_USER_FILE = "test_users.csv"
TEST_BRANCHES_FILE = "test_branches.csv"
TEST_PRODUCTS_FILE = "test_products.csv"
TEST_SALES_FILE = "test_sales.csv"

# Helper function to clear test files
def clear_test_files():
    for file in [TEST_USER_FILE, TEST_BRANCHES_FILE, TEST_PRODUCTS_FILE, TEST_SALES_FILE]:
        if os.path.exists(file):
            os.remove(file)

# Helper function to initialize test files
def initialize_test_files():
    headers_users = ['Username', 'Password']
    data_users = [['testuser', 'testpass']]
    csv_datasave(TEST_USER_FILE, data_users, headers=headers_users)

    headers_branches = ['Branch ID', 'Branch Name', 'Location']
    data_branches = [['5', 'Branch A', 'Location A']]
    csv_datasave(TEST_BRANCHES_FILE, data_branches, headers=headers_branches)

    headers_products = ['Product ID', 'Product Name']
    data_products = [['5', 'Product A']]
    csv_datasave(TEST_PRODUCTS_FILE, data_products, headers=headers_products)

    headers_sales = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
    data_sales = [['5', '5', '240', datetime.now().strftime('%Y-%m-%d')]]
    csv_datasave(TEST_SALES_FILE, data_sales, headers=headers_sales)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    clear_test_files()
    initialize_test_files()
    yield
    clear_test_files()

def test_load_data():
    data = loaddata(TEST_USER_FILE)
    assert len(data) == 1
    assert data[0] == ['testuser', 'testpass']

def test_save_data():
    new_data = [['5', 'Branch B', 'Location B']]
    csv_datasave(TEST_BRANCHES_FILE, new_data)
    data = loaddata(TEST_BRANCHES_FILE)
    assert len(data) == 2
    assert data[1] == ['5', 'Branch B', 'Location B']

def test_login_success():
    with patch('builtins.input', side_effect=['testuser', 'testpass']):
        result = login()
        assert result == True, f"Expected True but got {result}"

def test_login_failure():
    with patch('builtins.input', side_effect=['invaliduser', 'invalidpass']):
        result = login()
        assert result == False, f"Expected False but got {result}"

def test_monthly_sales_analysis():
    try:
        monthly_sales_analysis('5')
    except Exception as e:
        pytest.fail(f"monthly_sales_analysis raised an exception: {e}")

def test_price_analysis():
    try:
        price_analysis('5')
    except Exception as e:
        pytest.fail(f"price_analysis raised an exception: {e}")

def test_weekly_sales_analysis():
    try:
        weekly_sales_analysis()
    except Exception as e:
        pytest.fail(f"weekly_sales_analysis raised an exception: {e}")

def test_total_sales_amount_analysis():
    try:
        total_sales_amount_analysis()
    except Exception as e:
        pytest.fail(f"total_sales_amount_analysis raised an exception: {e}")

def test_all_branches_monthly_sales_analysis():
    try:
        all_branches_monthly_sales_analysis()
    except Exception as e:
        pytest.fail(f"all_branches_monthly_sales_analysis raised an exception: {e}")

@patch('app.input', side_effect=['5', 'Branch B', 'Location B'])
def test_add_branch_command(mock_input):
    command = AddBranchCommand()
    with patch('sys.stdout', new=MagicMock()):
        command.execute()
    # Ensure the new branch was added
    data = loaddata(TEST_BRANCHES_FILE)
    assert len(data) == 2
    assert data[1] == ['5', 'Branch B', 'Location B']

@patch('app.input', side_effect=['5', '5', '240'])
def test_add_sale_command(mock_input):
    command = AddSaleCommand()
    with patch('sys.stdout', new=MagicMock()):
        command.execute()
    # Ensure the new sale was added
    data = loaddata(TEST_SALES_FILE)
    assert len(data) == 2, f"Expected 2 entries but got {len(data)}"
    assert data[1][:4] == ['5', '5', '240']

def test_monthly_sales_analysis_command():
    command = MonthlySalesAnalysisCommand('5')
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"MonthlySalesAnalysisCommand raised an exception: {e}")

def test_price_analysis_command():
    command = PriceAnalysisCommand('5')
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"PriceAnalysisCommand raised an exception: {e}")

def test_weekly_sales_analysis_command():
    command = WeeklySalesAnalysisCommand()
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"WeeklySalesAnalysisCommand raised an exception: {e}")

def test_total_sales_amount_analysis_command():
    command = TotalSalesAmountAnalysisCommand()
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"TotalSalesAmountAnalysisCommand raised an exception: {e}")

def test_all_branches_monthly_sales_analysis_command():
    command = AllBranchesMonthlySalesAnalysisCommand()
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"AllBranchesMonthlySalesAnalysisCommand raised an exception: {e}")
