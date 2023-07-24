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

@Path("transaction")
@ApplicationScoped
public class TransactionResource {

  private static final Logger LOGGER = Logger.getLogger(TransactionResource.class.getName());
  
  @CheckedTemplate
  static class Templates {
    static native TemplateInstance list(List<TransactionEntity> transactionlist, List<AccountEntity> accountlist, List<ConfigEntity> categorylist, List<ConfigEntity> currencylist);
    //static native TemplateInstance detail(TransactionEntity transaction, List<AccountEntity> accountlist, List<ConfigEntity> categorylist, List<ConfigEntity> currencylist);
  }
  
  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list() {
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(transactionlist, accountlist, categorylist, currencylist);
  }
  
  /*
  @GET
  @Path("detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail(Long id) {
    TransactionEntity transaction = TransactionEntity.findById(id);
    if (transaction == null) {
      throw new WebApplicationException("transaction with id: " + id + " not found", 404);
    }
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.detail(transaction, accountlist, categorylist, currencylist);
  }
  */
  
  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create(@FormParam("name") String name, @FormParam("amount") String amount, @FormParam("accountid") String accountid, @FormParam("category") String category, @FormParam("currency") String currency, @FormParam("datetimestamp") String datetimestamp, @FormParam("description") String description) {
    TransactionEntity entity = new TransactionEntity();
    entity.name = name;
    entity.amount = Double.parseDouble(amount);
    entity.accountid = Long.parseLong(accountid);
    entity.category = category;
    entity.currency = currency;
    entity.datetimestamp = datetimestamp;
    entity.description = description;
    entity.persist();
    LOGGER.info("Saved Transaction: " + name);
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(transactionlist, accountlist, categorylist, currencylist);
  }
  
  /*
  @POST
  @Path("update/{id}/{field}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update(@PathParam("id") Long id, @PathParam("field") String field, @FormParam("fieldval") String fieldval) {
    TransactionEntity entity = TransactionEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    switch(fieldval) {
      case "name":
        entity.name = fieldval;
        entity.persist();
        break;
      case "amount":
        entity.amount = Double.parseDouble(fieldval);
        entity.persist();
        break;
      case "accountid":
        entity.accountid = Integer.parseInt(fieldval);
        entity.persist();
        break;
      case "category":
        entity.category = fieldval;
        entity.persist();
        break;
      case "currency":
        entity.currency = fieldval;
        entity.persist();
        break;
      case "datetimestamp":
        entity.datetimestamp = fieldval;
        entity.persist();
        break;
      case "description":
        entity.description = fieldval;
        entity.persist();
        break;
      default:
        break;
    }
    LOGGER.info("Update Transaction [" + id + "]: " + field);
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(transactionlist, accountlist, categorylist, currencylist);
  }
  */
  
  @POST
  @Path("delete/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance remove(@PathParam("id") Long id) {
    TransactionEntity entity = TransactionEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    entity.delete();
    LOGGER.info("Deleted Transaction [" + id + "]");
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(transactionlist, accountlist, categorylist, currencylist);
  }
    
  @GET
  @Path("list/sorted/{col}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_sorted(@PathParam("col") String col) {
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by(col));
    List<AccountEntity> accountlist = AccountEntity.listAll(Sort.by("id"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(transactionlist, accountlist, categorylist, currencylist);
  }
  
  /* REST Interface */
  
  @GET
  @Path("all")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public List<TransactionEntity> all() {
    return TransactionEntity.listAll(Sort.by("name"));
  }
  
  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public TransactionEntity get(@PathParam("id") Long id) {
    TransactionEntity transaction = TransactionEntity.findById(id);
    if (transaction == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    return transaction;
  }
  
  @POST
  @Path("add")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public TransactionEntity add(TransactionEntity entity) {
    entity.persist();
    return entity;
  }
  
  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(@PathParam("id") Long id) {
    TransactionEntity entity = TransactionEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("transaction with id: " + id + " not found", 404);
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
