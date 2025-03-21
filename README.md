# ffmpeg_screencap
Este script permite grabar la pantalla de tu computadora de manera fácil e intuitiva utilizando ffmpeg.

* [Requisitos](#requisitos)
* [Uso](#uso)
* [Instalación de ffmpeg](#instalación-de-ffmpeg)
* [Troubleshooting](#troubleshooting)
* [Créditos](#créditos)

## Requisitos
Para utilizar este script, debes:
- Instalar ffmpeg en tu sistema.
- Tener instalado python
- Copiar el archivo ffmpeg_screencap.py en un directorio y hacerlo ejecutable.

## Uso
Para utilizar el script, simplemente ejecuta el comando python ffmpeg_screencap.py en la terminal. El script te pedirá que selecciones algunas opciones de configuración, como la resolución, framerate, archivo de salida, codec, calidad, tasa de bits de video y audio, etc.

Los parámetros por defecto son los siguientes:

  -  Resolución: se obtiene automáticamente la resolución del monitor
  -  Framerate: 60 fps
  -  Archivo de salida: "output.mp4"
  -  Codec: "libx264"
  -  Calidad: "alta"
  -  Tasa de bits de video: 5000 kbps
  -  Audio: True
  -  Codec de audio: "aac"
  -  Tasa de bits de audio: 256 kbps

 Puedes modificar estos parámetros para ajustar la grabación a tus necesidades. Por ejemplo, puedes cambiar la resolución a una resolución específica, como 1080p o 4K, o cambiar el framerate a 30 fps o 120 fps.También te dará una opción para cargar todos los parametros por defecto y saltarse la selección. 

## Instalación de ffmpeg
 Puedes instalar ffmpeg en las siguientes distribuciones utilizando los siguientes comandos como root:

   - Ubuntu/Debian: apt install ffmpeg
   - Fedora/CentOS: dnf install ffmpeg
   - Arch Linux: pacman -S ffmpeg
   - OpenSUSE: zypper install ffmpeg
   - Gentoo: emerge ffmpeg
   - Void Linux: xbps-install -S ffmpeg
   - Slackware: slackpkg install ffmpeg
   - Oracle Linux: yum install ffmpeg    
   - Solus: eopkg install ffmpeg
   - Alpine Linux: apk add ffmpeg
   - FreeBSD: pkg install ffmpeg
   - OpenBSD: pkg_add ffmpeg
   - Mageia: urpmi ffmpeg
   - PCLinuxOS: apt-get install ffmpeg
   - OpenMandriva: `dnf install ffmpeg`

 Para obtener más información sobre ffmpeg, visita su [página web](https://ffmpeg.org/). 
 
 Nota: Asegúrate de que Python esté instalado en tu sistema. La mayoría de las distribuciones de Linux vienen con Python preinstalado, pero si no es así, puedes instalarlo utilizando el gestor de paquetes de tu distribución de la misma forma qu con ffmpeg.

 Si tu distribución no está incluida en la lista, puedes intentar buscar en la documentación de tu distribución o en los foros de soporte para obtener instrucciones específicas para instalar ffmpeg.

 El script te permite configurar la resolución, tasa de frames, codec de video y audio, y más. Puedes seleccionar entre una configuración personalizada o automática.
Parámetros

##Troubleshooting
 Si encuentras algún problema al utilizar el script, aquí te presento algunas soluciones comunes:

 *  Error de instalación de ffmpeg: asegúrate de que ffmpeg esté instalado correctamente en tu sistema. Puedes verificar esto ejecutando el comando ffmpeg -version en la terminal.
 *   Error de ejecución del script: asegúrate de que el script esté ejecutándose con los permisos correctos y que no haya errores de sintaxis en el código.
 *   Problemas de audio o video: asegúrate de que el audio y video estén configurados correctamente en el script. Puedes verificar esto ejecutando el comando ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4 en la terminal.
 *   Mi grabación no tiene audio: asegúrate de que el audio esté habilitado en el script y que el codec de audio esté configurado correctamente.
 *   Mi grabación está distorsionada: asegúrate de que la resolución y framerate estén configurados correctamente en el script.


 Este script fue creado principalmente con la ayuda de Inteligencia Artificial (IA). Utiliza Python como lenguaje de programación y ffmpeg como herramienta de grabación de pantalla. 
 El script fue creado y probado en un sistema Debian 12 con ffmpeg versión 5.1 y Python 3.11. Está pensado para funcionar en x11, por lo q no hay soporte para Wayland, Window ni MacOS por ahora. 
 Este es un script que creé para mi originalmente. No puedo garantizar que funcione en otros entornos. 

## Créditos
Este script utiliza [ffmpeg](https://ffmpeg.org/), una herramienta de código abierto para grabar y procesar video. Muchas gracias a los desarrolladores de ffmpeg por su excelente trabajo.


