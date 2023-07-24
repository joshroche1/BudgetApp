package net.jar.quarkus.budgetapp;


import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import io.quarkus.elytron.security.common.BcryptUtil;
import io.quarkus.security.jpa.Password;
import io.quarkus.security.jpa.Roles;
import io.quarkus.security.jpa.UserDefinition;
import io.quarkus.security.jpa.Username;

@Entity
@UserDefinition
public class UserEntity extends PanacheEntity {

  @Username
  public String username;

  @Password
  public String password;
  
  @Roles
  public String role;
  
  public String email;


  public static void add(String username, String password, String role, String email) {
    UserEntity usernamepresent = find("username", username).firstResult();
    UserEntity emailpresent = find("email", email).firstResult();
    if (usernamepresent == null && emailpresent == null) {
      UserEntity user = new UserEntity();
      user.username = username;
      user.password = BcryptUtil.bcryptHash(password);
      user.role = role;
      user.email = email;
      user.persist();
    }
  }
  
  public static UserEntity findByUsername(String username) {
    return find("username", username).firstResult();
  }
  
  public static UserEntity findByEmail(String email) {
    return find("email", email).firstResult();
  }
  
}