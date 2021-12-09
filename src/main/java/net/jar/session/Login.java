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
  private String seesionToken = "";

  public void setEmail(String em) { this.email = em;}
  public void setPassword(String pass) { this.password = pass;}
  public void setSessionToken(String txt) { this.sessionToken = txt;}

  public String getEmail() { return this.email; }
  public String getPassword() { return this.password; }
  public String getSessionToken() { return this.sessionToken; }

  public String getCurrentSession() {
    String result = "";
    HttpSession ses = SessionUtils.getSession();
    result = ses.getAttribute("usertoken").toString();
    setSessionToken(result);
    return result;
  }

  public String validateLogin() {
    DBUtil dbu = new DBUtil();
    boolean valid = dbu.validateUser(email, password);
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
