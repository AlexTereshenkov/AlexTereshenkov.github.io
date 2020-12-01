import subprocess
import shutil

import apt

# check that tree is not installed
print(f"tree executable location: {shutil.which('tree')}")

# update the cache
cache = apt.cache.Cache()
cache.update()
cache.open()

# mark packages you'd like to install
package = cache['tree']
package.candidate = package.versions.get('1.7.0-5')
package.mark_install()
cache.commit()

# open the cache again and inspect installed package
cache = apt.cache.Cache()
pkg = cache.get('tree')
print(f"Package installed: {pkg.is_installed}; version: {pkg.installed.source_version}")
print(f"Package location: {shutil.which('tree')}")

# delete the package
pkg.mark_delete()
cache.commit()

# open the cache again and check that the tree package is gone
cache = apt.cache.Cache()
print(f"tree executable location: {shutil.which('tree')}")
