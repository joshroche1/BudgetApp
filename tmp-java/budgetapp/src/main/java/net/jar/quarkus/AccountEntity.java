package net.jar.quarkus;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class AccountEntity extends PanacheEntity {

  public String name;
  public String description;
  public String accounttype;
  public String currency;
  public String notes;

}