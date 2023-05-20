package net.jar.quarkus.smc;

import javax.enterprise.event.Observes;
import javax.inject.Singleton;
import javax.transaction.Transactional;
import org.jboss.logging.Logger;
import io.quarkus.runtime.StartupEvent;

@Singleton
public class Startup {
  
  private static final Logger LOGGER = Logger.getLogger(AdminResource.class.getName());
  
  @Transactional
  public void loadDefaults(@Observes StartupEvent evt) {
    // Init objects
    SystemEntity system = SystemEntity.findByHostname("localhost");
    if (system == null) {
      SystemEntity entity = new SystemEntity();
      entity.hostname = "localhost";
      entity.ipaddress = "127.0.0.1";
      entity.category = "desktop";
      entity.groups = "Default";
      entity.notes = "test Test TEST";
      entity.os = "Operating System";
      entity.persist();
      LOGGER.info("Added localhost entity");
      SystemEntity test1 = new SystemEntity();
      test1.hostname = "pgsql";
      test1.ipaddress = "10.0.0.2";
      test1.category = "Container";
      test1.groups = "Default";
      test1.notes = "LXD Container";
      test1.os = "Debian";
      test1.persist();
      LOGGER.info("Added test1 entity");
    }
    
    PlaybookEntity pb = PlaybookEntity.findByFilename("get-facts.yml");
    if (pb == null) {
      PlaybookEntity playbook = new PlaybookEntity();
      playbook.filename = "get-facts.yml";
      playbook.content = "---\n- hosts:\n  - all\n  become: yes\n  gather_facts: yes\n  tasks:\n  - name: Hostname\n    debug:\n      var: ansible_facts.hostname\n  - name: nproc\n    debug:\n      var: ansible_facts.processor_nproc\n  - name: network interface\n    debug:\n      var: ansible_facts.default_ipv4.alias\n  - name: Disks\n    debug:\n      msg: '{{ item.device }} - {{ item.size_total }}'\n    loop: '{{ ansible_facts.mounts }}'";
      playbook.category = "desktop";
      playbook.groups = "Default";
      playbook.notes = "Test";
      playbook.persist();
      LOGGER.info("Added playbook entity"); 
    }
        
    ConfigEntity.add("Category", "Desktop");
    ConfigEntity.add("Category", "Laptop");
    ConfigEntity.add("Category", "Bare Metal");
    ConfigEntity.add("Category", "Virtual Machine");
    ConfigEntity.add("Category", "Container");
    ConfigEntity.add("Category", "Mobile");
    ConfigEntity.add("Category", "Other");
    
    ConfigEntity.add("Group", "Default");
    
    ConfigEntity.add("OS", "Windows 10/11");
    ConfigEntity.add("OS", "Windows Server 2019/2016");
    ConfigEntity.add("OS", "Other Windows OS");
    ConfigEntity.add("OS", "macOS");
    ConfigEntity.add("OS", "iOS");
    ConfigEntity.add("OS", "Ubuntu Desktop");
    ConfigEntity.add("OS", "Ubuntu Server");
    ConfigEntity.add("OS", "Debian");
    ConfigEntity.add("OS", "CentOS");
    ConfigEntity.add("OS", "RHEL");
    ConfigEntity.add("OS", "Fedora");
    ConfigEntity.add("OS", "Other Linux");
    ConfigEntity.add("OS", "Android");
    ConfigEntity.add("OS", "Other");
    
    UserEntity.add("admin", "admin", "user", "admin@admin.adm");
    LOGGER.info("Added user entity");
    
    /* AnyDesk Items */
    ConfigEntity.add("Provider", "Hetzner");
    ConfigEntity.add("Provider", "OVH");
    ConfigEntity.add("Provider", "Datapacket");
    ConfigEntity.add("Provider", "Limestone");
    ConfigEntity.add("Provider", "GCore");
    ConfigEntity.add("Provider", "Hostkey");
    ConfigEntity.add("Provider", "HQServ");
    ConfigEntity.add("Provider", "Leaseweb");
    ConfigEntity.add("Provider", "Linode");
    ConfigEntity.add("Provider", "Maxihost");
    ConfigEntity.add("Provider", "Streamline");
    ConfigEntity.add("Provider", "Other");
    
    ConfigEntity.add("Role", "Control");
    ConfigEntity.add("Role", "Database");
    ConfigEntity.add("Role", "Relay");
    ConfigEntity.add("Role", "Web");
    ConfigEntity.add("Role", "Other");
    
    ConfigEntity.add("Zone", "--");
    ConfigEntity.add("Zone", "AS");
    ConfigEntity.add("Zone", "AU");
    ConfigEntity.add("Zone", "BE_EU");
    ConfigEntity.add("Zone", "BG");
    ConfigEntity.add("Zone", "BT");
    ConfigEntity.add("Zone", "BT_V1");
    ConfigEntity.add("Zone", "BT_V2");
    ConfigEntity.add("Zone", "CN");
    ConfigEntity.add("Zone", "CN_JP");
    ConfigEntity.add("Zone", "CN_SC");
    ConfigEntity.add("Zone", "CN_SG");
    ConfigEntity.add("Zone", "ES");
    ConfigEntity.add("Zone", "EU");
    ConfigEntity.add("Zone", "FI");
    ConfigEntity.add("Zone", "GB");
    ConfigEntity.add("Zone", "IL");
    ConfigEntity.add("Zone", "IN");
    ConfigEntity.add("Zone", "JP");
    ConfigEntity.add("Zone", "KZ");
    ConfigEntity.add("Zone", "MA");
    ConfigEntity.add("Zone", "SA");
    ConfigEntity.add("Zone", "TR");
    ConfigEntity.add("Zone", "US");
    ConfigEntity.add("Zone", "US_CA");
    ConfigEntity.add("Zone", "US_FL");
    ConfigEntity.add("Zone", "US_IL");
    ConfigEntity.add("Zone", "US_NY");
    ConfigEntity.add("Zone", "US_TX");
    ConfigEntity.add("Zone", "US_VA");
    ConfigEntity.add("Zone", "US_WA");
    ConfigEntity.add("Zone", "XX");
    ConfigEntity.add("Zone", "XY");
    ConfigEntity.add("Zone", "ZA");
  }
}