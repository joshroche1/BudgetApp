package net.jar.quarkus;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Response;

@Path("account")
@ApplicationScoped
public class AccountResource {

  @Path("example")
  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public AccountEntity getExample() {
    AccountEntity aEntity = new AccountEntity();
    return aEntity;
  }
}