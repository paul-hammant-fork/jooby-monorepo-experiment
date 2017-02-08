#!/usr/bin/python
import os
import sys
import shutil
from subprocess import call

def needThis(neededModule, depMap, neededModules2):
    if neededModule in depMap:
        for dependency in depMap[neededModule]:
            needThis(dependency, depMap, neededModules2)
    neededModules2[neededModule] = True

def writepom(pom_template):
    dirname = os.path.dirname(pom_template)
    with open(pom_template) as f:
        if os.path.exists(dirname + '/pom.xml'):
            os.chmod(dirname + '/pom.xml', 0755)
        with open(dirname + '/pom.xml', 'w') as the_pom:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith("<module>") and line.strip().endswith("</module>"):
                    sub_project = line.strip()[8:]
                    sub_project = sub_project[:sub_project.index("<")]
                    f_path = dirname + "/" + sub_project
                    if os.path.exists(f_path + '/pom.xml') or os.path.exists(f_path + '/pom-template.xml'):
                        the_pom.write(line)
                else:
                    the_pom.write(line)
        os.chmod(dirname + '/pom.xml', 0444)

def recursive_delete_if_empty(path):
    """Recursively delete empty directories; return True
    if everything was deleted."""

    if not os.path.isdir(path):
        # If you also want to delete some files like desktop.ini, check
        # for that here, and return True if you delete them.
        return False

    # Note that the list comprehension here is necessary, a
    # generator expression would shortcut and we don't want that!
    if all([recursive_delete_if_empty(os.path.join(path, filename))
            for filename in os.listdir(path)]):
        # Either there was nothing here or it was all deleted
        os.rmdir(path)
        return True
    else:
        return False

neededModules = {}
depMap = {}

# passed in args into dict
for ix, arg in enumerate(sys.argv):
    if ix > 0:
        neededModules[arg] = True

# crunch dot graph into Python dict
with open("mr/dependency-graph.dot") as dot:
    lines = dot.readlines()
    for line in lines:
        line = line.replace("\"","")
        if " -> " in line:
            parts = line.split(" -> ")
            lpart = parts[0].split(":")[1]
            rpart = parts[1].split(":")[1]
            if lpart not in depMap:
                depMap[lpart] = {}
                depMap[lpart][rpart] = True

    # penultimate list of deps we need, tree into flat
    neededModules2 = {}
    for neededModule in neededModules:
        needThis(neededModule, depMap, neededModules2)

    # we always need these
    sparse_checkout = "/.gitignore\n/.gitattributes\n/checkstyle.xml\n/LICENSE\n/mr/*\n/README.md\n/pom-template.xml\n"

    with open("mr/all_poms.txt") as allpoms:
        lines = allpoms.readlines()
        for line in lines:
            hit = False
            for neededModule in neededModules2:
                if "/"+neededModule+"/" in line:
                    sparse_checkout += line[1:]
                    sparse_checkout += line[1:].replace("pom-template.xml","src/*")

        # Redo sparse-checkout file
        with open('.git/info/sparse-checkout', 'w') as sc:
            if len(sys.argv) == 1:
                sc.write("/*")
            else:
                sc.write(sparse_checkout)

        # Remove old pom files
        for root, dirs, files in os.walk("."):
            for currentFile in files:
                path_join = os.path.join(root, currentFile)
                if path_join.endswith("/pom.xml"):
                    os.remove(path_join)

        # sparse re-checkout
        call(["git", "checkout", "--"])

        # Write new pom files if approriate
        for root, dirs, files in os.walk("."):
            for currentFile in files:
                fullpath = os.path.join(root, currentFile)
                if fullpath.endswith("/pom-template.xml"):
                    writepom(fullpath)

        # Delete orphaned target folders and Intellij .iml files
        dirs_to_delete = []
        files_to_delete = []
        for root, dirs, files in os.walk("."):
            for currentDir in dirs:
                fullpath = os.path.join(root, currentDir)
                if fullpath.endswith("/target") and not os.path.exists(os.path.dirname(fullpath) + '/pom.xml'):
                    dirs_to_delete.append(fullpath)
            for currentFile in files:
                fullpath = os.path.join(root, currentFile)
                if fullpath.endswith(".iml") and not os.path.exists(os.path.dirname(fullpath) + '/pom.xml'):
                    files_to_delete.append(fullpath)

        for fullpath in dirs_to_delete:
            shutil.rmtree(fullpath)
        for fullpath in files_to_delete:
            os.remove(fullpath)

        recursive_delete_if_empty(".")
