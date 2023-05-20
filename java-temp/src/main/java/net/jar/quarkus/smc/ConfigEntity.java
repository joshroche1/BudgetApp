package net.jar.quarkus.smc;

import java.util.List;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class ConfigEntity extends PanacheEntity {

  public String name;
  public String value;
  
  public static ConfigEntity add(String name, String value) {
    ConfigEntity present = findByValue(value);
    if (present != null) {
      return present;
    }
    ConfigEntity entity = new ConfigEntity();
    entity.name = name;
    entity.value = value;
    entity.persist();
    return entity;
  }
  
  public static List<ConfigEntity> findByName(String name) {
    return list("name", name);
  }
  
  public static ConfigEntity findByValue(String value) {
    return find("value", value).firstResult();
  }

}