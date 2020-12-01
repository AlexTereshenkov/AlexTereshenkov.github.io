import re
import apt_pkg
apt_pkg.init_config()
apt_pkg.init_system()

pkgs = [pkg for pkg in apt_pkg.Cache().packages if re.compile(r'python').match(pkg.name)]

for pkg in [pkg for pkg in pkgs if pkg.current_state == apt_pkg.CURSTATE_INSTALLED]:
    print(pkg.name)
