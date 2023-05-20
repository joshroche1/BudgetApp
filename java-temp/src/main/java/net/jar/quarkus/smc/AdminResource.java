package net.jar.quarkus.smc;

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
  
  @ConfigProperty(name = "smc.base-dir")
  String basedir;
  
  @ConfigProperty(name = "smc.ansible.hostsfile")
  String ansible_hostsfilepath;
  
  @ConfigProperty(name = "smc.ansible.configfile")
  String ansible_configfilepath;
  
  @ConfigProperty(name = "smc.ansible.directory")
  String ansible_directory;
  
  @ConfigProperty(name = "smc.ansible.playbook-directory")
  String ansible_playbookdirectory;
  
  @ConfigProperty(name = "quarkus.datasource.db-kind")
  String db_kind;
  
  @ConfigProperty(name = "quarkus.datasource.jdbc.url")
  String db_jdbc_url;
  
  @ConfigProperty(name = "quarkus.log.file.path")
  String logfile;
    
  HashMap<String, String> config_map;
  
  @CheckedTemplate
  static class Templates {
    static native TemplateInstance settings(List<ConfigEntity> providerlist, List<ConfigEntity> rolelist, List<ConfigEntity> zonelist, List<UserEntity> userlist, List<ConfigEntity> categorylist, List<ConfigEntity> grouplist, List<ConfigEntity> oslist, HashMap<String, String> configmap);
    static native TemplateInstance userprofile(UserEntity currentuser);
  }
  
  private HashMap<String, String> get_config() {
    config_map = new HashMap<String, String>();
    config_map.put("ansible_hostsfile", FilesystemResource.readFile(ansible_hostsfilepath));
    config_map.put("ansible_configfile", FilesystemResource.readFile(ansible_configfilepath));
    config_map.put("ansible_hostsfilepath", ansible_hostsfilepath);
    config_map.put("ansible_configfilepath", ansible_configfilepath);
    config_map.put("ansible_directory", ansible_directory);
    config_map.put("ansible_playbookdirectory", ansible_playbookdirectory);
    config_map.put("basedir", basedir);
    config_map.put("uploaddir", basedir + "upload/");
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
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
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
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
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
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
  }
  
  @POST
  @Path("category/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance category_create(@FormParam("value") String value) {
    ConfigEntity.add("Category",value);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
  }
  
  @POST
  @Path("category/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance category_delete(Long id) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Category with ID: " + id + " not found", 404);
    }
    entity.delete();
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
  }  
  
  @POST
  @Path("group/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance group_create(@FormParam("groupvalue") String groupvalue) {
    ConfigEntity.add("Group",groupvalue);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
  }
  
  @POST
  @Path("group/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance group_delete(Long id) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("Category with ID: " + id + " not found", 404);
    }
    entity.delete();
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
  }
  
  @POST
  @Path("os/create")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance os_create(@FormParam("osvalue") String osvalue) {
    ConfigEntity.add("OS",osvalue);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
  }
  
  @POST
  @Path("os/delete/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance os_delete(Long id) {
    ConfigEntity entity = ConfigEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("OS with ID: " + id + " not found", 404);
    }
    entity.delete();
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<UserEntity> userlist = UserEntity.listAll(Sort.by("username"));
    HashMap<String, String> configmap = get_config();
    return Templates.settings(providerlist, rolelist, zonelist, userlist, categorylist, grouplist, oslist, configmap);
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