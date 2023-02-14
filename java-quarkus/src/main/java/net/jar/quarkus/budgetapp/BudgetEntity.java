package net.jar.quarkus.budgetapp;

import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class BudgetEntity extends PanacheEntity {

  public String name;
  public boolean active;
  public String month;  // JAN, FEB, ...
  public String year;  // 2023, 2024, ...
  public String incometotal;
  public String billtotal;
  public String remainder; 
  
  public static BudgetEntity findByName(String name) {
    return find("name", name).firstResult();
  }

}