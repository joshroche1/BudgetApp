package net.jar.quarkus.budgetapp;


import javax.annotation.security.PermitAll;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

import io.quarkus.qute.CheckedTemplate;
import io.quarkus.qute.TemplateInstance;

import io.vertx.core.http.HttpServerResponse;
import org.jboss.logging.Logger;

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
  public TemplateInstance logout(HttpServerResponse response) {
    response.removeCookie(cookieName, true);
    return Templates.login();
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