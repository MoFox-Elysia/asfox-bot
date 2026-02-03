[app]

title = 错题整理软件
package.name = errorquestion
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,txt

version = 1.0

requirements = python3,kivy==2.1.0,pillow==9.5.0,pyjnius==1.4.2,plyer==2.0.0,cython==0.29.28

orientation = portrait
fullscreen = 0

android.ndk = 23.1.7779620
android.minapi = 21
android.api = 28
android.ndk_api = 21

android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.features = android.hardware.camera
android.min_sdk = 21
android.archs = arm64-v8a
android.enable_androidx = False
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]
log_level = 2