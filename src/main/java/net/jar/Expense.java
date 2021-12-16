package net.jar;

import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.context.FacesContext;
import javax.servlet.http.HttpSession;

public class Expense {
  
  private String name;
  private int duedate;
  private double value;
  private double valuejan;
  private double valuefeb;
  private double valuemar;
  private double valueapr;
  private double valuemay;
  private double valuejun;
  private double valuejul;
  private double valueaug;
  private double valuesep;
  private double valueoct;
  private double valuenov;
  private double valuedec;
  private String description;
  private String category;
  private String memo;
  
  public void setName(String txt) { this.name = txt; }
  public void setDueDate(int val) { this.duedate = val; }
  public void setValue(double val) { this.value = val; }
  public void setValuejan(double val) { this.valuejan = val; }
  public void setValuefeb(double val) { this.valuefeb = val; }
  public void setValuemar(double val) { this.valuemar = val; }
  public void setValueapr(double val) { this.valueapr = val; }
  public void setValuemay(double val) { this.valuemay = val; }
  public void setValuejun(double val) { this.valuejun = val; }
  public void setValuejul(double val) { this.valuejul = val; }
  public void setValueaug(double val) { this.valueaug = val; }
  public void setValuesep(double val) { this.valuesep = val; }
  public void setValueoct(double val) { this.valueoct = val; }
  public void setValuenov(double val) { this.valuenov = val; }
  public void setValuedec(double val) { this.valuedec = val; }
  public void setDescription(String txt) { this.description = txt; }
  public void setCategory(String txt) { this.category = txt; }
  public void setMemo(String txt) { this.memo = txt; }
  
  public String getName() { return this.name; }
  public int getDueDate() { return this.duedate; }
  public double getValue() { return this.value; }
  public double getValuejan() { return this.valuejan; }
  public double getValuefeb() { return this.valuefeb; }
  public double getValuemar() { return this.valuemar; }
  public double getValueapr() { return this.valueapr; }
  public double getValuemay() { return this.valuemay; }
  public double getValuejun() { return this.valuejun; }
  public double getValuejul() { return this.valuejul; }
  public double getValueaug() { return this.valueaug; }
  public double getValuesep() { return this.valuesep; }
  public double getValueoct() { return this.valueoct; }
  public double getValuenov() { return this.valuenov; }
  public double getValuedec() { return this.valuedec; }
  public String getDescription() { return this.description; }
  public String setCategory() { return this.category; }
  public String getMemo() { return this.memo; }
}
