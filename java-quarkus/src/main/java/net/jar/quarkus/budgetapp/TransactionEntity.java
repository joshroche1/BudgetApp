package net.jar.quarkus.budgetapp;


import java.util.List;
import javax.persistence.Column;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class TransactionEntity extends PanacheEntity {

  public String name;
  public String datetimestamp;
  public Double amount;
  public Long accountid;
  public String category;
  public String currency;
  public Integer recurrenceday;
  public String description;
  
  public static TransactionEntity findByName(String name) {
    return find("name", name).firstResult();
  }
    
  public static List<TransactionEntity> findByDatetimestamp(String datetimestamp) {
    return list("datetimestamp", datetimestamp);
  }
  
  public static List<TransactionEntity> findByCategory(Long category) {
    return list("category", category);
  }
  public static List<TransactionEntity> findByCurrency(Long currency) {
    return list("currency", currency);
  }
  
  public static List<TransactionEntity> findByAccountId(Long accountid) {
    return list("accountid", accountid);
  }
  
}