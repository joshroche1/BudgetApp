#

def TestData():
  data = [
    ["2024-01-01", "Rent", "678.90"],
    ["2024-01-02", "Electricity", "234.56"],
    ["2024-01-03", "Utilities", "123.45"],
    ["2024-01-04", "Groceries", "98.76"],
    ["2024-01-05", "Phone", "56.78"]
  ]
  return data

def TestHeaders():
  headers = ["Date", "Name", "Amount"]
  return headers

def BudgetData():
  return {
    "headers": ["Name", "Description", "Currency"],
    "data": [
      ["Default", "Default Budget", "EUR"]
    ]
  }

def AccountData():
  return {
    "headers": ["Name", "Description", "Type", "Currency"],
    "data": [
      ["KSBB", "Kriessparkasse Boeblingen", "Checking", "EUR"]
    ]
  }

def TxactionData():
  return {
    "headers": ["Timestamp", "Amount", "Currency", "Category", "Name", "Description", "Account"],
    "data": [
      ["2024-01-02 10:11:12", "987.65", "EUR", "Housing", "Rent", "Transfer", "KSBB"],
      ["2024-01-03 09:08:07", "210.98", "EUR", "Electric", "EnBW", "SEPA", "KSBB"],
      ["2024-01-04 15:16:17", "95.85", "EUR", "Phone", "Telekom Mobile", "SEPA", "KSBB"],
      ["2024-01-05 11:22:33", "85.56", "EUR", "Food", "Edeka", "PoS Entry", "KSBB"],
      ["2024-01-06 17:18:19", "115.55", "EUR", "Internet", "Telekom", "SEPA", "KSBB"],
    ]
  }

