import os
import sys

from PyQt5.QtWidgets import QApplication

from qtview import MainWindow

from testdata import TestData, TestHeaders


def main():
  testdata = TestData()
  testheaders = TestHeaders()
  app = QApplication(sys.argv)
  app.setApplicationName("BudgetApp")

  window = MainWindow(testdata, testheaders)
  app.exec_()

if __name__ == "__main__":
  main()
