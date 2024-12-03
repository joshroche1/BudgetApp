package net.jar.quarkus;

import static jakarta.ws.rs.core.Response.Status.CREATED;
import static jakarta.ws.rs.core.Response.Status.NOT_FOUND;
import static jakarta.ws.rs.core.Response.Status.NO_CONTENT;

import java.util.List;
import java.util.ArrayList;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.WebApplicationException;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.ext.ExceptionMapper;
import jakarta.ws.rs.ext.Provider;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import io.quarkus.hibernate.reactive.panache.Panache;
import io.quarkus.panache.common.Sort;
import io.smallrye.mutiny.Uni;
import io.smallrye.mutiny.CompositeException;
import org.jboss.logging.Logger;
import org.hibernate.reactive.mutiny.Mutiny.SessionFactory;

@Path("account")
@ApplicationScoped
public class AccountResource {

  private static final Logger LOGGER = Logger.getLogger(AccountResource.class.getName());

  @Path("example")
  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public AccountEntity getExample() {
    AccountEntity aEntity = new AccountEntity();
    return aEntity;
  }

  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<List<AccountEntity>> get() {
	return AccountEntity.listAll(Sort.by("id"));
  }

  @Path("{id}")
  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<AccountEntity> getSingle(Long id) {
	return AccountEntity.findById(id);
  }

  @POST
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  public Uni<Response> create(AccountEntity entity) {
	if (entity == null || entity.id != null) {
	  throw new WebApplicationException("Id not set on request", 422);
	}
	return Panache.withTransaction(entity::persist).replaceWith(Response.ok(entity).status(CREATED)::build);
  }

  @Provider
  public static class ErrorMapper implements ExceptionMapper<Exception> {

    @Inject
    ObjectMapper objectMapper;

    @Override
    public Response toResponse(Exception exception) {
      LOGGER.error("Failed to handle request", exception);

      Throwable throwable = exception;

      int code = 500;
      if (throwable instanceof WebApplicationException) {
        code = ((WebApplicationException) exception).getResponse().getStatus();
      }

      // This is a Mutiny exception and it happens, for example, when we try to insert a new
      // fruit but the name is already in the database
      if (throwable instanceof CompositeException) {
        throwable = ((CompositeException) throwable).getCause();
      }

      ObjectNode exceptionJson = objectMapper.createObjectNode();
      exceptionJson.put("exceptionType", throwable.getClass().getName());
      exceptionJson.put("code", code);

	  if (exception.getMessage() != null) {
        exceptionJson.put("error", throwable.getMessage());
      }

      return Response.status(code).entity(exceptionJson).build();
    }
  }
}