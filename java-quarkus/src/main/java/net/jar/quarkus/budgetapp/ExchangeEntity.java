package net.jar.quarkus.budgetapp;


import java.util.List;
import javax.persistence.Column;
import javax.persistence.Entity;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

@Entity
public class ExchangeEntity extends PanacheEntity {

  public Double rate;
  public String currency_to;
  public String currency_from;
  
  public static ExchangeEntity add(String currency_from, String currency_to, Double rate) {
    ExchangeEntity present = ExchangeEntity.findByFromTo(currency_from, currency_to);
    if (present != null) {
      return present;
    }
    ExchangeEntity entity = new ExchangeEntity();
    entity.currency_from = currency_from;
    entity.currency_to = currency_to;
    entity.rate = rate;
    entity.persist();
    return entity;
  }
  
  public static ExchangeEntity findByFromTo(String currency_from, String currency_to) {
    ExchangeEntity result = new ExchangeEntity();
    List<ExchangeEntity> fromlist = list("currency_from", currency_from);
    List<ExchangeEntity> tolist = list("currency_to", currency_to);
    for (ExchangeEntity froment : fromlist) {
      for (ExchangeEntity toent : tolist) {
        if (froment.currency_from == toent.currency_from && froment.currency_to == toent.currency_to) {
          result = froment;
        }
      }
    }
    return result;
  }
  
}