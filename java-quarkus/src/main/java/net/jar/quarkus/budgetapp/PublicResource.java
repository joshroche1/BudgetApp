package net.jar.quarkus.budgetapp;

import java.util.List;
import java.net.URI;
import javax.annotation.security.PermitAll;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.persistence.EntityManager;
import javax.transaction.Transactional;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

import org.hibernate.Query;
import org.jboss.logging.Logger;
import io.quarkus.panache.common.Sort;
import io.quarkus.qute.CheckedTemplate;
import io.quarkus.qute.TemplateExtension;
import io.quarkus.qute.TemplateInstance;
import io.smallrye.common.annotation.Blocking;
import io.vertx.core.http.HttpServerResponse;
import org.jboss.resteasy.reactive.RestResponse;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;


@Path("/")
@ApplicationScoped
public class PublicResource {

  private static final Logger LOGGER = Logger.getLogger(PublicResource.class.getName());
  
  @ConfigProperty(name = "quarkus.http.auth.form.cookie-name")
  String cookieName;
  
  @Inject
  UriInfo uriInfo;

  @CheckedTemplate
  static class Templates {
    static native TemplateInstance index();
    static native TemplateInstance login();
    static native TemplateInstance error();
  }
  
  @GET
  @Path("/")
  @PermitAll
  @Produces(MediaType.TEXT_HTML)
  public TemplateInstance index() {
    return Templates.index();
  }
  
  @GET
  @Path("/login")
  @PermitAll
  @Produces(MediaType.TEXT_HTML)
  public TemplateInstance login() {
    return Templates.login();
  }
  
  @GET
  @Path("/logout")
  @PermitAll
  public RestResponse<Object> logout(HttpServerResponse response) {
    URI loginUri = uriInfo.getRequestUriBuilder().replacePath("/login").build();
    response.removeCookie(cookieName, true);
    return RestResponse.seeOther(loginUri);
  }
  
  @GET
  @Path("/error")
  @PermitAll
  @Produces(MediaType.TEXT_HTML)
  public TemplateInstance error() {
    return Templates.error();
  }


  @Provider
  public static class ErrorMapper implements ExceptionMapper<Exception> {

    @Inject
    ObjectMapper objectMapper;

    @Override
    public Response toResponse(Exception exception) {
      LOGGER.error("Failed to handle request", exception);

      int code = 500;
      if (exception instanceof WebApplicationException) {
        code = ((WebApplicationException) exception).getResponse().getStatus();
      }

      ObjectNode exceptionJson = objectMapper.createObjectNode();
      exceptionJson.put("exceptionType", exception.getClass().getName());
      exceptionJson.put("code", code);

      if (exception.getMessage() != null) {
        exceptionJson.put("error", exception.getMessage());
      }

      return Response.status(code)
        .entity(exceptionJson)
        .build();
    }

  }
}
