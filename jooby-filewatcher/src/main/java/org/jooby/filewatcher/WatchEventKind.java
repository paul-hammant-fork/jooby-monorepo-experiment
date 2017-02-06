package org.jooby.filewatcher;

import java.nio.file.Path;
import java.nio.file.WatchEvent;

class WatchEventKind implements WatchEvent.Kind<Path> {

  private String name;

  public WatchEventKind(final String name) {
    this.name = name.toUpperCase();
  }

  @Override
  public String toString() {
    return name;
  }

  @Override
  public String name() {
    return name;
  }

  @Override
  public Class<Path> type() {
    return Path.class;
  }

}
