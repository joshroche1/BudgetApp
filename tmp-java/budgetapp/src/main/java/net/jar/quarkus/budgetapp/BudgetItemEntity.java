package net.jar.quarkus.budgetapp;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class BudgetItemEntity extends PanacheEntity {

  public String name;
  public String description;
  public String category;
  public double amount;
  public String currency;
  public String recurrence;
  public int recurenceday;
  public Long budgetid;

}