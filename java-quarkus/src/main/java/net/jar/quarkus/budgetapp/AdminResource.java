package net.jar.quarkus.budgetapp;

import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import javax.annotation.security.RolesAllowed;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.persistence.EntityManager;
import javax.transaction.Transactional;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.FormParam;
import javax.ws.rs.PathParam;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.SecurityContext;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

import org.hibernate.Query;
import org.jboss.logging.Logger;
import io.quarkus.elytron.security.common.BcryptUtil;
import io.quarkus.panache.common.Sort;
import io.quarkus.qute.CheckedTemplate;
import io.quarkus.qute.TemplateExtension;
import io.quarkus.qute.TemplateInstance;
import io.smallrye.common.annotation.Blocking;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;


@Path("admin")
@ApplicationScoped
public class AdminResource {

  private static final Logger LOGGER = Logger.getLogger(AdminResource.class.getName());
    
  @ConfigProperty(name = "quarkus.datasource.db-kind")
  String db_kind;
  
  @ConfigProperty(name = "quarkus.datasource.jdbc.url")
  String db_jdbc_url;
  
  @ConfigProperty(name = "quarkus.log.file.path")
  String logfile;
    
  HashMap<String, String> config_map;
  
  @CheckedTemplate
  static class Templates {
    static native TemplateInstance settings(List<UserEntity> userlist, List<ConfigEntity> accounttypelist, List<ConfigEntity> categorylist, List<ConfigEntity> currencylist, List<ConfigEntity> countrylist, List<ExchangeEntity> exchangelist, HashMap<String, String> configmap);
    static native TemplateInstance userprofile(UserEntity currentuser);
  }
  
  private HashMap<String, String> get_config() {
    config_map = new HashMap<String, String>();
    config_map.put("db_kind", db_kind);
    config_map.put("db_jdbc_url", db_jdbc_url);
    config_map.put("logfile_path", logfile);
    config_map.put("logfile", FilesystemResource.readFile(logfile));
    return config_map;
  }

  
  @GET
  @Path("settings")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance settings() {
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    List<ExchangeEntity> exchangelist = ExchangeEntity.listAll(Sort.by("id"));
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(userlist, accounttypelist, categorylist, currencylist, countrylist, exchangelist, configmap);
  }
  
  @GET
  @Path("user")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_PLAIN)
  public String user(@Context SecurityContext securityContext) {
    return securityContext.getUserPrincipal().getName();
  }
  
  @GET
  @Path("userprofile")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance userprofile(@Context SecurityContext securityContext) {
    String username = securityContext.getUserPrincipal().getName();
    UserEntity currentuser = UserEntity.find("username", username).firstResult();
    return Templates.userprofile(currentuser);
  }
  
  @POST
  @Path("user/{id}/email/update")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance user_update_email(@FormParam("email") String newemail, @PathParam("id") Long id, @Context SecurityContext securityContext) {
    UserEntity entity = UserEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("User with id: " + id + " not found", 404);
    }
    entity.email = newemail;
    entity.persist();
    String username = securityContext.getUserPrincipal().getName();
    UserEntity currentuser = UserEntity.find("username", username).firstResult();
    return Templates.userprofile(currentuser);
  }
  
  @POST
  @Path("user/{id}/password/update")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance user_update_password(@FormParam("newpassword") String newpassword, @FormParam("passwordcheck") String passwordcheck, @PathParam("id") Long id, @Context SecurityContext securityContext) {
    if (newpassword == null || passwordcheck == null) {
      throw new WebApplicationException("Passwords required", 404);
    } else if (!newpassword.equals(passwordcheck)) {
      throw new WebApplicationException("Passwords must match", 404);
    }
    UserEntity entity = UserEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("User with id: " + id + " not found", 404);
    }
    entity.password = BcryptUtil.bcryptHash(newpassword);
    entity.persist();
    String username = securityContext.getUserPrincipal().getName();
    UserEntity currentuser = UserEntity.find("username", username).firstResult();
    return Templates.userprofile(currentuser);
  }
  
  @POST
  @Path("user/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance user_create(@FormParam("email") String email, @FormParam("username") String username, @FormParam("password") String password, @FormParam("passwordcheck") String passwordcheck) {
    if (username == null || password == null || passwordcheck == null) {
      throw new WebApplicationException("Username and passwords required", 404);
    } else if (!password.equals(passwordcheck)) {
      throw new WebApplicationException("Passwords must match", 404);
    }
    UserEntity entity1 = UserEntity.findByUsername(username);
    UserEntity entity2 = UserEntity.findByEmail(email);
    if (entity1 != null) {
      throw new WebApplicationException("Username already registered: " + username, 404);
    } else if (entity2 != null) {
      throw new WebApplicationException("Email address already registered: " + email, 404);
    }
    UserEntity.add(username, password, "user", email);
    LOGGER.info("Added user: " + username);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    List<ExchangeEntity> exchangelist = ExchangeEntity.listAll(Sort.by("id"));
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(userlist, accounttypelist, categorylist, currencylist, countrylist, exchangelist, configmap);
  }
  
  @POST
  @Path("user/delete/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance user_delete(@PathParam("id") Long id) {
    UserEntity entity = UserEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("User with id: " + id + " not found", 404);
    }
    entity.delete();
    LOGGER.info("Deleted user: " + id);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    List<ExchangeEntity> exchangelist = ExchangeEntity.listAll(Sort.by("id"));
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(userlist, accounttypelist, categorylist, currencylist, countrylist, exchangelist, configmap);
  }
  
  @POST
  @Path("config/{field}/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance config_create(@PathParam("field") String field, @FormParam("fieldval") String fieldval) {
    ConfigEntity.add(field,fieldval);
    LOGGER.info("Created ConfigEntity: " + field + ", " + fieldval);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    List<ExchangeEntity> exchangelist = ExchangeEntity.listAll(Sort.by("id"));
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(userlist, accounttypelist, categorylist, currencylist, countrylist, exchangelist, configmap);
  }
  
  @POST
  @Path("config/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance config_delete(Long id) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("ConfigEntity with ID: " + id + " not found", 404);
    }
    entity.delete();
    LOGGER.info("Deleted ConfigEntity [" + id + "]");
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    List<ExchangeEntity> exchangelist = ExchangeEntity.listAll(Sort.by("id"));
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(userlist, accounttypelist, categorylist, currencylist, countrylist, exchangelist, configmap);
  }
  
  @POST
  @Path("exchangerate/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance exchangerate_create(@FormParam("currency_from") String currency_from, @FormParam("currency_to") String currency_to, @FormParam("rate") String rate) {
    ExchangeEntity entity = new ExchangeEntity();
    entity.currency_from = currency_from;
    entity.currency_to = currency_to;
    entity.rate = Double.parseDouble(rate);    
    LOGGER.info("Created ExchangeEntity: " + currency_from + " to " + currency_to + ": " + rate);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    List<ExchangeEntity> exchangelist = ExchangeEntity.listAll(Sort.by("id"));
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(userlist, accounttypelist, categorylist, currencylist, countrylist, exchangelist, configmap);
  }
  
  @POST
  @Path("exchangerate/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance exchangerate_delete(Long id) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("ConfigEntity with ID: " + id + " not found", 404);
    }
    entity.delete();
    LOGGER.info("Deleted ConfigEntity [" + id + "]");
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    List<ExchangeEntity> exchangelist = ExchangeEntity.listAll(Sort.by("id"));
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(userlist, accounttypelist, categorylist, currencylist, countrylist, exchangelist, configmap);
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