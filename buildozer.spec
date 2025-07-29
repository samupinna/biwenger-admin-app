[app]
title = Biwenger Admin App
package.name = biwengeradmin
package.domain = org.biwenger.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
# uncomment below if you want to bundle files
# android.presplash = %(source.dir)s/data/presplash.png
# android.icon = %(source.dir)s/data/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
