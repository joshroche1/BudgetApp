package net.jar;

import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name="Budget")
public class Budget {
  
  private String name;
  private int duedate;
  private double value;
  private String description;
  private String category;
  private String memo;
  
  public void setName(String txt) { this.name = txt; }
  public void setDuedate(int dt) { this.duedate = dt; }
  public void setValue(double val) { this.value = val; }
  public void setDescription(String txt) { this.description = txt; }
  public void setCategory(String txt) { this.category = txt; }
  public void setMemo(String txt) { this.memo = txt; }
  
  public String getName() { return this.name; }
  public int getDuedate() { return this.duedate; }
  public double getValue() { return this.value; }
  public String getDescription() { return this.description; }
  public String getCategory() { return this.category; }
  public String getMemo() { return this.memo; }
  
}
