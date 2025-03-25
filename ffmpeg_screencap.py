# Importación de módulos necesarios
import subprocess
import os

# Función para grabar la pantalla
def grabar_pantalla(resolucion, framerate, archivo_salida, audio, codec, calidad, tasa_bits_video, tasa_bits_audio, codec_audio):
    try:
        # Configuración de grabación
        print("\nConfiguración de grabación:")
        print("---------------------------")
        config = {
            "Resolución": resolucion,
            "Tasa de frames": framerate,
            "Archivo de salida": archivo_salida,
            "Incluir audio": "Sí" if audio else "No",
            "Codec de video": codec,
            "Calidad de video": calidad,
            "Tasa de bits de video": tasa_bits_video,
            "Tasa de bits de audio": tasa_bits_audio,
            "Codec de audio": codec_audio
        }
        for key, value in config.items():
            print(f"{key}: {value}")
        print("---------------------------")
        print("Presione Ctrl+C para detener la grabación...\n")

        # Construcción del comando de grabación
        comando = f"ffmpeg -f x11grab -framerate {framerate} -video_size {resolucion} -i :0.0"
        if audio:
            # Detección del servidor de audio
            if subprocess.run(["which", "pipewire"], stdout=subprocess.DEVNULL).returncode == 0:
                comando += f" -f pipewire-0 -i default"
            elif subprocess.run(["which", "pulseaudio"], stdout=subprocess.DEVNULL).returncode == 0:
                comando += f" -f pulse -i default"
            else:
                print("No se detectó servidor de audio. La grabación de audio no está disponible.")
                audio = False
        if audio:
            comando += f" -c:a {codec_audio} -b:a {tasa_bits_audio}k"
        comando += f" -c:v {codec} -crf {get_crf(calidad)} -b:v {tasa_bits_video}k"
        comando += f" -preset ultrafast -tune zerolatency {archivo_salida}"

        # Ejecución del comando de grabación
        subprocess.run(comando, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar ffmpeg: {e}")
    except KeyboardInterrupt:
        print("\nGrabación detenida por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Función para obtener la calidad de video
def get_crf(calidad):
    # Mapeo de calidad a CRF
    calidad_crf = {
        "alta": 18,
        "media": 23,
        "baja": 28
    }
    return calidad_crf.get(calidad, 23)

# Función para obtener la resolución de la pantalla
def get_monitor_resolution():
    # Obtención de la resolución de la pantalla utilizando xrandr
    output = subprocess.check_output(["xrandr", "-q", "-d", ":0"])
    lines = output.decode("utf-8").splitlines()
    for line in lines:
        if "*" in line:
            resolution = line.split()[0]
            return resolution

# Función para guardar la configuración
def save_config(config, filename):
    # Guardado de la configuración en un archivo
    with open(filename, "w") as f:
        for key, value in config.items():
            f.write(f"{key}: {value}\n")

# Función para cargar la configuración
def load_config(filename):
    # Carga de la configuración desde un archivo
    config = {}
    try:
        with open(filename, "r") as f:
            for line in f.readlines():
                key, value = line.strip().split(": ")
                config[key] = value
        return config
    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")
        return None

# Función principal
def main():
    print("Opciones de configuración:")
    print("---------------------------")
    print("1. Configuración personalizada")
    print("2. Configuración automática (detecta resolución y otros parámetros)")
    print("3. Importar configuración desde archivo")
    print("---------------------------")
    opcion = input("Ingrese su opción: ")

    if opcion == "1":
        # Configuración personalizada
        print("\nConfiguración personalizada:")
        print("---------------------------")
        resolucion = input("Ingrese la resolución de la pantalla (por ejemplo, 1920x1080): ")
        while not resolucion:
            resolucion = input("La resolución no puede estar vacía. Ingrese la resolución de la pantalla (por ejemplo, 1920x1080): ")
        framerate = int(input("Ingrese la tasa de frames por segundo (por ejemplo, 60): "))
        while framerate <= 0:
            framerate = int(input("La tasa de frames debe ser un número positivo. Ingrese la tasa de frames por segundo (por ejemplo, 60): "))
        archivo_salida = input("Ingrese el nombre del archivo de salida (por ejemplo, output.mp4): ")
        while not archivo_salida:
            archivo_salida = input("El nombre del archivo de salida no puede estar vacío. Ingrese el nombre del archivo de salida (por ejemplo, output.mp4): ")
        codec = input("Ingrese el codec de video (por ejemplo, libx264): ")
        while not codec:
            codec = input("El codec de video no puede estar vacío. Ingrese el codec de video (por ejemplo, libx264): ")
        calidad = input("Ingrese la calidad de video (alta, media o baja): ")
        while calidad not in ["alta", "media", "baja"]:
            calidad = input("La calidad de video debe ser alta, media o baja. Ingrese la calidad de video: ")
        tasa_bits_video = int(input("Ingrese la tasa de bits de video (por ejemplo, 5000): "))
        while tasa_bits_video <= 0:
            tasa_bits_video = int(input("La tasa de bits de video debe ser un número positivo. Ingrese la tasa de bits de video (por ejemplo, 5000): "))
        audio = input("¿Incluir audio? (s/n): ").lower()
        while audio not in ["s", "n"]:
            audio = input("La opción debe ser s o n. ¿Incluir audio? (s/n): ").lower()
        audio = audio == "s"
        if audio:
            codec_audio = input("Ingrese el codec de audio (por ejemplo, aac): ")
            while not codec_audio:
                codec_audio = input("El codec de audio no puede estar vacío. Ingrese el codec de audio (por ejemplo, aac): ")
            tasa_bits_audio = int(input("Ingrese la tasa de bits de audio (por ejemplo, 256): "))
            while tasa_bits_audio <= 0:
                tasa_bits_audio = int(input("La tasa de bits de audio debe ser un número positivo. Ingrese la tasa de bits de audio (por ejemplo, 256): "))
        else:
            codec_audio = "aac"
            tasa_bits_audio = 256

    elif opcion == "2":
        # Configuración automática
        print("\nConfiguración automática:")
        print("---------------------------")
        resolucion = get_monitor_resolution()
        framerate = 60
        archivo_salida = "output.mp4"
        codec = "libx264"
        calidad = "alta"
        tasa_bits_video = 5000
        audio = input("¿Incluir audio? (s/n): ").lower()
        while audio not in ["s", "n"]:
            audio = input("La opción debe ser s o n. ¿Incluir audio? (s/n): ").lower()
        audio = audio == "s"
        if audio:
            codec_audio = "aac"
            tasa_bits_audio = 256
        else:
            codec_audio = "aac"
            tasa_bits_audio = 256

    elif opcion == "3":
        # Importar configuración desde archivo
        print("\nImportar configuración desde archivo:")
        print("---------------------------")
        filename = input("Ingrese el nombre del archivo de configuración: ")
        config = load_config(filename)
        if config:
            resolucion = config["Resolución"]
            framerate = int(config["Tasa de frames"])
            archivo_salida = config["Archivo de salida"]
            audio = config["Incluir audio"] == "Sí"
            codec = config["Codec de video"]
            calidad = config["Calidad de video"]
            tasa_bits_video = int(config["Tasa de bits de video"])
            codec_audio = config["Codec de audio"]
            tasa_bits_audio = int(config["Tasa de bits de audio"])
        else:
            print("No se pudo cargar la configuración.")
            return

    else:
        print("Opción inválida. Saliendo...")
        return

    # Guardado de configuración en archivo
    save_config({
        "Resolución": resolucion,
        "Tasa de frames": str(framerate),
        "Archivo de salida": archivo_salida,
        "Incluir audio": "Sí" if audio else "No",
        "Codec de video": codec,
        "Calidad de video": calidad,
        "Tasa de bits de video": str(tasa_bits_video),
        "Tasa de bits de audio": str(tasa_bits_audio),
        "Codec de audio": codec_audio
    }, "config.txt")

    print("\nListo para grabar. Presione Ctrl+C para detener.")
    input("Presione Enter para comenzar la grabación...")

    grabar_pantalla(resolucion, framerate, archivo_salida, audio, codec, calidad, tasa_bits_video, tasa_bits_audio, codec_audio)

if __name__ == "__main__":
    main()
