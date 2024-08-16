import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


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


class MainWindow(QMainWindow):
  def __init__(self, data, headers):
    super().__init__()

    layout = QVBoxLayout()
    
    self.path = None
    
    tablewidget = DataTableView(data, headers, len(data), len(headers))
    layout.addWidget(tablewidget)
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)

    self.status = QStatusBar()
    self.setStatusBar(self.status)

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

    self.update_title()
    self.show()

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

