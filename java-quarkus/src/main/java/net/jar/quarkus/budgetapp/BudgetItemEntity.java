package net.jar.quarkus.budgetapp;


import java.util.List;
import javax.persistence.Column;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class BudgetItemEntity extends PanacheEntity {

  public String name;
  public Double amount;
  public Long budgetid;
  public String category;
  public String recurrence;
  public Integer recurrenceday;
  public String description;
  
  public static BudgetItemEntity findByName(String name) {
    return find("name", name).firstResult();
  }
    
  public static List<BudgetItemEntity> findByCategory(String category) {
    return list("category", category);
  }
  
  public static List<BudgetItemEntity> findByBudget(Long budgetid) {
    return list("budgetid", budgetid);
  }
  
}