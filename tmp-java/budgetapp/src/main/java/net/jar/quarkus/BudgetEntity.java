package net.jar.quarkus;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class BudgetEntity extends PanacheEntity {

  public String name;
  public String currency;
  public String description;
  public Long userid;

}