package net.jar.quarkus;

import static jakarta.ws.rs.core.Response.Status.CREATED;
import static jakarta.ws.rs.core.Response.Status.NOT_FOUND;
import static jakarta.ws.rs.core.Response.Status.NO_CONTENT;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
//import jakarta.transaction.Transactional;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Response;

import io.smallrye.mutiny.Uni;
import org.hibernate.reactive.mutiny.Mutiny.SessionFactory;

@Path("transaction")
@ApplicationScoped
public class TransactionResource {

  @Inject
  SessionFactory sf;

  @Path("example")
  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<Response> getExample() {
    TransactionEntity tEntity = new TransactionEntity();
    tEntity.datetimestamp = "20240101 12:34:56";
    tEntity.name = "Example";
    tEntity.description = "Example Transaction";
    tEntity.category = "Example";
    tEntity.amount = 123.45;
    tEntity.currency = "EUR";
    tEntity.notes = "EXAMPLE";
    return sf.withTransaction((s,t) -> s.persist(tEntity)).replaceWith(Response.ok(tEntity).status(CREATED)::build);
  }
}