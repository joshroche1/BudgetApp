package net.jar.quarkus.budgetapp;

import java.io.IOException;
import java.io.InputStream;
import java.io.BufferedReader;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
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

import org.jboss.resteasy.plugins.providers.multipart.InputPart;
import org.jboss.resteasy.plugins.providers.multipart.MultipartFormDataInput;

@Path("transactions")
@ApplicationScoped
public class TransactionResource {

  private static final Logger LOGGER = Logger.getLogger(TransactionResource.class.getName());


  @CheckedTemplate
  static class Templates {
    static native TemplateInstance listview(List<TransactionEntity> transactionlist);
    static native TemplateInstance createview(List<ConfigEntity> categorylist);
    static native TemplateInstance detailview(TransactionEntity transaction, List<ConfigEntity> categorylist);
  }
  
  @GET
  @Path("view/list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_view() {
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    return Templates.listview(transactionlist);
  }
  
  @GET
  @Path("view/create")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance create_view() {
    List<ConfigEntity> categorylist = ConfigResource.getList("category");
    return Templates.createview(categorylist);
  }
  
  @POST
  @Path("view/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create_form(@FormParam("name") String name, @FormParam("amount") String amount, @FormParam("datetimestamp") String datetimestamp, @FormParam("description") String description, @FormParam("category") String category, @FormParam("reference") String reference) {
    String msg = " " + name + " " + amount + " " + datetimestamp + " " + description + " " + category + " " + reference;
    LOGGER.info(msg);
    TransactionEntity entity = new TransactionEntity();
    entity.name = name;
    Double amt = new Double(amount);
    entity.amount = amt;
    try {
      DateFormat formatter = new SimpleDateFormat("yyyy-MM-dd'T'hh:mm");
      Date dts = (Date)formatter.parse(datetimestamp);
      entity.datetimestamp = dts;
    } catch (Exception ex) {
      LOGGER.error(ex.getMessage());
    }
    entity.description = description;
    entity.category = category;
    entity.reference = reference;
    entity.persist();
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    return Templates.listview(transactionlist);
  }
  
  @GET
  @Path("view/detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail_view(Long id) {
    TransactionEntity transaction = TransactionEntity.findById(id);
    if (transaction == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    List<ConfigEntity> categorylist = ConfigResource.getList("category");
    return Templates.detailview(transaction, categorylist);
  }
  
  @POST
  @Path("view/update/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update_view(Long id, @FormParam("name") String name, @FormParam("amount") Double amount, @FormParam("datetimestamp") Date datetimestamp, @FormParam("description") String description, @FormParam("category") String category, @FormParam("reference") String reference) {
    TransactionEntity entity = TransactionEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    if (name != "") { entity.name = name; }
    if (amount != null) { entity.amount = amount; }
    if (datetimestamp != null) { entity.datetimestamp = datetimestamp; }
    if (description != "") { entity.description = description; }
    if (category != "") { entity.category = category; }
    if (reference != "") { entity.reference = reference; }
    entity.persist();
    List<ConfigEntity> categorylist = ConfigResource.getList("category");
    return Templates.detailview(entity, categorylist);
  }
  
  @POST
  @Path("view/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance delete_view(Long id) {
    TransactionEntity transaction = TransactionEntity.findById(id);
    if (transaction == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    transaction.delete();
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    return Templates.listview(transactionlist);
  }
  
  @POST
  @Path("view/importcsv")
  @RolesAllowed("user")
  @Consumes(MediaType.MULTIPART_FORM_DATA)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance import_csv_view(MultipartFormDataInput csvdatainput) {
    try {
    Map<String, List<InputPart>> map = csvdatainput.getFormDataMap();
    for (Iterator<String> it = map.keySet().iterator(); it.hasNext();) {
      String key = it.next();
      InputPart inputPart = map.get(key).iterator().next();
      LOGGER.info(key);
      LOGGER.info(inputPart.getBodyAsString());
    }
    /*
    InputStream inputStream = csvfile.getInputStream();
    BufferedReader br = new BufferedReader(new InputStreamReader(inputStream));
    String result = "";
    while (br.readLine() != null) {
      result += br.readLine();
    }
    */
    LOGGER.info(csvdatainput.toString());
    //LOGGER.info(result);
    } catch (Exception ex) {
      LOGGER.error(ex.getMessage());
    }
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    return Templates.listview(transactionlist);
  }

  /* REST INTERFACE */

  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<TransactionEntity> list() {
    List<TransactionEntity> transactionlist = TransactionEntity.listAll(Sort.by("id"));
    return transactionlist;
  }

  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public TransactionEntity get(long id) {
    TransactionEntity transaction = TransactionEntity.findById(id);
    return transaction;
  }

  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public TransactionEntity create(TransactionEntity entity) {
    entity.persist();
    return entity;
  }

  @PUT
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public TransactionEntity update(Long id, TransactionEntity transaction) {
    TransactionEntity entity = TransactionEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    entity.name = transaction.name;
    entity.amount = transaction.amount;
    entity.datetimestamp = transaction.datetimestamp;
    entity.description = transaction.description;
    entity.category = transaction.category;
    entity.reference = transaction.reference;
    return entity;
  }

  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(Long id) {
    TransactionEntity entity = TransactionEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Transaction with id: " + id + " not found", 404);
    }
    entity.delete();
  }
  /*
  @GET
  @Path("search/name/{name}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public TransactionEntity search_name(String name) {
    TransactionEntity transaction = TransactionEntity.findByName(name);
    return transaction;
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
