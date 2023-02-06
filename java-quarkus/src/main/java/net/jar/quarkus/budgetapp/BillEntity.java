package net.jar.quarkus.budgetapp;

import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class BillEntity extends PanacheEntity {

  public String name;
  public String amount;
  public String recurrence;
  public String date_occurence;
  
  public static AccountEntity findByName(String name) {
    return find("name", name).firstResult();
  }

}