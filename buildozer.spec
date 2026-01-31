[app]

# (str) Title of your application
title = 错题整理软件

# (str) Package name
package.name = errorquestion

# (str) Package domain (needed for android/ios packaging)
package.domain = org.errorquestion

# (str) Source files where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,pillow,fpdf2,pyjnius,plyer,cython,pyopenssl

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Android NDK version to use
# android.ndk = 25b

# (str) Android NDK API level to use
android.minapi = 21

# (int) Target Android API, should be as high as possible.
android.api = 33

# (str) NDK API level to build with
android.ndk_api = 21

# (bool) Copy your application's assets to the app's "assets" folder.
# This allows the app to access them at runtime.
#android.copy_extras = Python/kivy/app.py

# (list) Permissions
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Android features
android.features = android.hardware.camera

# (int) Android minimal SDK
android.min_sdk = 21

# (str) Android archs
# 只构建 arm64-v8a 以加快构建速度
android.archs = arm64-v8a

# (bool) Enable AndroidX support.
android.enable_androidx = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android apptheme, is available only when starting as a new project
#android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Patterns to exclude from building
#exclude_patterns = license,images/*,

# (bool) enables Android auto backup feature (Android API 23+)
#android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
