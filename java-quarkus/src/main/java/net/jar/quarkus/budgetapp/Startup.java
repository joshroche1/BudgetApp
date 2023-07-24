package net.jar.quarkus.budgetapp;

import javax.enterprise.event.Observes;
import javax.inject.Singleton;
import javax.transaction.Transactional;
import org.jboss.logging.Logger;
import io.quarkus.runtime.StartupEvent;

@Singleton
public class Startup {
  
  private static final Logger LOGGER = Logger.getLogger(AdminResource.class.getName());
  
  @Transactional
  public void loadDefaults(@Observes StartupEvent evt) {
    // Init objects
    AccountEntity account = AccountEntity.findByName("Default");
    if (account == null) {
      AccountEntity entity = new AccountEntity();
      entity.name = "Default";
      entity.accounttype = "Checking";
      entity.currency = "USD";
      entity.country = "USA";
      entity.persist();
      LOGGER.info("Added Account entity");
    }
    BudgetEntity budget = BudgetEntity.findByName("Default");
    if (budget == null) {
      BudgetEntity entity = new BudgetEntity();
      entity.name = "Default";
      entity.currency = "USD";
      entity.description = "Default Budget";
      entity.persist();
      LOGGER.info("Added Budget entity");
    }
    
    ConfigEntity.add("Category", "Housing");
    ConfigEntity.add("Category", "Electric");
    ConfigEntity.add("Category", "Water");
    ConfigEntity.add("Category", "Utilities");
    ConfigEntity.add("Category", "Phone");
    ConfigEntity.add("Category", "Internet");
    ConfigEntity.add("Category", "Insurance");
    ConfigEntity.add("Category", "Debt");
    ConfigEntity.add("Category", "Credit");
    ConfigEntity.add("Category", "Food");
    ConfigEntity.add("Category", "Mobility");
    ConfigEntity.add("Category", "Entertainment");
    ConfigEntity.add("Category", "Income");
    ConfigEntity.add("Category", "Expense");
    ConfigEntity.add("Category", "Other");
    ConfigEntity.add("AccountType", "Checking");
    ConfigEntity.add("AccountType", "Savings");
    ConfigEntity.add("Currency", "USD");
    ConfigEntity.add("Currency", "EUR");
    ConfigEntity.add("Country", "USA");
    ConfigEntity.add("Country", "DE");
    ExchangeEntity.add("EUR","USD",1.08);
    ExchangeEntity.add("USD","EUR",0.93);
    
    UserEntity.add("admin", "admin", "user", "admin@admin.adm");
    LOGGER.info("Added user entity");
  }
}