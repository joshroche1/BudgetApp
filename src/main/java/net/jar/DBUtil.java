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

public class DBUtil {
  
  public Connection connect() {
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
