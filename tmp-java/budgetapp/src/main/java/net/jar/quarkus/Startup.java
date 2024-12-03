package net.jar.quarkus;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.transaction.Transactional;
import io.quarkus.runtime.StartupEvent;

@ApplicationScoped
public class Startup {

  @Transactional
  public void loadDefaults(@Observes StartupEvent evt) {
    /* Init objects
	TransactionEntity.add("20240101 12:34:56", "Example 1", "Example transaction 1", "Income", 1234.56, "EUR", "Example Transaction");
	*/
  }
}