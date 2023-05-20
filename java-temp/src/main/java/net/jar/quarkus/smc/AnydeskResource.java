package net.jar.quarkus.smc;

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

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

@Path("ad")
@ApplicationScoped
public class AnydeskResource {

  private static final Logger LOGGER = Logger.getLogger(AnydeskResource.class.getName());

  @CheckedTemplate
  static class Templates {
    static native TemplateInstance ad_control(List<ConfigEntity> zonelist, List<SystemEntity> relaylist, ArrayList<String> results);
    static native TemplateInstance ad_relay(List<SystemEntity> relaylist, ArrayList<String> results);
    static native TemplateInstance ad_mad(List<SystemEntity> relaylist, ArrayList<String> results);
  }
  
  /* Views */
  
  @GET
  @Path("control")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_control() {
    ArrayList<String> results = new ArrayList<String>();
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_control(zonelist, relaylist, results);
  }
  
  @GET
  @Path("relay")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_relay() {
    ArrayList<String> results = new ArrayList<String>();
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_relay(relaylist, results);
  }
  
  @GET
  @Path("mad")
  @RolesAllowed("user")
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_mad() {
    ArrayList<String> results = new ArrayList<String>();
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_mad(relaylist, results);
  }
  
  /* Control Functions */
  
  @POST
  @Path("control/zonestats")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_control_zone_stats(@FormParam("zone_id") String zone_id) {
    LOGGER.info("AD Control - Get Zone Stats: " + zone_id);
    String extravars = "-e \"zone_id=" + zone_id + "\"";
    ArrayList<String> results = new ArrayList<String>();
    results = AnsibleResource.runPlaybook("zone-stats.yml", "control", extravars);
    List<ConfigEntity> zonelist = ConfigEntity.findByName("Zone");
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_control(zonelist, relaylist, results);
  }
  
  /* Relay Functions */
  
  @POST
  @Path("relay/weight/zero/multiple")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_relay_weight_zero_multiple(@FormParam("relay_ids") String relay_ids) {
    LOGGER.info("AD Relay - Set Relay Weight 0: " + relay_ids);
    String extravars = "-e \"relay_ids=" + relay_ids + "\"";
    ArrayList<String> results = new ArrayList<String>();
    results = AnsibleResource.runPlaybook("relay-set-zero-weight-multiple.yml", "control", extravars);
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_relay(relaylist, results);
  }
  
  @POST
  @Path("relay/weight/original/multiple")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_relay_weight_original_multiple(@FormParam("relay_ids") String relay_ids) {
    LOGGER.info("AD Relay - Set Relay Original Weight: " + relay_ids);
    String extravars = "-e \"relay_ids=" + relay_ids + "\"";
    ArrayList<String> results = new ArrayList<String>();
    results = AnsibleResource.runPlaybook("relay-set-original-weight-multiple.yml", "control", extravars);
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_relay(relaylist, results);
  }
  
  /* MAD Functions */
  
  @POST
  @Path("mad/find/bannedip")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_mad_find_ip(@FormParam("ipaddress") String ipaddress) {
    LOGGER.info("AD MAD - Find banned IP: " + ipaddress);
    String extravars = "-e \"ipaddress=" + ipaddress + "\"";
    ArrayList<String> results = new ArrayList<String>();
    results = AnsibleResource.runPlaybook("myad-find-banned-ip.yml", "www-console", extravars);
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_mad(relaylist, results);
  }
  
  @POST
  @Path("mad/ip/unban")
  @RolesAllowed("user")
  @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
  @Produces(MediaType.TEXT_HTML)
  @Blocking
  public TemplateInstance ad_mad_unban_ip(@FormParam("ipaddress") String ipaddress) {
    LOGGER.info("AD MAD - Unban IP Address: " + ipaddress);
    String extravars = "-e \"ipaddress=" + ipaddress + "\"";
    ArrayList<String> results = new ArrayList<String>();
    results = AnsibleResource.runPlaybook("myad-unban-ip.yml", "www-console", extravars);
    List<SystemEntity> relaylist = SystemEntity.listAll(Sort.by("hostname"));
    return Templates.ad_mad(relaylist, results);
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