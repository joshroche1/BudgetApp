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

@Path("budget")
@ApplicationScoped
public class BudgetResource {

  private static final Logger LOGGER = Logger.getLogger(BudgetResource.class.getName());
  
  @CheckedTemplate
  static class Templates {
    static native TemplateInstance list(List<BudgetEntity> budgetlist, List<ConfigEntity> currencylist);
    static native TemplateInstance detail(BudgetEntity budget, List<BudgetItemEntity> budgetitemlist, List<ConfigEntity> categorylist, List<ConfigEntity> currencylist);
    static native TemplateInstance overview(BudgetEntity budget, List<BudgetEntity> budgetlist, List<BudgetItemEntity> budgetitemlist, List<TransactionEntity> transactionlist, String tabledata, String budgettabledata);
  }
  
  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list() {
    List<BudgetEntity> budgetlist = BudgetEntity.listAll(Sort.by("id"));
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(budgetlist, currencylist);
  }
  
  @GET
  @Path("detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail(@PathParam("id") Long id) {
    BudgetEntity budget = BudgetEntity.findById(id);
    if (budget == null) {
      throw new WebApplicationException("budget with id: " + id + " not found", 404);
    }
    List<BudgetItemEntity> budgetitemlist = BudgetItemEntity.findByBudget(id);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.detail(budget, budgetitemlist, categorylist, currencylist);
  }
  
  @GET
  @Path("overview")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance overview() {
    BudgetEntity budget = BudgetEntity.findByName("Default");
    if (budget == null) {
      throw new WebApplicationException("budget not found", 404);
    }
    List<BudgetEntity> budgetlist = BudgetEntity.listAll(Sort.by("id"));
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    List<BudgetItemEntity> budgetitemlist = BudgetItemEntity.findByBudget(budget.id);
    String tabledata = "";
    String budgettabledata = "";
    return Templates.overview(budget, budgetlist, budgetitemlist, transactionlist, tabledata, budgettabledata);
  }
  
  @GET
  @Path("overview/id")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance overview_by_id(@FormParam("budgetid") String budgetid) {
    BudgetEntity budget = BudgetEntity.findById(Long.parseLong(budgetid));
    if (budget == null) {
      throw new WebApplicationException("budget with id: " + budgetid + " not found", 404);
    }
    List<BudgetEntity> budgetlist = BudgetEntity.listAll(Sort.by("id"));
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    List<BudgetItemEntity> budgetitemlist = BudgetItemEntity.findByBudget(Long.parseLong(budgetid));
    String tabledata = "";
    String budgettabledata = "";
    return Templates.overview(budget, budgetlist, budgetitemlist, transactionlist, tabledata, budgettabledata);
  }
  
  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create(@FormParam("name") String name, @FormParam("currency") String currency, @FormParam("description") String description) {
    BudgetEntity entity = new BudgetEntity();
    entity.name = name;
    entity.currency = currency;
    entity.description = description;
    entity.persist();
    LOGGER.info("Saved Budget: " + name);
    List<BudgetEntity> budgetlist = BudgetEntity.listAll(Sort.by("id"));
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(budgetlist, currencylist);
  }
  
  @POST
  @Path("update/{id}/{field}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update(@PathParam("id") Long id, @PathParam("field") String field, @FormParam("fieldval") String fieldval) {
    BudgetEntity entity = BudgetEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Budget with id: " + id + " not found", 404);
    }
    switch(fieldval) {
      case "name":
        entity.name = fieldval;
        entity.persist();
        break;
      case "currency":
        entity.currency = fieldval;
        entity.persist();
        break;
      case "description":
        entity.description = fieldval;
        entity.persist();
        break;
      default:
        break;
    }
    LOGGER.info("Update Budget [" + id + "]: " + field);
    List<BudgetEntity> budgetlist = BudgetEntity.listAll(Sort.by("id"));
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(budgetlist, currencylist);
  }
  
  @POST
  @Path("delete/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance remove(@PathParam("id") Long id) {
    BudgetEntity entity = BudgetEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Budget with id: " + id + " not found", 404);
    }
    entity.delete();
    LOGGER.info("Deleted Budget [" + id + "]");
    List<BudgetEntity> budgetlist = BudgetEntity.listAll(Sort.by("id"));
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(budgetlist, currencylist);
  }
    
  @GET
  @Path("list/sorted/{col}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_sorted(@PathParam("col") String col) {
    List<BudgetEntity> budgetlist = BudgetEntity.listAll(Sort.by(col));
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.list(budgetlist, currencylist);
  }
  
  @POST
  @Path("{bid}/budgetitem/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance budgetitem_create(@PathParam("bid") Long bid, @FormParam("name") String name, @FormParam("amount") String amount, @FormParam("category") String category, @FormParam("recurrence") String recurrence, @FormParam("recurrenceday") String recurrenceday, @FormParam("description") String description) {
    BudgetEntity budget = BudgetEntity.findById(bid);
    if (budget == null) {
      throw new WebApplicationException("budget with id: " + bid + " not found", 404);
    }
    BudgetItemEntity entity = new BudgetItemEntity();
    entity.name = name;
    entity.amount = Double.parseDouble(amount);
    entity.budgetid = bid;
    entity.category = category;
    entity.recurrence = recurrence;
    entity.recurrenceday = Integer.parseInt(recurrenceday);
    entity.description = description;
    entity.persist();
    LOGGER.info("Saved BudgetItem: " + name);
    List<BudgetItemEntity> budgetitemlist = BudgetItemEntity.findByBudget(bid);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.detail(budget, budgetitemlist, categorylist, currencylist);
  }
    
  @POST
  @Path("{bid}/budgetitem/delete/{itemid}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance remove(@PathParam("bid") Long bid, @PathParam("itemid") Long itemid) {
    BudgetEntity budget = BudgetEntity.findById(bid);
    if (budget == null) {
      throw new WebApplicationException("budget with id: " + bid + " not found", 404);
    }
    BudgetItemEntity entity = BudgetItemEntity.findById(itemid);
    if (entity == null) {
      throw new WebApplicationException("BudgetItem with id: " + itemid + " not found", 404);
    }
    entity.delete();
    LOGGER.info("Deleted BudgetItem [" + bid + "]");
    List<BudgetItemEntity> budgetitemlist = BudgetItemEntity.findByBudget(bid);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> currencylist = ConfigEntity.findByName("Currency");
    return Templates.detail(budget, budgetitemlist, categorylist, currencylist);
  }
  
  /* REST Interface */
  
  @GET
  @Path("all")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public List<BudgetEntity> all() {
    return BudgetEntity.listAll(Sort.by("name"));
  }
  
  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public BudgetEntity get(@PathParam("id") Long id) {
    BudgetEntity budget = BudgetEntity.findById(id);
    if (budget == null) {
      throw new WebApplicationException("Budget with id: " + id + " not found", 404);
    }
    return budget;
  }
  
  @POST
  @Path("add")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public BudgetEntity add(BudgetEntity entity) {
    entity.persist();
    return entity;
  }
  
  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(@PathParam("id") Long id) {
    BudgetEntity entity = BudgetEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("budget with id: " + id + " not found", 404);
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
