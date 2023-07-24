package net.jar.quarkus.budgetapp;


import java.util.List;
import javax.persistence.Column;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class BudgetEntity extends PanacheEntity {

  public String name;
  public String currency;
  public String description;
  
  public static BudgetEntity findByName(String name) {
    return find("name", name).firstResult();
  }
    
  public static List<BudgetEntity> findByCurrency(String currency) {
    return list("currency", currency);
  }
  
}