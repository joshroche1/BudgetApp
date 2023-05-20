package net.jar.quarkus.smc;

import java.util.ArrayList;
import java.util.List;
import java.lang.Process;
import java.lang.ProcessBuilder;
import java.lang.StringBuilder;
import java.io.File;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.annotation.security.RolesAllowed;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.persistence.EntityManager;
import javax.transaction.Transactional;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
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


@ApplicationScoped
public class CommandResource {

  private static final Logger LOGGER = Logger.getLogger(CommandResource.class.getName());

  public static ArrayList<String> run_command(String cmd) {
    LOGGER.info("Run Command: " + cmd);
    String msg = "";
    ArrayList<String> result = new ArrayList<String>();
    try {
      ProcessBuilder processBuilder = new ProcessBuilder("bash", "-c", cmd);
      Process process = processBuilder.start();
      StringBuilder output = new StringBuilder();
      BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
      String line;
      while ((line = reader.readLine()) != null) {
        result.add(line);
        output.append(line + "\n");
      }
      int exitValue = process.waitFor();
      //result = output.toString();
      if (exitValue == 0) {
        return result;
      } else {
        result.add("ERROR");
      }
    } catch (Exception ex) {
      result.add("!EXCEPTION!:" + ex.getMessage());
    }
    return result;
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
