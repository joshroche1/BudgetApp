package net.jar.quarkus.smc;

import java.io.File;
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
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
import io.quarkus.panache.common.Sort;
import io.quarkus.qute.CheckedTemplate;
import io.quarkus.qute.TemplateExtension;
import io.quarkus.qute.TemplateInstance;
import io.smallrye.common.annotation.Blocking;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

@Path("playbook")
@ApplicationScoped
public class PlaybookResource {

  private static final Logger LOGGER = Logger.getLogger(PlaybookResource.class.getName());
  
  @ConfigProperty(name = "smc.ansible.playbook-directory")
  String playbookdir;

  @CheckedTemplate
  static class Templates {
    static native TemplateInstance list(List<PlaybookEntity> playbooklist, List<ConfigEntity> categorylist, List<ConfigEntity> grouplist);
    static native TemplateInstance grid(List<PlaybookEntity> playbooklist, List<ConfigEntity> categorylist, List<ConfigEntity> grouplist);
    static native TemplateInstance detail(PlaybookEntity playbook, List<ConfigEntity> categorylist, List<ConfigEntity> grouplist);
//    static native TemplateInstance create();
    static native TemplateInstance run(List<PlaybookEntity> playbooklist, List<SystemEntity> systemlist, ArrayList<String> results);
  }
  
  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list() {
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.list(playbooklist, categorylist, grouplist);
  }
  
  @GET
  @Path("grid")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance grid() {
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.grid(playbooklist, categorylist, grouplist);
  }
  
  @GET
  @Path("detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail(Long id) {
    PlaybookEntity playbook = PlaybookEntity.findById(id);
    if (playbook == null) {
      throw new WebApplicationException("playbook with id: " + id + " not found", 404);
    }
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.detail(playbook, categorylist, grouplist);
  } 
  
/*  @GET
  @Path("create")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  public TemplateInstance create() {
    return Templates.create();
  } */
  
  @POST
  @Path("create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance create(@FormParam("filename") String filename, @FormParam("content") String content, @FormParam("category") String category, @FormParam("groups") String groups, @FormParam("notes") String notes) {
    PlaybookEntity entity = new PlaybookEntity();
    entity.filename = filename;
    entity.content = content;
    entity.category = category;
    entity.groups = groups;
    entity.notes = notes;
    entity.persist();
    String filepath = "/opt/smc/ansible/playbooks/" + filename;
    String result = FilesystemResource.createFile(filepath, content);
    LOGGER.info("Saved Playbook: " + result);
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.list(playbooklist, categorylist, grouplist);
  }
  
  @POST
  @Path("update/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update(@PathParam("id") Long id, @FormParam("filename") String filename, @FormParam("content") String content, @FormParam("category") String category, @FormParam("groups") String groups, @FormParam("notes") String notes) {
    PlaybookEntity entity = PlaybookEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Playbook with id: " + id + " not found", 404);
    }
    entity.filename = filename;
    entity.content = content;
    entity.category = category;
    entity.groups = groups;
    entity.notes = notes;
    entity.persist();
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.list(playbooklist, categorylist, grouplist);
  }
  
  @POST
  @Path("delete/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance remove(@PathParam("id") Long id) {
    PlaybookEntity entity = PlaybookEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Playbook with id: " + id + " not found", 404);
    }
    String filename = entity.filename;
    entity.delete();
    String filepath = "/opt/smc/ansible/playbooks/" + filename;
    if (FilesystemResource.deleteFile(filepath)) {
      LOGGER.info("Deleted Playbook File: " + filepath);
    }
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.list(playbooklist, categorylist, grouplist);
  }
  
  @POST
  @Path("upload")
  @RolesAllowed("user")
  @Consumes(MediaType.MULTIPART_FORM_DATA)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance testpage_upload(@FormParam("uploadplaybook") File uploadplaybook) {
    LOGGER.info(uploadplaybook.getName());
    String result = "";
    try {
      Scanner filescan = new Scanner(uploadplaybook);
      String filecontents = "";
      while (filescan.hasNextLine()) {
        filecontents += filescan.nextLine();
      }
      PlaybookEntity entity = new PlaybookEntity();
      entity.filename = uploadplaybook.getName();
      entity.content = filecontents;
      entity.category = "";
      entity.groups = "Default";
      entity.notes = "File Import";
      entity.persist();
      String filepath = playbookdir + uploadplaybook.getName();
      result = FilesystemResource.createFile(filepath,filecontents);
      LOGGER.info(result);
      filescan.close();
    } catch (Exception ex) {
      result = ex.toString();
      LOGGER.warn(result);
    }
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.list(playbooklist, categorylist, grouplist);
  }
  
  @GET
  @Path("list/sorted/{col}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_sorted(@PathParam("col") String col) {
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by(col));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    return Templates.list(playbooklist, categorylist, grouplist);
  }
  
  @GET
  @Path("run")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance run() {
    ArrayList<String> results = new ArrayList<String>();
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.run(playbooklist, systemlist, results);
  }
  
  @POST
  @Path("run")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance run_pb(@FormParam("system") String system, @FormParam("playbook") String playbook, @FormParam("exkey1") String exkey1, @FormParam("exvalue1") String exvalue1, @FormParam("exkey2") String exkey2, @FormParam("exvalue2") String exvalue2, @FormParam("exkey3") String exkey3, @FormParam("exvalue3") String exvalue3, @FormParam("exkey4") String exkey4, @FormParam("exvalue4") String exvalue4) {
    String extravars = "";
    ArrayList<String> results = new ArrayList<String>();
    results = AnsibleResource.runPlaybook(playbook, system, extravars);
    List<PlaybookEntity> playbooklist = PlaybookEntity.listAll(Sort.by("filename"));
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.run(playbooklist, systemlist, results);
  }
  
  /* REST Interface */
  
  @GET
  @Path("all")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public List<PlaybookEntity> all() {
    return PlaybookEntity.listAll(Sort.by("filename"));
  }
  
  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public PlaybookEntity get(@PathParam("id") Long id) {
    PlaybookEntity playbook = PlaybookEntity.findById(id);
    if (playbook == null) {
      throw new WebApplicationException("Playbook with id: " + id + " not found", 404);
    }
    return playbook;
  }
  
  @POST
  @Path("add")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public PlaybookEntity add(PlaybookEntity entity) {
    entity.persist();
    return entity;
  }
  
  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(@PathParam("id") Long id) {
    PlaybookEntity entity = PlaybookEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("playbook with id: " + id + " not found", 404);
    }
    entity.delete();
  }
  
  @GET
  @Path("search/filename/{filename}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public PlaybookEntity search_filename(String filename) {
    PlaybookEntity playbook = PlaybookEntity.findByFilename(filename);
    return playbook;
  }
  
  @GET
  @Path("search/category/{category}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<PlaybookEntity> search_category(String category) {
    List<PlaybookEntity> playbooklist = PlaybookEntity.findByCategory(category);
    return playbooklist;
  }
  
  @GET
  @Path("search/group/{group}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<PlaybookEntity> search_group(String group) {
    List<PlaybookEntity> playbooklist = PlaybookEntity.findByGroup(group);
    return playbooklist;
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
