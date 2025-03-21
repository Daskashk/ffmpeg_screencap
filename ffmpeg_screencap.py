import subprocess
import os

def grabar_pantalla(resolucion, framerate, archivo_salida, audio, codec, calidad, tasa_bits_video, tasa_bits_audio, codec_audio):
    try:
        print(f"\nConfiguración de grabación:")
        print(f"Resolución: {resolucion}")
        print(f"Tasa de frames: {framerate} FPS")
        print(f"Archivo de salida: {archivo_salida}")
        print(f"Incluir audio: {audio}")
        print(f"Codec de video: {codec}")
        print(f"Calidad de video: {calidad}")
        print(f"Tasa de bits de video: {tasa_bits_video} kbps")
        print(f"Tasa de bits de audio: {tasa_bits_audio} kbps")
        print(f"Codec de audio: {codec_audio}")
        print("\nPresione Ctrl+C para detener la grabación...\n")

        comando = f"ffmpeg -f x11grab -framerate {framerate} -video_size {resolucion} -i :0.0"
        if audio:
            comando += f" -f pulse -i default"
        comando += f" -c:v {codec} -crf {get_crf(calidad)} -b:v {tasa_bits_video}k"
        if audio:
            comando += f" -c:a {codec_audio} -b:a {tasa_bits_audio}k"
        comando += f" -preset ultrafast -tune zerolatency {archivo_salida}"

        subprocess.run(comando, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar ffmpeg: {e}")
    except KeyboardInterrupt:
        print("\nGrabación detenida por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def get_crf(calidad):
    if calidad == "alta":
        return 18
    elif calidad == "media":
        return 23
    elif calidad == "baja":
        return 28
    else:
        return 23

def get_monitor_resolution():
    output = subprocess.check_output(["xrandr", "-q", "-d", ":0"])
    lines = output.decode("utf-8").splitlines()
    for line in lines:
        if "*" in line:
            resolution = line.split()[0]
            return resolution

def main():
    print("Opciones de configuración:")
    print("1. Configuración personalizada")
    print("2. Configuración automática (detecta resolución y otros parámetros)")
    opcion = input("Ingrese su opción: ")

    if opcion == "1":
        resolucion = get_monitor_resolution()
        framerate = input(f"Ingrese la tasa de frames por segundo (valor por defecto: 60): ") or "60"
        while not framerate.isdigit():
            framerate = input(f"La tasa de frames debe ser un número. Ingrese la tasa de frames por segundo (por ejemplo, 60, valor por defecto: 60): ")
        framerate = int(framerate)
        archivo_salida = input(f"Ingrese el nombre del archivo de salida (valor por defecto: output.mp4): ") or "output.mp4"
        while not archivo_salida:
            archivo_salida = input(f"El nombre del archivo de salida no puede estar vacío. Ingrese el nombre del archivo de salida (por ejemplo, output.mp4, valor por defecto: output.mp4): ")
        codec = input(f"Ingrese el codec de video (valor por defecto: libx264): ") or "libx264"
        calidad = input(f"Ingrese la calidad de video (alta, media o baja, valor por defecto: alta): ") or "alta"
        tasa_bits_video = input(f"Ingrese la tasa de bits de video (valor por defecto: 5000): ") or "5000"
        while not tasa_bits_video.isdigit():
            tasa_bits_video = input(f"La tasa de bits de video debe ser un número. Ingrese la tasa de bits de video (por ejemplo, 5000, valor por defecto: 5000): ")
        tasa_bits_video = int(tasa_bits_video)
        audio = input(f"¿Incluir audio? (s/n, valor por defecto: s): ").lower() or "s"
        while audio not in ["s", "n"]:
            audio = input(f"La opción debe ser s o n. ¿Incluir audio? (s/n, valor por defecto: s): ").lower()
        audio = audio == "s"
        if audio:
            codec_audio = input(f"Ingrese el codec de audio (valor por defecto: aac): ") or "aac"
            while codec_audio not in ["aac", "mp3", "opus"]:
                codec_audio = input(f"El codec de audio debe ser aac, mp3 o opus. Ingrese el codec de audio (por ejemplo, aac, valor por defecto: aac): ")
            tasa_bits_audio = input(f"Ingrese la tasa de bits de audio (valor por defecto: 256): ") or "256"
            while not tasa_bits_audio.isdigit():
                tasa_bits_audio = input(f"La tasa de bits de audio debe ser un número. Ingrese la tasa de bits de audio (por ejemplo, 256, valor por defecto: 256): ")
            tasa_bits_audio = int(tasa_bits_audio)
        else:
            codec_audio = "aac"
            tasa_bits_audio = 256

    elif opcion == "2":
        resolucion = get_monitor_resolution()
        framerate = 60
        archivo_salida = "output.mp4"
        codec = "libx264"
        calidad = "alta"
        tasa_bits_video = 5000
        audio = True
        codec_audio = "aac"
        tasa_bits_audio = 256

    else:
        print("Opción inválida. Saliendo...")
        return

    print("\nListo para grabar. Presione Ctrl+C para detener.")
    input("Presione Enter para comenzar la grabación...")

    grabar_pantalla(resolucion, framerate, archivo_salida, audio, codec, calidad, tasa_bits_video, tasa_bits_audio, codec_audio)

if __name__ == "__main__":
    main()
