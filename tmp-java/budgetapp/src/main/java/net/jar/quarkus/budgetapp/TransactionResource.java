package net.jar.quarkus.budgetapp;

import static jakarta.ws.rs.core.Response.Status.CREATED;
import static jakarta.ws.rs.core.Response.Status.NOT_FOUND;
import static jakarta.ws.rs.core.Response.Status.NO_CONTENT;

import java.util.List;
import java.util.ArrayList;

import jakarta.enterprise.context.ApplicationScoped;

import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.WebApplicationException;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import io.quarkus.hibernate.reactive.panache.Panache;
import io.quarkus.panache.common.Sort;
import io.smallrye.mutiny.Uni;

import org.jboss.logging.Logger;

@Path("transaction")
@ApplicationScoped
public class TransactionResource {

  private static final Logger LOGGER = Logger.getLogger(TransactionResource.class.getName());

  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<List<TransactionEntity>> getAll() {
    return TransactionEntity.listAll();
  }

  @Path("{id}")
  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<TransactionEntity> getSingle(Long id) {
    return TransactionEntity.findById(id);
  }

  @POST
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<Response> create(TransactionEntity entity) {
    if (entity == null || entity.id != null) {
      throw new WebApplicationException("Id not set.", 422);
    }
    return Panache.withTransaction(entity::persist).replaceWith(Response.ok(entity).status(CREATED)::build);
  }

  @PUT
  @Path("{id}")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<Response> update(Long id, TransactionEntity tEntity) {
    if (tEntity == null || tEntity.id == null) {
      throw new WebApplicationException("Entity not found.", 422);
    }
    return Panache.withTransaction(() -> TransactionEntity.<TransactionEntity> findById(id).onItem().ifNotNull().invoke(entity -> entity.id = tEntity.id)).onItem().ifNotNull().transform(entity -> Response.ok(entity).build()).onItem().ifNull().continueWith(Response.ok().status(NOT_FOUND)::build);
  }

  @DELETE
  @Path("{id}")
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<Response> delete(Long id) {
    return Panache.withTransaction(() -> TransactionEntity.deleteById(id)).map(deleted -> deleted ? Response.ok().status(NO_CONTENT).build() : Response.ok().status(NOT_FOUND).build());
  }

}