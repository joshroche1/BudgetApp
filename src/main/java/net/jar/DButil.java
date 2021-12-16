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

import net.jar.Income;
import net.jar.Expense;

@ManagedBean(name = "beanDButil", eager = true)
public class DButil {

  private Connection c = null;
  private ResultSet rs = null;
	
	private double incomeTotal;
	private double expenseTotal;
	private double remainder;
  
  private double in_jan;
  private double in_feb;
  private double in_mar;
  private double in_apr;
  private double in_may;
  private double in_jun;
  private double in_jul;
  private double in_aug;
  private double in_sep;
  private double in_oct;
  private double in_nov;
  private double in_dec;
	private double ex_jan;
  private double ex_feb;
  private double ex_mar;
  private double ex_apr;
  private double ex_may;
  private double ex_jun;
  private double ex_jul;
  private double ex_aug;
  private double ex_sep;
  private double ex_oct;
  private double ex_nov;
  private double ex_dec;
  
  public void setIn_jan(double val) { this.in_jan = val; }
  public void setIn_feb(double val) { this.in_feb = val; }
  public void setIn_mar(double val) { this.in_mar = val; }
  public void setIn_apr(double val) { this.in_apr = val; }
  public void setIn_may(double val) { this.in_may = val; }
  public void setIn_jun(double val) { this.in_jun = val; }
  public void setIn_jul(double val) { this.in_jul = val; }
  public void setIn_aug(double val) { this.in_aug = val; }
  public void setIn_sep(double val) { this.in_sep = val; }
  public void setIn_oct(double val) { this.in_oct = val; }
  public void setIn_nov(double val) { this.in_nov = val; }
  public void setIn_dec(double val) { this.in_dec = val; }
  public void setEx_jan(double val) { this.ex_jan = val; }
  public void setEx_feb(double val) { this.ex_feb = val; }
  public void setEx_mar(double val) { this.ex_mar = val; }
  public void setEx_apr(double val) { this.ex_apr = val; }
  public void setEx_may(double val) { this.ex_may = val; }
  public void setEx_jun(double val) { this.ex_jun = val; }
  public void setEx_jul(double val) { this.ex_jul = val; }
  public void setEx_aug(double val) { this.ex_aug = val; }
  public void setEx_sep(double val) { this.ex_sep = val; }
  public void setEx_oct(double val) { this.ex_oct = val; }
  public void setEx_nov(double val) { this.ex_nov = val; }
  public void setEx_dec(double val) { this.ex_dec = val; }
	public void setIncomeTotal(double val) { this.incomeTotal = val; }
	public void setExpenseTotal(double val) { this.expenseTotal = val; }
	public void setRemainder(double val) { this.remainder = val; }
  
  public double getIn_jan() { return this.in_jan; }
  public double getIn_feb() { return this.in_feb; }
  public double getIn_mar() { return this.in_mar; }
  public double getIn_apr() { return this.in_apr; }
  public double getIn_may() { return this.in_may; }
  public double getIn_jun() { return this.in_jun; }
  public double getIn_jul() { return this.in_jul; }
  public double getIn_aug() { return this.in_aug; }
  public double getIn_sep() { return this.in_sep; }
  public double getIn_oct() { return this.in_oct; }
  public double getIn_nov() { return this.in_nov; }
  public double getIn_dec() { return this.in_dec; }
	public double getEx_jan() { return this.ex_jan; }
  public double getEx_feb() { return this.ex_feb; }
  public double getEx_mar() { return this.ex_mar; }
  public double getEx_apr() { return this.ex_apr; }
  public double getEx_may() { return this.ex_may; }
  public double getEx_jun() { return this.ex_jun; }
  public double getEx_jul() { return this.ex_jul; }
  public double getEx_aug() { return this.ex_aug; }
  public double getEx_sep() { return this.ex_sep; }
  public double getEx_oct() { return this.ex_oct; }
  public double getEx_nov() { return this.ex_nov; }
  public double getEx_dec() { return this.ex_dec; }
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
      PreparedStatement stmt = c.prepareStatement("SELECT name,value,valuejan,valuefeb,valuemar,valueapr,valuemay,valuejun,valuejul,valueaug,valuesep,valueoct,valuenov,valuedec,description,memo FROM Income",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
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
      PreparedStatement stmt = c.prepareStatement("SELECT name,duedate,value,valuejan,valuefeb,valuemar,valueapr,valuemay,valuejun,valuejul,valueaug,valuesep,valueoct,valuenov,valuedec,description,category,memo FROM Expense",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
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
