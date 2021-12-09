package net.jar;

//import

import net.jar.session.Login;
import net.jar.entity.User;
import net.jar.entity.Transaction;
import net.jar.entity.Budget;

@Stateful
@Named("beanUser")
public class UserBean {
  
  private String email;
  private String password;
  private String phone;
  
  public void setEmail(String txt) { this.email = txt; }
  public void setPassword(String txt) { this.password = txt; }
  public void setPhone(String txt) { this.phone = txt; }
  
  public String getEmail() { return this.email; }
  public String getPassword() { return this.password; }
  public String getPhone() { return this.phone; }
  
  public String login() {
    
    return "index";
  }
  public String register() {
    
    return "index";
  }
  public String getCurrentBudget() {
    
    return "";
  }
}
