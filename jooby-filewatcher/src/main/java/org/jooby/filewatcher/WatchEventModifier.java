package org.jooby.filewatcher;

import java.nio.file.WatchEvent;

class WatchEventModifier implements WatchEvent.Modifier {

  private String name;

  public WatchEventModifier(final String name) {
    this.name = name.toUpperCase();
  }

  @Override
  public String name() {
    return name;
  }

  @Override
  public String toString() {
    return name;
  }
}
