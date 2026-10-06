[app]
p4a.branch = v2024.01.21
android.ndk = 25b
android.api = 33
title = Ceritaku
package.name = ceritaku
package.domain = org.ceritaku
source.dir = .
source.include_exts = py,json
version = 0.1
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
