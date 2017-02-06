package org.jooby.filewatcher;

import java.nio.file.Path;
import java.nio.file.PathMatcher;
import java.util.List;

class FirstOfPathMatcher implements PathMatcher {

  private List<PathMatcher> matchers;

  FirstOfPathMatcher(final List<PathMatcher> matchers) {
    this.matchers = matchers;
  }

  @Override
  public boolean matches(final Path path) {
    for (PathMatcher matcher : matchers) {
      if (matcher.matches(path)) {
        return true;
      }
    }
    return false;
  }

  @Override
  public String toString() {
    return this.matchers.toString();
  }
}
