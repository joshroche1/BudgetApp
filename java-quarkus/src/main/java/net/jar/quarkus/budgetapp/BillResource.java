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

@Path("bills")
@ApplicationScoped
public class BillResource {

  private static final Logger LOGGER = Logger.getLogger(BillResource.class.getName());


  @CheckedTemplate
  static class Templates {
    static native TemplateInstance listview(List<BillEntity> billlist);
    static native TemplateInstance createview();
    static native TemplateInstance detailview(BillEntity bill);
  }
  
  @GET
  @Path("view/list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_view() {
    List<BillEntity> billlist = BillEntity.listAll(Sort.by("id"));
    return Templates.listview(billlist);
  }
  
  @GET
  @Path("view/create")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance create_view() {
    return Templates.createview();
  }
  
  @POST
  @Path("view/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create_form(@FormParam("name") String name, @FormParam("amount") String amount, @FormParam("recurrence") String recurrence, @FormParam("date_occurence") String date_occurence) {
    BillEntity entity = new BillEntity();
    entity.name = name;
    entity.amount = amount;
    entity.recurrence = recurrence;
    entity.date_occurence = date_occurence;
    entity.persist();
    List<BillEntity> billlist = BillEntity.listAll(Sort.by("id"));
    return Templates.listview(billlist);
  }
  
  @GET
  @Path("view/detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail_view(Long id) {
    BillEntity bill = BillEntity.findById(id);
    if (bill == null) {
      throw new WebApplicationException("Bill with id: " + id + " not found", 404);
    }
    return Templates.detailview(bill);
  }
  
  @POST
  @Path("view/update/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update_view(Long id, @FormParam("name") String name, @FormParam("amount") String amount, @FormParam("recurrence") String recurrence, @FormParam("date_occurence") String date_occurence) {
    BillEntity entity = BillEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Bill with id: " + id + " not found", 404);
    }
    if (name != "") { entity.name = name; }
    if (amount != "") { entity.amount = amount; }
    if (recurrence != "") { entity.recurrence = recurrence; }
    if (date_occurence != "") { entity.date_occurence = date_occurence; }
    entity.persist();
    return Templates.detailview(entity);
  }
  
  @POST
  @Path("view/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance delete_view(Long id) {
    BillEntity bill = BillEntity.findById(id);
    if (bill == null) {
      throw new WebApplicationException("Bill with id: " + id + " not found", 404);
    }
    bill.delete();
    List<BillEntity> billlist = BillEntity.listAll(Sort.by("id"));
    return Templates.listview(billlist);
  }

  /* REST INTERFACE */

  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<BillEntity> list() {
    List<BillEntity> billlist = BillEntity.listAll(Sort.by("id"));
    return billlist;
  }

  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public BillEntity get(long id) {
    BillEntity bill = BillEntity.findById(id);
    return bill;
  }

  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public BillEntity create(BillEntity entity) {
    entity.persist();
    return entity;
  }

  @PUT
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public BillEntity update(Long id, BillEntity bill) {
    BillEntity entity = BillEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Bill with id: " + id + " not found", 404);
    }
    entity.name = bill.name;
    entity.amount = bill.amount;
    entity.recurrence = bill.recurrence;
    entity.date_occurence = bill.date_occurence;
    return entity;
  }

  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(Long id) {
    BillEntity entity = BillEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Bill with id: " + id + " not found", 404);
    }
    entity.delete();
  }
  /*
  @GET
  @Path("search/name/{name}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public BillEntity search_name(String name) {
    BillEntity bill = BillEntity.findByName(name);
    return bill;
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
