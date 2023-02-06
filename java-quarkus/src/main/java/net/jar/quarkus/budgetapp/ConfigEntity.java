package net.jar.quarkus.budgetapp;

import java.util.List;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class ConfigEntity extends PanacheEntity {

  public String name;
  public String value;
  
  public static ConfigEntity findByValue(String value) {
    return find("value", value).firstResult();
  }
  
  public static List<ConfigEntity> findByName(String name) {
    return list("name", name);
  }

}