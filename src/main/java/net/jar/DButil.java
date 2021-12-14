package net.jar;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.PreparedStatement;
import java.sql.DriverManager;
import java.sql.SQLException;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.context.FacesContext;
import javax.servlet.http.HttpSession;


@ManagedBean(name = "beanDButil", eager = true)
public class DButil {

  private Connection c = null;
  private ResultSet rs = null;
  
  private String name;
  private int duedate;
  private double expected_value;
  private double value_jan;
  private double value_feb;
  private double value_mar;
  private double value_apr;
  private double value_may;
  private double value_jun;
  private double value_jul;
  private double value_aug;
  private double value_sep;
  private double value_oct;
  private double value_nov;
  private double value_dec;
  private String description;
  private String category;
  private String memo;
  
  public void setName(String txt) { this.name = txt; }
  public void setDueDate(int val) { this.duedate = val; }
  public void setExpected_value(double val) { this.expected_value = val; }
  public void setValue_jan(double val) { this.value_jan = val; }
  public void setValue_feb(double val) { this.value_feb = val; }
  public void setValue_mar(double val) { this.value_mar = val; }
  public void setValue_apr(double val) { this.value_apr = val; }
  public void setValue_may(double val) { this.value_may = val; }
  public void setValue_jun(double val) { this.value_jun = val; }
  public void setValue_jul(double val) { this.value_jul = val; }
  public void setValue_aug(double val) { this.value_aug = val; }
  public void setValue_sep(double val) { this.value_sep = val; }
  public void setValue_oct(double val) { this.value_oct = val; }
  public void setValue_nov(double val) { this.value_nov = val; }
  public void setValue_dec(double val) { this.value_dec = val; }
  public void setDescription(String txt) { this.description = txt; }
  public void setCategory(String txt) { this.category = txt; }
  public void setMemo(String txt) { this.memo = txt; }
  
  public String getName() { return this.name; }
  public int getDueDate() { return this.duedate; }
  public double getExpected_value() { return this.expected_value; }
  public double getValue_jan() { return this.value_jan; }
  public double getValue_feb() { return this.value_feb; }
  public double getValue_mar() { return this.value_mar; }
  public double getValue_apr() { return this.value_apr; }
  public double getValue_may() { return this.value_may; }
  public double getValue_jun() { return this.value_jun; }
  public double getValue_jul() { return this.value_jul; }
  public double getValue_aug() { return this.value_aug; }
  public double getValue_sep() { return this.value_sep; }
  public double getValue_oct() { return this.value_oct; }
  public double getValue_nov() { return this.value_nov; }
  public double getValue_dec() { return this.value_dec; }
  public String getDescription() { return this.description; }
  public String getCategory() { return this.category; }
  public String getMemo() { return this.memo; }
  
  public Connection connect() {
    try {
      Class.forName("com.mysql.cj.jdbc.Driver");
      String url = "jdbc:mysql://localhost:3306/budgetapp";
      String user = "budgetappuser";
      String pass = "budgetapppasswor";
      c = DriverManager.getConnection(url, user, pass);
    } catch (Exception e) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, e.getMessage(), "..."));
    }
    return c;
  }
  
  public ResultSet query(String sql) {
    Connection c = null;
    Statement stmt = null;
    ResultSet rs = null;
    c = this.connect();
    try {
      c.setAutoCommit(false);
      stmt = c.createStatement();
      rs = stmt.executeQuery(sql);
      stmt.close();
      c.close();
    } catch (SQLException e) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, e.getMessage(), "..."));
    }
    return rs;
  }
  
  public ResultSet select(String text) {
    try {
      Statement stmt = c.createStatement();
      rs = stmt.executeQuery(text);
    } catch (SQLException e) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, e.getMessage(), "..."));
    }
    return rs;  
  }
  
  public void closeRS() {
    try {
      rs.close();
    } catch (SQLException e) {
      e.printStackTrace();
    }  
  }
  public void close() {
	  try {
		  c.close();
	  } catch (SQLException e) {
		  FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, e.getMessage(), "..."));
	  }
  }
  
  public ResultSet getBudget() {
    rs = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("SELECT name,duedate,expected_value,value_jan,value_feb,value_mar,value_apr,value_may,value_jun,value_jul,value_aug,value_sep,value_oct,value_nov,value_dec,description,category,memo FROM Budget",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      rs = stmt.executeQuery();
    } catch (SQLException ex) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return rs;
  }
  
  public String updateBudget(String nam, String field, String content, double value) { 
    String var1 = "";
    String var2 = "";
    switch (field) {
      case "expected_value": var1 = "expected_value"; var2 = value; break;
      case "value_jan": var1 = "value_jan"; var2 = value; break;
      case "value_feb": var1 = "value_feb"; var2 = value; break;
      case "value_mar": var1 = "value_mar"; var2 = value; break;
      case "value_apr": var1 = "value_apr"; var2 = value; break;
      case "value_may": var1 = "value_may"; var2 = value; break;
      case "value_jun": var1 = "value_jun"; var2 = value; break;
      case "value_jul": var1 = "value_jul"; var2 = value; break;
      case "value_aug": var1 = "value_aug"; var2 = value; break;
      case "value_sep": var1 = "value_sep"; var2 = value; break;
      case "value_oct": var1 = "value_oct"; var2 = value; break;
      case "value_nov": var1 = "value_nov"; var2 = value; break;
      case "value_dec": var1 = "value_dec"; var2 = value; break;
      case "description": var1 = "description"; var2 = content; break;
      case "category": var1 = "category"; var2 = content; break;
      case "memo": var1 = "memo"; var2 = content; break;
      default: return "main";
    }
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("UPDATE Budget SET ?=? WHERE name=?",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      stmt.setString(1,var1);
      stmt.setString(2,var2);
      stmt.setString(3,nam);
      stmt.execute();
    } catch (SQLException ex) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
		resetValues();
    return "main";
  }
  
}
