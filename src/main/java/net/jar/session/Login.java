package net.jar.session;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.context.FacesContext;
import javax.servlet.http.HttpSession;

import net.jar.datasource.DBUtil;
import net.jar.session.SessionUtils;

@ManagedBean(name = "beanLogin", eager = true)
@SessionScoped
public class Login {

  private String email = "";
  private String password = "";

  public void setEmail(String em) { this.email = em;}
  public void setPassword(String pass) { this.password = pass;}

  public String getEmail() { return this.email; }
  public String getPassword() { return this.password; }

  public String getCurrentSession() {
    String result = "";
    HttpSession ses = SessionUtils.getSession();
    String temp = ses.getAttribute("usertoken").toString();
    user += "" + temp;
    return result;
  }

  public String validateLogin() {
    boolean valid = DAOlogin.validatePatient(username, password);
    if (valid) {
      HttpSession sess = SessionUtils.getSession();
      sess.setAttribute("usertoken", email);
      return "main";
    } else {
      FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(
                   FacesMessage.SEVERITY_WARN, "Incorrect username and/or password", "..."));
      return "login";
    }
  }
  
  public String logout() {
    HttpSession session = SessionUtils.getSession();
    session.invalidate();
    return "index";
  }
}
