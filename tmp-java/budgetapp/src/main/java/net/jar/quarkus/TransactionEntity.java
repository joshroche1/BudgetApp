package net.jar.quarkus;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class TransactionEntity extends PanacheEntity {

  public String datetimestamp;
  public String name;
  public String description;
  public String category;
  public double amount;
  public String currency;
  public String notes;

}