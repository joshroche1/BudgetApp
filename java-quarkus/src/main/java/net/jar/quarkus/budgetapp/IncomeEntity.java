package net.jar.quarkus.budgetapp;

import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class IncomeEntity extends PanacheEntity {

  public String name;
  public String incometype;
  public String amount;
  public String recurrence;  // Monthly, Bi-Weekly, Weekly, ...
  public String date_occurence;
  public boolean paid; 
  public boolean active; 
  
  public static IncomeEntity findByName(String name) {
    return find("name", name).firstResult();
  }

}