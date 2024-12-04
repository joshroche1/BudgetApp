package net.jar.quarkus.budgetapp;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class UserEntity extends PanacheEntity {

  public String username;
  public String password;
  public String email;

}