package net.jar.quarkus.budgetapp;

import javax.enterprise.event.Observes;
import javax.inject.Singleton;
import javax.transaction.Transactional;

import io.quarkus.runtime.StartupEvent;

@Singleton
public class Startup {
  @Transactional
  public void loadUsers(@Observes StartupEvent evt) {
    // reset and load all test users
    UserEntity.add("user", "user", "user", "user@user.usr");
  }
}