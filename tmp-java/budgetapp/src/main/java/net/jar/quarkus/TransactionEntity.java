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
  public Long accountid;

  public static void add(String datetimestamp, String name, String description, String category, double amount, String currency) {
    TransactionEntity entity = new TransactionEntity();
	entity.datetimestamp = datetimestamp;
    entity.name = name;
    entity.category = category;
	entity.amount = amount;
    entity.currency = currency;
    entity.persist();
  }
}