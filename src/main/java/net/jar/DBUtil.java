package net.jar;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.PreparedStatement;
import java.sql.DriverManager;
import java.sql.SQLException;
import javax.faces.application.FacesMessage;
import javax.faces.context.FacesContext;

public class DBUtil {
  
  private Connection connect() {
    Connection c = null;
    try {
      Class.forName("com.mysql.cj.jdbc.Driver");
      String url = "jdbc:mysql://localhost:3306/myRx";
      String user = "dbuser";
      String pass = "cmsc495";
      c = DriverManager.getConnection(url, user, pass);
    } catch (Exception e) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, e.getMessage(), "..."));
    }
    return c;
  }
  public ResultSet select(String selectors, String tablename, String criteria) {
    Connection c = null;
    ResultSet rs = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("SELECT ? FROM ? WHERE ?",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      stmt.setString(1, selectors);
      stmt.setString(2, tablename);
      stmt.setString(3, critera);
      rs = stmt.executeQuery();
    } catch (SQLException ex) {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return rs;
  }
  public String insert(String tablename, String record) {
    Connection c = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("INSERT INTO ? VALUES ?",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      stmt.setString(1,tablename);
      stmt.setString(2,record);
      stmt.execute();
    } catch (SQLException ex) {
      System.out.println(ex.getMessage());
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return "";
  }
  public String delete(String tablename, String criteria) {
    Connection c = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("DELETE FROM ? WHERE ?",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      stmt.setString(1,tablename);
      stmt.setString(2,criteria);
      stmt.execute();
    } catch (SQLException ex) {
      System.out.println(ex.getMessage());
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return "";
  }
  public String update(String tablename, String values, String criteria) {
    Connection c = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("UPDATE ? SET ? WHERE ?",ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);
      stmt.setString(1,tablename);
      stmt.setString(2,values);
      stmt.setString(3,criteria);
      stmt.execute();
    } catch (SQLException ex) {
      System.out.println(ex.getMessage());
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_INFO, ex.getMessage(), "..."));
    }
    return "";
  }
  
  public Boolean validateUser(String user, String pass) {
    Connection c = null;
    ResultSet rs = null;
    try {
      c = this.connect();
      PreparedStatement stmt = c.prepareStatement("SELECT email FROM Users WHERE email=? AND password=?");
      stmt.setString(1, user);
      stmt.setString(2, pass);
      rs = stmt.executeQuery();
      stmt.close();
      c.close();
      if (rs != null) { 
        rs.close();
        return true; 
      }
    } catch (SQLException ex) {
      System.err.println(ex.getMessage());
    }
    return false;
  }
}
