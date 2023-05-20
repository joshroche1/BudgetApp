package net.jar.quarkus.smc;


import java.util.List;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;


@Entity
public class SystemEntity extends PanacheEntity {

  public String hostname;
  public String machineid;
  public String ipaddress;
  public String category;
  public String groups;
  public String notes;
  public String os;
  public String zone;
  public String role;
  public String provider;
  public String datacenter;
  public String country;
  
  public String cputype;
  public String cpuarch;
  public Integer cpucores;
  public String cpuspeed;
  
  public String memtotal;
  public String memtype;
  public Integer memnum;
  public String memsize;
  public String memspeed;
  
  public String disktotal;
  public Integer disknum;
  public String disktype;
  public String disksize;
  public String diskspeed;
  
  public static SystemEntity findByHostname(String hostname) {
    return find("hostname", hostname).firstResult();
  }
  
  public static List<SystemEntity> findByGroup(String group) {
    return list("groups", group);
  }
  
  public static List<SystemEntity> findByCategory(String category) {
    return list("category", category);
  }
  
  public static SystemEntity findByIP(String ipaddress) {
    return find("ipaddress", ipaddress).firstResult();
  }
  
  public static List<SystemEntity> findByZone(String zone) {
    return list("zone", zone);
  }
  
  public static List<SystemEntity> findByRole(String role) {
    return list("role", role);
  }
  
  public static List<SystemEntity> findByProvider(String provider) {
    return list("provider", provider);
  }
    
}