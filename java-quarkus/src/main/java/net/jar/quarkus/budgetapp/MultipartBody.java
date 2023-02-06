package net.jar.quarkus.budgetapp;

import java.io.InputStream;

import javax.ws.rs.FormParam;
import javax.ws.rs.core.MediaType;

import org.jboss.resteasy.annotations.providers.multipart.PartType;

public class MultipartBody {

  @FormParam("file")
  @PartType(MediaType.TEXT_PLAIN)
  public String file;

  @FormParam("fileName")
  @PartType(MediaType.TEXT_PLAIN)
  public String fileName;
  
}