package net.jar.quarkus.budgetapp;

import java.util.List;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class AccountEntity extends PanacheEntity {

  public String name;
  public String number;
  public String iban;
  public String bic;
  public String type;
  public String address;
  public String city;
  public String state;
  public String country;
  public String api_credential;
  public String currency;
  public String telephone;
  
  public static AccountEntity findByName(String name) {
    return find("name", name).firstResult();
  }
  
  public static List<AccountEntity> findByType(String type) {
    return list("type", type);
  }

}