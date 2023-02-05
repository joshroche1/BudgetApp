package net.jar.quarkus.budgetapp;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import javax.annotation.security.RolesAllowed;
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
import javax.ws.rs.core.Response;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

import org.hibernate.Query;
import org.jboss.logging.Logger;
import io.quarkus.panache.common.Sort;
import io.quarkus.qute.CheckedTemplate;
import io.quarkus.qute.TemplateExtension;
import io.quarkus.qute.TemplateInstance;
import io.smallrye.common.annotation.Blocking;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

@ApplicationScoped
public class ConfigResource {

  private static final Logger LOGGER = Logger.getLogger(ConfigResource.class.getName());


  public static ConfigEntity get(String name) {
    ConfigEntity entity = ConfigEntity.findByName(name);
    if (entity == null) {
      throw new WebApplicationException("Config Resource with name: " + name + " not found", 404);
    }
    return entity;
  }
  
  public static void create(String name, String value) {
    ConfigEntity entity = new ConfigEntity();
    entity.name = name;
    entity.value = value;
    entity.persist();
  }
  
  public static ConfigEntity update(Long id, String name, String value) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Config Resource with id: " + id + " not found", 404);
    }
    entity.name = name;
    entity.value = value;
    entity.persist();
    return entity;
  }
  
  public static void delete(Long id) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Config Resource with id: " + id + " not found", 404);
    }
    entity.delete();
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
