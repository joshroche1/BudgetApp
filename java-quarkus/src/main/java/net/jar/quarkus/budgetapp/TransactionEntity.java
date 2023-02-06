package net.jar.quarkus.budgetapp;

import java.util.Date;
import java.util.List;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class TransactionEntity extends PanacheEntity {

  public String name;
  public Date datetimestamp;
  public Double amount;
  public String description;
  public String category;
  public String reference;
  
  public static TransactionEntity findByName(String name) {
    return find("name", name).firstResult();
  }

  public static List<TransactionEntity> findByCategory(String category) {
    return list("category", category);
  }

}