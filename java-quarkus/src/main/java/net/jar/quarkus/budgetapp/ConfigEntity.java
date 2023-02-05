package net.jar.quarkus.budgetapp;

import java.util.List;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class ConfigEntity extends PanacheEntity {

  public String name;
  public String value;
  
  public static ConfigEntity findByName(String name) {
    return find("name", name).firstResult();
  }

}