package net.jar.quarkus.smc;


import java.util.List;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;


@Entity
public class SystemImportEntity extends PanacheEntity {
  
  public String machineid;
  public String hostname;
  public String provider;
  public String datacenter;
  public String category;   // type in CSV
  public String role;
  public String zone;
  public String cores;
  public String memory;
  public String ipaddress;
  public String address;
  public String os;
  public String country;
  
}