import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QStatusBar,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

ACCOUNTTABLEHEADERS = ["id", "name", "description", "accounttype", "currency", "ownerid"]
BUDGETTABLEHEADERS = ["id","name","description","currency","ownerid"]
TXTABLEHEADERS = ["id", "datetimestamp", "amount", "convertedvalue", "category", "currency", "name", "description", "accountid"]

class DataTableView(QTableWidget):
  def __init__(self, data, headers, *args):
    QTableWidget.__init__(self, *args)
    self.data = data
    self.headers = headers
    self.setData()
    self.resizeColumnsToContents()
    self.resizeRowsToContents()

  def setData(self):
    tableHeaders = []
    for rownum in range(len(self.data)):
      for index in range(len(self.data[rownum])):
        newitem = QTableWidgetItem(self.data[rownum][index])
        self.setItem(rownum, index, newitem)
    self.setHorizontalHeaderLabels(self.headers)


class TabView(QTabWidget):
  def __init__(self, budgetdata, accountdata, txdata, parent = None):
    super(TabView, self).__init__(parent)
    self.tab1 = QWidget()
    self.tab2 = QWidget()
    self.tab3 = QWidget()
    self.addTab(self.tab1, "Budgets")
    self.addTab(self.tab2, "Accounts")
    self.addTab(self.tab3, "Transactions")
    self.tab1UI(budgetdata)
    self.tab2UI(accountdata)
    self.tab3UI(txdata)
    self.setWindowTitle("Tab Demo")
    self.show()
    
  def tab1UI(self, budgetdata):
    budgetlayout = QVBoxLayout()
    budgettableview = DataTableView(budgetdata, BUDGETTABLEHEADERS, len(budgetdata), len(BUDGETTABLEHEADERS))
    budgetlayout.addWidget(budgettableview)
    self.setTabText(0, "Budgets")
    self.tab1.setLayout(budgetlayout)

  def tab2UI(self, accountdata):
    accountlayout = QVBoxLayout()
    accounttableview = DataTableView(accountdata, ACCOUNTTABLEHEADERS, len(accountdata), len(ACCOUNTTABLEHEADERS))
    accountlayout.addWidget(accounttableview)
    self.setTabText(1, "Accounts")
    self.tab2.setLayout(accountlayout)

  def tab3UI(self, txdata):
    txlayout = QVBoxLayout()
    txtableview = DataTableView(txdata, TXTABLEHEADERS, len(txdata), len(TXTABLEHEADERS))
    txlayout.addWidget(txtableview)
    self.setTabText(2, "Transactions")
    self.tab3.setLayout(txlayout)


class MainWindow(QMainWindow):
  def __init__(self, budgetdata, accountdata, txdata):
    super().__init__()
    mainlayout = QVBoxLayout()
    self.path = None
    container = TabView(budgetdata, accountdata, txdata)
    #container = QWidget()
    self.setCentralWidget(container)
    self.status = QStatusBar()
    self.setStatusBar(self.status)
    self.initToolBar()
    self.update_title()
    self.show()

  def initToolBar(self):
    file_toolbar = QToolBar("File")
    file_toolbar.setIconSize(QSize(14, 14))
    self.addToolBar(file_toolbar)
    file_menu = self.menuBar().addMenu("&File")
    open_file_action = QAction(
      "Open",
      self,
    )
    open_file_action.setStatusTip("Open file")
    open_file_action.triggered.connect(self.file_open)
    file_menu.addAction(open_file_action)
    file_toolbar.addAction(open_file_action)
    save_file_action = QAction("Save", self)
    save_file_action.setStatusTip("Save current page")
    save_file_action.triggered.connect(self.file_save)
    file_menu.addAction(save_file_action)
    file_toolbar.addAction(save_file_action)
    saveas_file_action = QAction(
      "Save As",
      self,
    )
    saveas_file_action.setStatusTip("Save current page to specified file")
    saveas_file_action.triggered.connect(self.file_saveas)
    file_menu.addAction(saveas_file_action)
    file_toolbar.addAction(saveas_file_action)
    print_action = QAction(
      "Print",
      self,
    )
    print_action.setStatusTip("Print current page")
    print_action.triggered.connect(self.file_print)
    file_menu.addAction(print_action)
    file_toolbar.addAction(print_action)
    edit_toolbar = QToolBar("Edit")
    edit_toolbar.setIconSize(QSize(16, 16))
    self.addToolBar(edit_toolbar)
    edit_menu = self.menuBar().addMenu("&Edit")
    edit_menu.addSeparator()
    wrap_action = QAction(
      "Wrap text to window",
      self,
    )
    wrap_action.setStatusTip("Toggle wrap text to window")
    wrap_action.setCheckable(True)
    wrap_action.setChecked(True)
    wrap_action.triggered.connect(self.edit_toggle_wrap)
    edit_menu.addAction(wrap_action)

  def dialog_critical(self, s):
    dlg = QMessageBox(self)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Icon.Critical)
    dlg.show()

  def file_open(self):
    path, _ = QFileDialog.getOpenFileName(
      self,
      "Open file",
      "",
      "Text documents (*.txt);;All files (*.*)",
    )
    if path:
      try:
        with open(path, "rU") as f:
          text = f.read()
      except Exception as e:
        self.dialog_critical(str(e))
      else:
        self.path = path
        self.editor.setPlainText(text)
        self.update_title()

  def file_save(self):
    if self.path is None:
      # If we do not have a path, we need to use Save As.
      return self.file_saveas()

    self._save_to_path(self.path)

  def file_saveas(self):
    path, _ = QFileDialog.getSaveFileName(
      self,
      "Save file",
      "",
      "Text documents (*.txt);;All files (*.*)",
    )
    if not path:
            # If dialog is cancelled, will return ''
      return
    self._save_to_path(path)

  def _save_to_path(self, path):
    text = self.editor.toPlainText()
    try:
      with open(path, "w") as f:
        f.write(text)
    except Exception as e:
      self.dialog_critical(str(e))
    else:
      self.path = path
      self.update_title()

  def file_print(self):
    dlg = QPrintDialog()
    if dlg.exec_():
      self.editor.print_(dlg.printer())

  def update_title(self):
    self.setWindowTitle("%s - BudgetApp" % (os.path.basename(self.path) if self.path else "Untitled"))

  def edit_toggle_wrap(self):
    self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)



