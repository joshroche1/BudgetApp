package budgetapp;

import java.awt.*;
import javax.swing.*;

public class AppUI {
  String windowTitle = "Java Swing Example";
  String longtext = "x2be3f143f0068721bc2ceb796e394f6733afeb693d4b700086b4ab770ee5e186";
  JFrame mainframe;
  JTextArea textarea;
  
  AppUI() {
    initUI();
  }

  public void initUI() {
    mainframe = new JFrame(windowTitle);
    mainframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    JPanel panel = new JPanel(new BorderLayout());
    panel.setBackground(Color.gray);
    textarea = new JTextArea(longtext);
    textarea.setBounds(10, 10, 300, 300);
    JPanel tab1 = new JPanel();
    JPanel tab2 = new JPanel();
    JPanel tab3 = new JPanel();
    tab1.add(textarea);
    JTabbedPane tabpane = new JTabbedPane();
    tabpane.setBounds(0, 0, 400, 400);
    tabpane.add("Tab 1", tab1);
    tabpane.add("Tab 2", tab2);
    tabpane.add("Tab 3", tab3);
    panel.add(tabpane);
    mainframe.add(panel);
    mainframe.setSize(400, 400);
    mainframe.setVisible(true);
  }
  
  public void setTextArea(String longtext) {
    mainframe.
  }
}

