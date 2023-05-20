package net.jar.quarkus.smc;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;
import javax.annotation.security.RolesAllowed;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.persistence.EntityManager;
import javax.transaction.Transactional;
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
import io.smallrye.common.annotation.Blocking;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

@ApplicationScoped
public class FilesystemResource {

  private static final Logger LOGGER = Logger.getLogger(FilesystemResource.class.getName());
  
  @ConfigProperty(name = "smc.base-dir")
  String basedir;

  // read directory
  public static List<String> readDirectory(String dirpath) {
    List<String> result = new ArrayList<String>();
    Path dir = Paths.get(dirpath);
    try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir)) {
      for (Path file: stream) {
        result.add(file.getFileName().toString());
      }
    } catch (IOException x) {    
      System.err.println(x);
    }
    return result;
  }
  
  // read file
  public static String readFile(String filepath) {
    String filecontents = "";
    try {
      Path fpath = Paths.get(filepath);
      Charset chset = Charset.forName("UTF-8");
      List<String> lines = Files.readAllLines(fpath, chset);
      for (String line : lines) {
        filecontents += line + "\n";
      }
      LOGGER.info("Read file: " + filepath);
    } catch (Exception ex) {
      LOGGER.error(ex.getMessage(), ex);
      filecontents = ex.getMessage();
    }
    return filecontents;
  }
  
  // create file
  public static String createFile(String filepath, String contents) {
    String result = "";
    try {
      Path fpath = Paths.get(filepath);
      Path createFilePath = Files.createFile(fpath);
      Files.write(fpath, contents.getBytes());
      result = filepath;
    } catch (Exception ex) {
      LOGGER.error(ex.getMessage(), ex);
      result = ex.getMessage();
    }
    return result;
  }
  
  // overwrite file
  public static String updateFile(String filepath, String contents) {
    String result = "";
    
    return result;
  }
  
  // delete file
  public static boolean deleteFile(String filepath) {
    boolean result = false;
    try {
      Path fpath = Paths.get(filepath);
      Files.delete(fpath);
      result = true;
    } catch (Exception ex) {
      LOGGER.error(ex.getMessage(), ex);
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
