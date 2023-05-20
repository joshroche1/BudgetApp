package net.jar.quarkus.smc;


import java.util.List;
import javax.persistence.Column;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;


@Entity
public class PlaybookEntity extends PanacheEntity {

  public String filename;
  @Column(length = 8191)
  public String content;
  public String category;
  public String groups;
  public String notes;
  
  public static PlaybookEntity findByFilename(String filename) {
    return find("filename", filename).firstResult();
  }
  
  public static List<PlaybookEntity> findByGroup(String group) {
    return list("groups", group);
  }
  
  public static List<PlaybookEntity> findByCategory(String category) {
    return list("category", category);
  }
    
}