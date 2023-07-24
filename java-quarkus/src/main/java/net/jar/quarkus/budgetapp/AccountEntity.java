package net.jar.quarkus.budgetapp;


import java.util.List;
import javax.persistence.Column;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class AccountEntity extends PanacheEntity {

  public String name;
  public String accounttype;
  public String currency;
  public String country;
  
  public static AccountEntity findByName(String name) {
    return find("name", name).firstResult();
  }
  
  public static List<AccountEntity> findByType(String accounttype) {
    return list("accounttype", accounttype);
  }
  
  public static List<AccountEntity> findByCurrency(String currency) {
    return list("currency", currency);
  }
  
  public static List<AccountEntity> findByCountry(String country) {
    return list("country", country);
  }
  
}