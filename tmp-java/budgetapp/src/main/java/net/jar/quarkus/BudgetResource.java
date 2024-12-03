package net.jar.quarkus;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Response;

@Path("budget")
@ApplicationScoped
public class BudgetResource {

  @Path("example")
  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public BudgetEntity getExample() {
    BudgetEntity bEntity = new BudgetEntity();
    return bEntity;
  }
}