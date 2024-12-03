package net.jar.quarkus;

import jakarta.persistence.Entity;
import io.quarkus.security.jpa.Username;
import io.quarkus.security.jpa.Password;
import io.quarkus.security.jpa.Roles;
import io.quarkus.security.jpa.UserDefinition;
import io.quarkus.hibernate.reactive.panache.PanacheEntity;

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

}