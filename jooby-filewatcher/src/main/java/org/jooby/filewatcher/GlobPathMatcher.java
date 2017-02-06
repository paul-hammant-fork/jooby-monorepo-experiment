package org.jooby.filewatcher;

import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.PathMatcher;

class GlobPathMatcher implements PathMatcher {

  private String expression;

  private PathMatcher matcher;

  public GlobPathMatcher(final String expression) {
    this.expression = expression.trim();
    this.matcher = FileSystems.getDefault().getPathMatcher("glob:" + this.expression);
  }

  @Override
  public boolean matches(final Path path) {
    return matcher.matches(path);
  }

  @Override
  public String toString() {
    return expression;
  }

}
