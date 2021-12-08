package net.jar;

import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name="User")
public class User {
  
  private String email;
  private String password;
  private String phone;
  
  public void setEmail(String txt) { this.email = txt; }
  public void setPassword(String txt) { this.password = txt; }
  public void setPhone(String txt) { this.phone = txt; }
  
  public String getEmail() { return this.email; }
  public String getPassword() { return this.password; }
  public String getPhone() { return this.phone; }
    
}
