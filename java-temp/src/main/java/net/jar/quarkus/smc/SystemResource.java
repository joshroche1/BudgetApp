package net.jar.quarkus.smc;

import java.util.List;
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

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

@Path("system")
@ApplicationScoped
public class SystemResource {

  private static final Logger LOGGER = Logger.getLogger(SystemResource.class.getName());

  @CheckedTemplate
  static class Templates {
    static native TemplateInstance list(List<SystemEntity> systemlist, List<ConfigEntity> categorylist, List<ConfigEntity> grouplist, List<ConfigEntity> oslist, List<ConfigEntity> zonelist, List<ConfigEntity> rolelist, List<ConfigEntity> providerlist);
    static native TemplateInstance grid(List<SystemEntity> systemlist, List<ConfigEntity> categorylist, List<ConfigEntity> grouplist, List<ConfigEntity> oslist, List<ConfigEntity> zonelist, List<ConfigEntity> rolelist, List<ConfigEntity> providerlist);
    static native TemplateInstance detail(SystemEntity system, List<ConfigEntity> categorylist, List<ConfigEntity> grouplist, List<ConfigEntity> oslist, List<ConfigEntity> zonelist, List<ConfigEntity> rolelist, List<ConfigEntity> providerlist);
//    static native TemplateInstance create();
  }
  
  @GET
  @Path("list")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list() {
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by("hostname"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.list(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  @GET
  @Path("grid")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance grid() {
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by("hostname"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.grid(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  @GET
  @Path("detail/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance detail(Long id) {
    SystemEntity system = SystemEntity.findById(id);
    if (system == null) {
      throw new WebApplicationException("System with id: " + id + " not found", 404);
    }
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.detail(system, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
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
  public TemplateInstance create(@FormParam("hostname") String hostname, @FormParam("machineid") String machineid, @FormParam("ipaddress") String ipaddress, @FormParam("os") String os, @FormParam("category") String category, @FormParam("groups") String groups, @FormParam("provider") String provider, @FormParam("role") String role, @FormParam("zone") String zone, @FormParam("notes") String notes) {
    SystemEntity entity = new SystemEntity();
    entity.hostname = hostname;
    entity.machineid = machineid;
    entity.ipaddress = ipaddress;
    entity.os = os;
    entity.category = category;
    entity.groups = groups;
    entity.provider = provider;
    entity.role = role;
    entity.zone = zone;
    entity.notes = notes;
    entity.persist();
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by("hostname"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.list(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  @POST
  @Path("update/{id}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update(@PathParam("id") Long id, @FormParam("hostname") String hostname, @FormParam("ipaddress") String ipaddress, @FormParam("os") String os, @FormParam("category") String category, @FormParam("groups") String groups, @FormParam("notes") String notes) {
    SystemEntity entity = SystemEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("System with id: " + id + " not found", 404);
    }
    entity.hostname = hostname;
    entity.ipaddress = ipaddress;
    entity.os = os;
    entity.category = category;
    entity.groups = groups;
    entity.notes = notes;
    entity.persist();
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by("hostname"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.list(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  @POST
  @Path("update/{id}/{field}")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance update_field(@PathParam("id") Long id, @PathParam("field") String field, @FormParam("newvalue") String newvalue) {
    SystemEntity entity = SystemEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("System with id: " + id + " not found", 404);
    }
    switch(field) {
      case "hostname":
        entity.hostname = newvalue;
        entity.persist();
        break;
      case "machineid":
        entity.machineid = newvalue;
        entity.persist();
        break;
      case "ipaddress":
        entity.ipaddress = newvalue;
        entity.persist();
        break;
      case "category":
        entity.category = newvalue;
        entity.persist();
        break;
      case "groups":
        entity.groups = newvalue;
        entity.persist();
        break;
      case "os":
        entity.os = newvalue;
        entity.persist();
        break;
      case "provider":
        entity.provider = newvalue;
        entity.persist();
        break;
      case "datacenter":
        entity.datacenter = newvalue;
        entity.persist();
        break;
      case "country":
        entity.country = newvalue;
        entity.persist();
        break;
      case "role":
        entity.role = newvalue;
        entity.persist();
        break;
      case "zone":
        entity.zone = newvalue;
        entity.persist();
        break;
      case "notes":
        entity.notes = newvalue;
        entity.persist();
        break;
      default:
        break;
    }
    SystemEntity system = SystemEntity.findById(id);
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.detail(system, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  @POST
  @Path("delete/{id}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Transactional
  public TemplateInstance remove(@PathParam("id") Long id) {
    SystemEntity entity = SystemEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("System with id: " + id + " not found", 404);
    }
    entity.delete();
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by("hostname"));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.list(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  /* Filtered, Sorted Views */
  
  @POST
  @Path("list/filtered")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_filtered(@FormParam("filterkey") String filterkey, @FormParam("filtervalue") String filtervalue) {
    List<SystemEntity> systemlist;
    String filterval = filtervalue.toLowerCase();
    System.out.println(filterkey + " " + filtervalue + " " + filterval);
    switch(filterkey) {
      case "Category": systemlist = SystemEntity.findByCategory(filterval); break;
      case "Group": systemlist = SystemEntity.findByGroup(filterval); break;
      case "Role": systemlist = SystemEntity.findByRole(filtervalue); break;
      case "Zone": systemlist = SystemEntity.findByZone(filterval); break;
      case "Provider": systemlist = SystemEntity.findByProvider(filtervalue); break;
      default: systemlist = SystemEntity.listAll(Sort.by("hostname")); break;
    }
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.list(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  @GET
  @Path("list/sorted/{col}")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance list_sorted(@PathParam("col") String col) {
    List<SystemEntity> systemlist = SystemEntity.listAll(Sort.by(col));
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.list(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  @POST
  @Path("grid/filtered")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance grid_filtered(@FormParam("filterkey") String filterkey, @FormParam("filtervalue") String filtervalue) {
    List<SystemEntity> systemlist;
    String filterval = filtervalue.toLowerCase();
    System.out.println(filterkey + " " + filtervalue + " " + filterval);
    switch(filterkey) {
      case "Category": systemlist = SystemEntity.findByCategory(filterval); break;
      case "Group": systemlist = SystemEntity.findByGroup(filterval); break;
      case "Role": systemlist = SystemEntity.findByRole(filtervalue); break;
      case "Zone": systemlist = SystemEntity.findByZone(filterval); break;
      case "Provider": systemlist = SystemEntity.findByProvider(filtervalue); break;
      default: systemlist = SystemEntity.listAll(Sort.by("hostname")); break;
    }
    List<ConfigEntity> categorylist = ConfigEntity.findByName("Category");
    List<ConfigEntity> grouplist = ConfigEntity.findByName("Group");
    List<ConfigEntity> oslist = ConfigEntity.findByName("OS");
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<ConfigEntity> rolelist = ConfigEntity.findByName("Role");
    List<ConfigEntity> providerlist = ConfigEntity.findByName("Provider");
    return Templates.grid(systemlist, categorylist, grouplist, oslist, zonelist, rolelist, providerlist);
  }
  
  /* REST Interface */
  
  @GET
  @Path("all")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public List<SystemEntity> all() {
    return SystemEntity.listAll(Sort.by("hostname"));
  }
  
  @GET
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  public SystemEntity get(@PathParam("id") Long id) {
    SystemEntity system = SystemEntity.findById(id);
    if (system == null) {
      throw new WebApplicationException("System with id: " + id + " not found", 404);
    }
    return system;
  }
  
  @POST
  @Path("add")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public SystemEntity add(SystemEntity entity) {
    entity.persist();
    return entity;
  }
  
  @POST
  @Path("{id}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Transactional
  public void delete(@PathParam("id") Long id) {
    SystemEntity entity = SystemEntity.findById(id);
    if (entity == null) {
      throw new WebApplicationException("System with id: " + id + " not found", 404);
    }
    entity.delete();
  }
  
  @GET
  @Path("search/hostname/{hostname}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public SystemEntity search_hostname(String hostname) {
    SystemEntity system = SystemEntity.findByHostname(hostname);
    return system;
  }
  
  @GET
  @Path("search/ipaddress/{ipaddress}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public SystemEntity search_ipaddress(String ipaddress) {
    SystemEntity system = SystemEntity.findByIP(ipaddress);
    return system;
  }
  
  @GET
  @Path("search/category/{category}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<SystemEntity> search_category(String category) {
    List<SystemEntity> systemlist = SystemEntity.findByCategory(category);
    return systemlist;
  }
  
  @GET
  @Path("search/group/{group}")
  @RolesAllowed("user")
  @Produces(MediaType.APPLICATION_JSON)
  @Blocking
  public List<SystemEntity> search_group(String group) {
    List<SystemEntity> systemlist = SystemEntity.findByGroup(group);
    return systemlist;
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
