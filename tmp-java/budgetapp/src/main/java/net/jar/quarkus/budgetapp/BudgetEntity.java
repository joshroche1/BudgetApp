package net.jar.quarkus.budgetapp;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class BudgetEntity extends PanacheEntity {

  public String name;
  public String description;
  public String currency;
  public Long userid;

}