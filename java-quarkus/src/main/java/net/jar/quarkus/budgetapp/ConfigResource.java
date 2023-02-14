package net.jar.quarkus.budgetapp;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Iterator;
import javax.annotation.security.RolesAllowed;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.persistence.EntityManager;
import javax.transaction.Transactional;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.FormParam;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.core.Response;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.MediaType;
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

@Path("admin")
@ApplicationScoped
public class ConfigResource {

  private static final Logger LOGGER = Logger.getLogger(ConfigResource.class.getName());


  @CheckedTemplate
  static class Templates {
    static native TemplateInstance settingsview(List<ConfigEntity> categorylist, List<ConfigEntity> accounttypelist, List<ConfigEntity> currencylist, List<ConfigEntity> countrylist, List<ConfigEntity> systemcurrencies);
  }
  
  @GET
  @Path("view/settings")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance settings_view() {
    List<ConfigEntity> categorylist = ConfigEntity.findByName("category");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("accounttype");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("country");
    List<ConfigEntity> systemcurrencies = ConfigEntity.findByName("systemcurrency");
    return Templates.settingsview(categorylist, accounttypelist, currencylist, countrylist, systemcurrencies);
  }
  
  @POST
  @Path("category/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance category_create(@FormParam("category") String category) {
    ConfigEntity entity = new ConfigEntity();
    entity.name = "category";
    entity.value = category;
    entity.persist();
    List<ConfigEntity> categorylist = ConfigEntity.findByName("category");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("accounttype");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("country");
    List<ConfigEntity> systemcurrencies = ConfigEntity.findByName("systemcurrency");
    return Templates.settingsview(categorylist, accounttypelist, currencylist, countrylist, systemcurrencies);
  }
  
  @POST
  @Path("category/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance delete_view(Long id) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Config Entity with id: " + id + " not found", 404);
    }
    entity.delete();
    List<ConfigEntity> categorylist = ConfigEntity.findByName("category");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("accounttype");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("country");
    List<ConfigEntity> systemcurrencies = ConfigEntity.findByName("systemcurrency");
    return Templates.settingsview(categorylist, accounttypelist, currencylist, countrylist, systemcurrencies);
  }
  
  public static List<ConfigEntity> getList(String name) {
    List<ConfigEntity> entitylist = ConfigEntity.findByName(name);
    return entitylist;
  }
  
  public static ConfigEntity get(String value) {
    ConfigEntity entity = ConfigEntity.findByValue(value);
    if (entity == null) {
      throw new WebApplicationException("Config Resource with value: " + value + " not found", 404);
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
