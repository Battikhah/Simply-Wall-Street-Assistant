import requests
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

# Load environment variables from lock.env file
load_dotenv('lock.env')

# Load API key and endpoint from environment variables
api_key = os.getenv('Pro_API_Key')
api_endpoint = os.getenv('API_Endpoint')

# Define the headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def search_companies(query):
    search_query = """
    query searchCompanies($query: String!) {
      searchCompanies(query: $query) {
        id
        name
        exchangeSymbol
        tickerSymbol
      }
    }
    """
    variables = {"query": query}
    response = requests.post(api_endpoint, headers=headers, json={"query": search_query, "variables": variables})
    return response.json()

def get_company_info_by_id(company_id):
    company_query = """
    query Query($id: ID!) {
      company(id: $id) {
        id
        name
        tickerSymbol
      }
    }
    """
    variables = {"id": company_id}
    response = requests.post(api_endpoint, headers=headers, json={"query": company_query, "variables": variables})
    return response.json()

def get_company_info_by_ticker(exchange, symbol):
    ticker_query = """
    query companyByExchangeAndTickerSymbol($exchange: String!, $symbol: String!) {
      companyByExchangeAndTickerSymbol(exchange: $exchange, tickerSymbol: $symbol) {
        id
        name
        exchangeSymbol
        tickerSymbol
      }
    }
    """
    variables = {"exchange": exchange, "symbol": symbol}
    response = requests.post(api_endpoint, headers=headers, json={"query": ticker_query, "variables": variables})
    return response.json()

def list_exchanges():
    exchanges_query = """
    query {
      exchanges {
        symbol
      }
    }
    """
    response = requests.post(api_endpoint, headers=headers, json={"query": exchanges_query})
    return response.json()

def get_companies_by_exchange(exchange, limit, offset):
    companies_query = """
    query {
      companies(exchange: $exchange, limit: $limit, offset: $offset) {
        id
        name
        tickerSymbol
      }
    }
    """
    variables = {"exchange": exchange, "limit": limit, "offset": offset}
    response = requests.post(api_endpoint, headers=headers, json={"query": companies_query, "variables": variables})
    return response.json()

def execute_function():
    selected_function = function_combobox.get()
    param1 = param1_entry.get()
    param2 = param2_entry.get()
    param3 = param3_entry.get()

    if selected_function == "Search Companies":
        result = search_companies(param1)
    elif selected_function == "Get Company Info by ID":
        result = get_company_info_by_id(param1)
    elif selected_function == "Get Company Info by Ticker":
        result = get_company_info_by_ticker(param1, param2)
    elif selected_function == "List Exchanges":
        result = list_exchanges()
    elif selected_function == "Get Companies by Exchange":
        result = get_companies_by_exchange(param1, int(param2), int(param3))
    else:
        result = "Invalid function selected"

    formatted_result = json.dumps(result, indent=4)
    messagebox.showinfo("Result", formatted_result)

def update_param_visibility(event):
    selected_function = function_combobox.get()
    if selected_function in ["Get Company Info by Ticker"]:
        param2_label.grid()
        param2_entry.grid()
    elif selected_function in ["Get Companies by Exchange"]:
        param3_label.grid()
        param3_entry.grid()
        param4_label.grid()
        param4_entry.grid()
    else:
        param2_label.grid_remove()
        param2_entry.grid_remove()
        param3_label.grid_remove()
        param3_entry.grid_remove()
        param4_label.grid_remove()
        param4_entry.grid_remove()

# Create the main window
root = tk.Tk()
root.title("API Function Selector")

# Create and place the function selection combobox
function_label = tk.Label(root, text="Select Function:")
function_label.grid(row=0, column=0, padx=10, pady=10)
function_combobox = ttk.Combobox(root, values=[
    "Search Companies",
    "Get Company Info by ID",
    "Get Company Info by Ticker",
    "List Exchanges",
    "Get Companies by Exchange"
])
function_combobox.grid(row=0, column=1, padx=10, pady=10)
function_combobox.bind("<<ComboboxSelected>>", update_param_visibility)

# Create and place the parameter entry fields
param1_label = tk.Label(root, text="Name:")
param1_label.grid(row=1, column=0, padx=10, pady=10)
param1_entry = tk.Entry(root)
param1_entry.grid(row=1, column=1, padx=10, pady=10)

param2_label = tk.Label(root, text="Exchange:")
param2_label.grid(row=2, column=0, padx=10, pady=10)
param2_entry = tk.Entry(root)
param2_entry.grid(row=2, column=1, padx=10, pady=10)

param3_label = tk.Label(root, text="Limit:")
param3_label.grid(row=3, column=0, padx=10, pady=10)
param3_entry = tk.Entry(root)
param3_entry.grid(row=3, column=1, padx=10, pady=10)

param4_label = tk.Label(root, text="Offset:")
param4_label.grid(row=4, column=0, padx=10, pady=10)
param4_entry = tk.Entry(root)
param4_entry.grid(row=4, column=1, padx=10, pady=10)

# Initially hide param2 and param3
param2_label.grid_remove()
param2_entry.grid_remove()
param3_label.grid_remove()
param3_entry.grid_remove()
param4_entry.grid_remove()
param4_label.grid_remove()

# Create and place the execute button
execute_button = tk.Button(root, text="Execute", command=execute_function)
execute_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()