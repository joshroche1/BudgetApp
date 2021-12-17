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
	
	private double incomeTotal;
	private double expenseTotal;
	private double remainder;
  
	private String name;
	private String category;
	private String description;
	private String memo;
	private int duedate;
	private double value;
  
	public void setIncomeTotal(double val) { this.incomeTotal = val; }
	public void setExpenseTotal(double val) { this.expenseTotal = val; }
	public void setRemainder(double val) { this.remainder = val; }
	
	public void setName(String txt) { this.name = txt; }
	public void setDescription(String txt) { this.description = txt; }
  public void setMemo(String txt) { this.memo = txt; }
  public void setCategory(String txt) { this.category = txt; }
	public void setDueDate(int x) { this.duedate = x; }
	public void setValue(double val) { this.value = val; }
	
	public String getName() { return this.name; }
	public String getDescription() { return this.description; }
	public String getMemo() { return this.memo; }
	public String getCategory() { return this.category; }
	public int getDueDate() { return this.duedate; }
	public double getValue() { return this.value; }
  
	public double getIncomeTotal() { return this.incomeTotal; }
	public double getExpenseTotal() { return this.expenseTotal; }
	public double getRemainder() { return this.remainder; }
  
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
	
	public double getIncomeAmount() {
		double result = 0;
		try {
			DButil dbu = new DButil();
			rs = dbu.getIncomes();
			while (rs.next()) {
				result += rs.getDouble("value");
			}
		} catch (SQLException ex) {
			FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
		}
		return result;
	}
	public double getExpenseAmount() {
		double result = 0;
		try {
			DButil dbu = new DButil();
			rs = dbu.getExpenses();
			while (rs.next()) {
				result += rs.getDouble("value");
			}
		} catch (SQLException ex) {
			FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
		}
		return result;
	}
	public double getRemainderAmount(double in, double ex) {
		return in-ex;
	}
	
	public ResultSet getIncomes() {
		rs = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("SELECT name,value,description,memo FROM Income",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      rs = stmt.executeQuery();
    } catch (SQLException ex) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return rs;
	}
	public ResultSet getExpenses() {
		rs = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("SELECT name,duedate,value,description,category,memo FROM Expense",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      rs = stmt.executeQuery();
    } catch (SQLException ex) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return rs;
	}
  
  public ResultSet getBudget() {
    rs = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("*",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      rs = stmt.executeQuery();
    } catch (SQLException ex) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return rs;
  }  
}
