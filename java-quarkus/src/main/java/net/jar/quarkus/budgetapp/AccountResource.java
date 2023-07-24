package net.jar.quarkus.budgetapp;

import java.util.List;
import java.util.ArrayList;
import javax.annotation.security.RolesAllowed;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.transaction.Transactional;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.FormParam;
import javax.ws.rs.PathParam;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

import org.jboss.logging.Logger;
import io.quarkus.panache.common.Sort;
import io.quarkus.qute.CheckedTemplate;
import io.quarkus.qute.TemplateInstance;
import io.smallrye.common.annotation.Blocking;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

@Path("account")
@ApplicationScoped
public class AccountResource {

  private static final Logger LOGGER = Logger.getLogger(AccountResource.class.getName());
  
  @CheckedTemplate
  static class Templates {
    static native TemplateInstance list(List<AccountEntity> accountlist, List<ConfigEntity> accounttypelist, List<ConfigEntity> currencylist, List<ConfigEntity> countrylist);
    static native TemplateInstance detail(AccountEntity account, List<ConfigEntity> accounttypelist, List<ConfigEntity> currencylist, List<ConfigEntity> countrylist);
  }
  
  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list() {
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    return Templates.list(accountlist, accounttypelist, currencylist, countrylist);
  }
  
  @GET
  @Path("detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail(Long id) {
    AccountEntity account = AccountEntity.findById(id);
    if (account == null) {
      throw new WebApplicationException("account with id: " + id + " not found", 404);
    }
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    return Templates.detail(account, accounttypelist, currencylist, countrylist);
  }
  
  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create(@FormParam("name") String name, @FormParam("accounttype") String accounttype, @FormParam("currency") String currency, @FormParam("country") String country) {
    AccountEntity entity = new AccountEntity();
    entity.name = name;
    entity.accounttype = accounttype;
    entity.currency = currency;
    entity.country = country;
    entity.persist();
    LOGGER.info("Saved Account: " + name);
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    return Templates.list(accountlist, accounttypelist, currencylist, countrylist);
  }
  
  @POST
  @Path("update/{id}/{field}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update(@PathParam("id") Long id, @PathParam("field") String field, @FormParam("fieldval") String fieldval) {
    AccountEntity entity = AccountEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    switch(fieldval) {
      case "name":
        entity.name = fieldval;
        entity.persist();
        break;
      case "accounttype":
        entity.accounttype = fieldval;
        entity.persist();
        break;
      case "currency":
        entity.currency = fieldval;
        entity.persist();
        break;
      case "country":
        entity.country = fieldval;
        entity.persist();
        break;
      default:
        break;
    }
    LOGGER.info("Update Account [" + id + "]: " + field);
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    return Templates.list(accountlist, accounttypelist, currencylist, countrylist);
  }
  
  @POST
  @Path("delete/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance remove(@PathParam("id") Long id) {
    AccountEntity entity = AccountEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    entity.delete();
    LOGGER.info("Deleted Account [" + id + "]");
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    return Templates.list(accountlist, accounttypelist, currencylist, countrylist);
  }
    
  @GET
  @Path("list/sorted/{col}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_sorted(@PathParam("col") String col) {
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by(col));
    List<ConfigEntity> accounttypelist = ConfigEntity.findByName("AccountType");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    List<ConfigEntity> countrylist = ConfigEntity.findByName("Country");
    return Templates.list(accountlist, accounttypelist, currencylist, countrylist);
  }
  
  /* REST Interface */
  
  @GET
  @Path("all")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public List<AccountEntity> all() {
    return AccountEntity.listAll(Sort.by("name"));
  }
  
  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public AccountEntity get(@PathParam("id") Long id) {
    AccountEntity account = AccountEntity.findById(id);
    if (account == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    return account;
  }
  
  @POST
  @Path("add")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public AccountEntity add(AccountEntity entity) {
    entity.persist();
    return entity;
  }
  
  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(@PathParam("id") Long id) {
    AccountEntity entity = AccountEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("account with id: " + id + " not found", 404);
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
