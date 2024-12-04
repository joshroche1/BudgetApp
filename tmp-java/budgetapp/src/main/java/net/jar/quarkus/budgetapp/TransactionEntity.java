package net.jar.quarkus.budgetapp;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class TransactionEntity extends PanacheEntity {

  public String datetimestamp;
  public double amount;
  public double convertedamount;
  public String name;
  public String description;
  public String category;
  public String currency;
  public Long accountid;

}