import os
import sys

from PyQt5.QtWidgets import QApplication

from qtview import MainWindow
from database import get_accounts, get_budgets, get_budgetitems, get_transactions
from testdata import TestData, TestHeaders, BudgetData, AccountData, TxactionData


def main():
  budgetlist = get_budgets()
  budgetitemlist = get_budgetitems()
  accountlist = get_accounts()
  txlist = get_transactions()
  txdata = TxactionData()
  app = QApplication(sys.argv)
  app.setApplicationName("BudgetApp")

  window = MainWindow(budgetlist, accountlist, txlist)
  app.exec_()

if __name__ == "__main__":
  main()
