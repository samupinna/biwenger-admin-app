[app]

# (str) Título de tu aplicación
title = Biwenger Liga Manager

# (str) Nombre del paquete
package.name = biwengerliga

# (str) Dominio del paquete (necesario para Android/iOS)
package.domain = com.biwenger.liga

# (str) Archivo fuente principal de tu aplicación
source.main = main.py

# (list) Directorios fuente (donde están los archivos .py)
source.dir = .

# (list) Patrones de archivos para incluir
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Versión de la aplicación
version = 1.0

# (list) Requisitos de la aplicación
requirements = python3,kivy,plyer,requests,certifi

# (str) Icono de la aplicación
#icon.filename = assets/icon.png

# (str) Imagen de inicio
#presplash.filename = assets/presplash.png

[buildozer]

# (int) Nivel de log (0 = error, 1 = info, 2 = debug)
log_level = 2

# (int) Mostrar advertencias (0 = no, 1 = sí)
warn_on_root = 1

[android]

# (str) Título de la actividad principal
android.activity_class_name = org.kivy.android.PythonActivity

# (str) Nombre del servicio principal
android.service_main = main

# (str) Archivo de configuración de permisos
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Tema de Android
android.theme = "@android:style/Theme.NoTitleBar"

# (list) APIs de Android para usar
android.api = 33

# (int) Versión mínima de SDK
android.minapi = 21

# (str) NDK a usar
android.ndk = 25b

# (bool) Usar SDK privado
android.private_storage = True

# (str) Directorio donde se almacenan los archivos
android.storage_dir = /storage/emulated/0/BiwengerLiga

# (bool) Permitir backup
android.allow_backup = True

# (str) Orientación
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (str) Modo de presentación
android.presplash_color = #FFFFFF

[ios]

# (str) Título de la aplicación iOS
ios.title = Biwenger Liga Manager

# (str) Bundle ID
ios.bundle_id = com.biwenger.liga

# (str) Versión de iOS mínima
ios.deployment_target = 11.0

# (str) Arquitecturas soportadas
ios.archs = arm64, x86_64

# (bool) Codesign
ios.codesign = True
