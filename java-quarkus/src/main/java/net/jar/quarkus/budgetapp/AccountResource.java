package net.jar.quarkus.budgetapp;

import java.io.IOException;
import java.util.List;
import java.util.Map;
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
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

import org.jboss.logging.Logger;
import io.quarkus.panache.common.Sort;
import io.quarkus.qute.CheckedTemplate;
import io.quarkus.qute.TemplateExtension;
import io.quarkus.qute.TemplateInstance;
import io.smallrye.common.annotation.Blocking;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

@Path("accounts")
@ApplicationScoped
public class AccountResource {

  private static final Logger LOGGER = Logger.getLogger(AccountResource.class.getName());


  @CheckedTemplate
  static class Templates {
    static native TemplateInstance listview(List<AccountEntity> accountlist);
    static native TemplateInstance createview(List<ConfigEntity> accounttypelist, List<ConfigEntity> countrylist, List<ConfigEntity> currencylist);
    static native TemplateInstance detailview(AccountEntity account, List<ConfigEntity> accounttypelist, List<ConfigEntity> countrylist, List<ConfigEntity> currencylist);
  }
  
  @GET
  @Path("view/list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_view() {
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    return Templates.listview(accountlist);
  }
  
  @GET
  @Path("view/create")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance create_view() {
    List<ConfigEntity> accounttypelist = ConfigResource.getList("accounttype");
    List<ConfigEntity> countrylist = ConfigResource.getList("country");
    List<ConfigEntity> currencylist = ConfigResource.getList("currency");
    return Templates.createview(accounttypelist, countrylist, currencylist);
  }
  
  @POST
  @Path("view/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create_form(@FormParam("name") String name, @FormParam("number") String number, @FormParam("iban") String iban, @FormParam("bic") String bic, @FormParam("type") String type, @FormParam("address") String address, @FormParam("city") String city, @FormParam("state") String state, @FormParam("country") String country, @FormParam("api_credential") String api_credential, @FormParam("currency") String currency, @FormParam("telephone") String telephone) {
    String msg = "" + name + "" + number + "" + iban + "" + bic + "" + type + "" + address + "" + city + "" + state + "" + country + "" + api_credential + "" + currency + "" + telephone;
    System.out.println(msg);
    AccountEntity entity = new AccountEntity();
    entity.name = name;
    entity.number = number;
    entity.iban = iban;
    entity.bic = bic;
    entity.type = type;
    entity.address = address;
    entity.city = city;
    entity.state = state;
    entity.country = country;
    entity.api_credential = api_credential;
    entity.currency = currency;
    entity.telephone = telephone;
    entity.persist();
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    return Templates.listview(accountlist);
  }
  
  @GET
  @Path("view/detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail_view(Long id) {
    AccountEntity account = AccountEntity.findById(id);
    if (account == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    List<ConfigEntity> accounttypelist = ConfigResource.getList("accounttype");
    List<ConfigEntity> countrylist = ConfigResource.getList("country");
    List<ConfigEntity> currencylist = ConfigResource.getList("currency");
    return Templates.detailview(account, accounttypelist, countrylist, currencylist);
  }
  
  @POST
  @Path("view/update/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update_view(Long id, @FormParam("name") String name, @FormParam("number") String number, @FormParam("iban") String iban, @FormParam("bic") String bic, @FormParam("type") String type, @FormParam("address") String address, @FormParam("city") String city, @FormParam("state") String state, @FormParam("country") String country, @FormParam("api_credential") String api_credential, @FormParam("currency") String currency, @FormParam("telephone") String telephone) {
    AccountEntity entity = AccountEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    String msg = "" + name + "" + number + "" + iban + "" + bic + "" + type + "" + address + "" + city + "" + state + "" + country + "" + api_credential + "" + currency + "" + telephone;
    System.out.println(msg);
    if (name != "") { entity.name = name; }
    if (number != "") { entity.number = number; }
    if (iban != "") { entity.iban = iban; }
    if (bic != "") { entity.bic = bic; }
    if (type != "") { entity.type = type; }
    if (address != "") { entity.address = address; }
    if (city != "") { entity.city = city; }
    if (state != "") { entity.state = state; }
    if (country != "") { entity.country = country; }
    if (api_credential != "") { entity.api_credential = api_credential; }
    if (currency != "") { entity.currency = currency; }
    if (telephone != "") { entity.telephone = telephone; }
    entity.persist();
    List<ConfigEntity> accounttypelist = ConfigResource.getList("accounttype");
    List<ConfigEntity> countrylist = ConfigResource.getList("country");
    List<ConfigEntity> currencylist = ConfigResource.getList("currency");
    return Templates.detailview(entity, accounttypelist, countrylist, currencylist);
  }
  
  @POST
  @Path("view/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance delete_view(Long id) {
    AccountEntity account = AccountEntity.findById(id);
    if (account == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    account.delete();
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    return Templates.listview(accountlist);
  }

  /* REST INTERFACE */

  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<AccountEntity> list() {
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("hostname"));
    return accountlist;
  }

  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public AccountEntity get(long id) {
    AccountEntity account = AccountEntity.findById(id);
    return account;
  }

  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public AccountEntity create(AccountEntity entity) {
    entity.persist();
    return entity;
  }

  @PUT
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public AccountEntity update(Long id, AccountEntity account) {
    AccountEntity entity = AccountEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    entity.name = account.name;
    entity.number = account.number;
    entity.iban = account.iban;
    entity.bic = account.bic;
    entity.type = account.type;
    entity.address = account.address;
    entity.city = account.city;
    entity.state = account.state;
    entity.country = account.country;
    entity.api_credential = account.api_credential;
    entity.currency = account.currency;
    entity.telephone = account.telephone;
    return entity;
  }

  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(Long id) {
    AccountEntity entity = AccountEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Account with id: " + id + " not found", 404);
    }
    entity.delete();
  }
  
  @GET
  @Path("search/name/{name}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public AccountEntity search_name(String name) {
    AccountEntity account = AccountEntity.findByName(name);
    return account;
  }
  
  @GET
  @Path("search/type/{type}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<AccountEntity> search_type(String type) {
    List<AccountEntity> accountlist = AccountEntity.findByType(type);
    return accountlist;
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
