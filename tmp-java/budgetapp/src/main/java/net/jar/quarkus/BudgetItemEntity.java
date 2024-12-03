package net.jar.quarkus;

import jakarta.persistence.Entity;

import io.quarkus.hibernate.reactive.panache.PanacheEntity;

@Entity
public class BudgetItemEntity extends PanacheEntity {

  public String name;
  public Double amount;
  public String category;
  public String recurrence;
  public Integer recurrenceday;
  public Long budgetid;
  public String description;

}