package net.jar.entity;

import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name="Transaction")
public class Transaction {
  
  private String source;
  private Date datetime;
  private double value;
  private String description;
  private String category;
  private String memo;
  
  public void setSource(String txt) { this.source = txt; }
  public void setDate(Date dt) { this.datetime = dt; }
  public void setValue(double val) { this.value = val; }
  public void setDescription(String txt) { this.description = txt; }
  public void setCategory(String txt) { this.category = txt; }
  public void setMemo(String txt) { this.memo = txt; }
  
  public String getSource() { return this.source; }
  public Date getDate() { return this.datetime; }
  public double getValue() { return this.value; }
  public String getDescription() { return this.description; }
  public String getCategory() { return this.category; }
  public String getMemo() { return this.memo; }
  
}
