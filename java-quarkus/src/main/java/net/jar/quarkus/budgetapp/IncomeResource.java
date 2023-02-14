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

@Path("incomes")
@ApplicationScoped
public class IncomeResource {

  private static final Logger LOGGER = Logger.getLogger(IncomeResource.class.getName());


  @CheckedTemplate
  static class Templates {
    static native TemplateInstance listview(List<IncomeEntity> incomelist);
    static native TemplateInstance createview(List<ConfigEntity> incometypelist);
    static native TemplateInstance detailview(IncomeEntity income, List<ConfigEntity> incometypelist);
  }
  
  @GET
  @Path("view/list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_view() {
    List<IncomeEntity> incomelist = IncomeEntity.listAll(Sort.by("id"));
    return Templates.listview(incomelist);
  }
  
  @GET
  @Path("view/create")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance create_view() {
    List<ConfigEntity> incometypelist = ConfigResource.getList("incometype");
    return Templates.createview(incometypelist);
  }
  
  @POST
  @Path("view/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create_form(@FormParam("name") String name, @FormParam("incometype") String incometype, @FormParam("amount") String amount, @FormParam("recurrence") String recurrence, @FormParam("date_occurence") String date_occurence, @FormParam("paid") boolean paid, @FormParam("active") boolean active) {
    IncomeEntity entity = new IncomeEntity();
    entity.name = name;
    entity.incometype = incometype;
    entity.amount = amount;
    entity.recurrence = recurrence;
    entity.date_occurence = date_occurence;
    entity.paid = paid;
    entity.active = active;
    entity.persist();
    List<IncomeEntity> incomelist = IncomeEntity.listAll(Sort.by("id"));
    return Templates.listview(incomelist);
  }
  
  @GET
  @Path("view/detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail_view(Long id) {
    IncomeEntity income = IncomeEntity.findById(id);
    if (income == null) {
      throw new WebApplicationException("Income with id: " + id + " not found", 404);
    }
    List<ConfigEntity> incometypelist = ConfigResource.getList("incometype");
    return Templates.detailview(income, incometypelist);
  }
  
  @POST
  @Path("view/update/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update_view(Long id, @FormParam("name") String name, @FormParam("incometype") String incometype,  @FormParam("amount") String amount, @FormParam("recurrence") String recurrence, @FormParam("date_occurence") String date_occurence, @FormParam("paid") boolean paid, @FormParam("active") boolean active) {
    IncomeEntity entity = IncomeEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Income with id: " + id + " not found", 404);
    }
    if (name != "") { entity.name = name; }
    if (incometype != "") { entity.incometype = incometype; }
    if (amount != "") { entity.amount = amount; }
    if (recurrence != "") { entity.recurrence = recurrence; }
    if (date_occurence != "") { entity.date_occurence = date_occurence; }
    //if (paid != null) { entity.paid = paid; }
    //if (active != null) { entity.active = active; }
    entity.persist();
    List<ConfigEntity> incometypelist = ConfigResource.getList("incometype");
    return Templates.detailview(entity, incometypelist);
  }
  
  @POST
  @Path("view/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance delete_view(Long id) {
    IncomeEntity Income = IncomeEntity.findById(id);
    if (Income == null) {
      throw new WebApplicationException("Income with id: " + id + " not found", 404);
    }
    Income.delete();
    List<IncomeEntity> incomelist = IncomeEntity.listAll(Sort.by("id"));
    return Templates.listview(incomelist);
  }

  /* REST INTERFACE */

  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<IncomeEntity> list() {
    List<IncomeEntity> incomelist = IncomeEntity.listAll(Sort.by("id"));
    return incomelist;
  }

  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public IncomeEntity get(long id) {
    IncomeEntity income = IncomeEntity.findById(id);
    return income;
  }

  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public IncomeEntity create(IncomeEntity entity) {
    entity.persist();
    return entity;
  }

  @PUT
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public IncomeEntity update(Long id, IncomeEntity Income) {
    IncomeEntity entity = IncomeEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Income with id: " + id + " not found", 404);
    }
    entity.name = Income.name;
    entity.amount = Income.amount;
    entity.recurrence = Income.recurrence;
    entity.date_occurence = Income.date_occurence;
    return entity;
  }

  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(Long id) {
    IncomeEntity entity = IncomeEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Income with id: " + id + " not found", 404);
    }
    entity.delete();
  }
  /*
  @GET
  @Path("search/name/{name}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public IncomeEntity search_name(String name) {
    IncomeEntity Income = IncomeEntity.findByName(name);
    return Income;
  }
  */


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
