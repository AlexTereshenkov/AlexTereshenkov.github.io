import subprocess
import aptsources.sourceslist as sourceslist

# showing original sources
sources = sourceslist.SourcesList()
uris_before = set([source.uri for source in sources.list])
print(uris_before)

# adding a custom apt source
source = ("deb [trusted=yes]", "http://download.virtualbox.org/virtualbox/debian",
          "bionic", ["contrib"])
sources.add(*source)
sources.save()

# showing extended sources
uris_after = set([source.uri for source in sources.list])
print(uris_after)

# printing the contents of the sources.list file
process = subprocess.Popen(["tail", "/etc/apt/sources.list"],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
out, errors = process.communicate()
print(out.decode())
print(errors.decode())

# install a package from the VirtualBox Debian pool
...
