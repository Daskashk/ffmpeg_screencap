# Importación de módulos necesarios
import subprocess
import os


def check_path(bin):
    """ "Verifica si el binario existe en el PATH del sistema"""
    raw_path = str(os.getenv("PATH"))
    path = raw_path.split(":")
    for dir in path:
        if os.path.exists(dir) and bin in os.listdir(dir):
            return True
    return False


# Función para grabar la pantalla
def grabar_pantalla(
    resolucion,
    framerate,
    archivo_salida,
    audio,
    microfono,
    codec,
    calidad,
    tasa_bits_video,
    tasa_bits_audio,
    tasa_bits_microfono,
    codec_audio,
    codec_microfono,
    server_type,
):
    try:
        # Configuración de grabación
        print("\nConfiguración de grabación:")
        print("---------------------------")
        config = {
            "Resolución": resolucion,
            "Tasa de frames": framerate,
            "Archivo de salida": archivo_salida,
            "Incluir audio": "Sí" if audio else "No",
            "Incluir microfono": "Sí" if microfono else "No",
            "Codec de video": codec,
            "Calidad de video": calidad,
            "Tasa de bits de video": tasa_bits_video,
            "Tasa de bits de audio": tasa_bits_audio,
            "Tasa de bits de microfono": tasa_bits_microfono,
            "Codec de audio": codec_audio,
            "Codec de microfono": codec_microfono,
        }
        for key, value in config.items():
            print(f"{key}: {value}")
        print("---------------------------")
        print("Presione Ctrl+C para detener la grabación...\n")

        # Construcción del comando de grabación
        if server_type == "x11":
            comando = f"ffmpeg -f x11grab -framerate {framerate} -video_size {resolucion} -i :0.0"
        elif server_type == "wayland":
            comando = f"ffmpeg -f wayland -framerate {framerate} -video_size {resolucion} -i wayland"

        if audio or microfono:
            if check_path("pipewire"):
                comando += f" -f pipewire-0 -i default"
            elif check_path("pulseaudio"):
                comando += f" -f pulse -i default"
            else:
                print(
                    "No se detectó servidor de audio. La grabación de audio no está disponible."
                )
                audio = False
                microfono = False

        comando += f" -c:v {codec} -crf {get_crf(calidad)} -b:v {tasa_bits_video}k"
        if audio or microfono:
            comando += f" -c:a {codec_audio} -b:a {tasa_bits_audio}k"
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
    calidad_crf = {"alta": 18, "media": 23, "baja": 28}
    return calidad_crf.get(calidad, 23)


# Función para obtener el servidor de pantalla
def get_server_type():
    # Detección del servidor de pantalla
    server = os.getenv("XDG_SESSION_TYPE")
    if not server:
        return None
    return server


# Función para obtener la resolución de la pantalla
def get_monitor_resolution(server_type):
    # Obtención de la resolución de la pantalla
    if server_type == "x11":
        output = subprocess.check_output(["xrandr", "-q", "-d", ":0"])
        lines = output.decode("utf-8").splitlines()
        for line in lines:
            if "*" in line:
                resolution = line.split()[0]
                return resolution
    elif server_type == "wayland":
        output = subprocess.check_output(["wlr-randr"])
        lines = output.decode("utf-8").splitlines()
        for line in lines:
            if "current" in line:
                resolution = line.split()[0]
                return resolution
    return None


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

    server_type = get_server_type()
    if server_type is None:
        print("No se detectó servidor de pantalla.")
        return

    resolucion = get_monitor_resolution(server_type)

    if opcion == "1":
        # Configuración personalizada
        print("\nConfiguración personalizada:")
        print("---------------------------")
        input_resolucion = input(
            f"Ingrese la resolución de la pantalla ({resolucion}): "
        )
        if input_resolucion:
            resolucion = input_resolucion
        framerate = input("Ingrese la tasa de frames por segundo (60): ")
        if not framerate:
            framerate = 60
        else:
            framerate = int(framerate)
        archivo_salida = input("Ingrese el nombre del archivo de salida (output.mp4): ")
        if not archivo_salida:
            archivo_salida = "output.mp4"
        codec = input("Ingrese el codec de video (libx264): ")
        if not codec:
            codec = "libx264"
        calidad = input("Ingrese la calidad de video (alta): ")
        if not calidad:
            calidad = "alta"
        tasa_bits_video = input("Ingrese la tasa de bits de video (5000): ")
        if not tasa_bits_video:
            tasa_bits_video = 5000
        else:
            tasa_bits_video = int(tasa_bits_video)
        audio = input("¿Incluir audio? (s/n): ").lower()
        while audio not in ["s", "n", ""]:
            audio = input("La opción debe ser s o n. ¿Incluir audio? (s/n): ").lower()
        if audio == "":
            audio = False
        else:
            audio = audio == "s"
        if audio:
            codec_audio = input("Ingrese el codec de audio (aac): ")
            if not codec_audio:
                codec_audio = "aac"
            tasa_bits_audio = input("Ingrese la tasa de bits de audio (256): ")
            if not tasa_bits_audio:
                tasa_bits_audio = 256
            else:
                tasa_bits_audio = int(tasa_bits_audio)
        else:
            codec_audio = "aac"
            tasa_bits_audio = 256
        microfono = input("¿Incluir microfono? (s/n): ").lower()
        while microfono not in ["s", "n", ""]:
            microfono = input(
                "La opción debe ser s o n. ¿Incluir microfono? (s/n): "
            ).lower()
        if microfono == "":
            microfono = False
        else:
            microfono = microfono == "s"
        if microfono:
            codec_microfono = input("Ingrese el codec de microfono (aac): ")
            if not codec_microfono:
                codec_microfono = "aac"
            tasa_bits_microfono = input("Ingrese la tasa de bits de microfono (256): ")
            if not tasa_bits_microfono:
                tasa_bits_microfono = 256
            else:
                tasa_bits_microfono = int(tasa_bits_microfono)
        else:
            codec_microfono = "aac"
            tasa_bits_microfono = 256

    elif opcion == "2":
        # Configuración automática
        print("\nConfiguración automática:")
        print("---------------------------")
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
        microfono = input("¿Incluir microfono? (s/n): ").lower()
        while microfono not in ["s", "n"]:
            microfono = input(
                "La opción debe ser s o n. ¿Incluir microfono? (s/n): "
            ).lower()
        microfono = microfono == "s"
        if microfono:
            codec_microfono = "aac"
            tasa_bits_microfono = 256
        else:
            codec_microfono = "aac"
            tasa_bits_microfono = 256

    elif opcion == "3":
        # Importar configuración desde archivo
        print("\nImportar configuración desde archivo:")
        print("---------------------------")
        filename = input("Ingrese el nombre del archivo de configuración: ")
        config = load_config(filename)
        if config:
            framerate = int(config["Tasa de frames"])
            archivo_salida = config["Archivo de salida"]
            codec = config["Codec de video"]
            calidad = config["Calidad de video"]
            tasa_bits_video = int(config["Tasa de bits de video"])
            audio = config["Incluir audio"] == "Sí"
            codec_audio = config["Codec de audio"]
            tasa_bits_audio = int(config["Tasa de bits de audio"])
            microfono = config["Incluir microfono"] == "Sí"
            codec_microfono = config["Codec de microfono"]
            tasa_bits_microfono = int(config["Tasa de bits de microfono"])
        else:
            print("No se pudo cargar la configuración.")
            return

    else:
        print("Opción inválida. Saliendo...")
        return

    # Guardado de configuración en archivo
    save_config(
        {
            "Resolución": resolucion,
            "Tasa de frames": str(framerate),
            "Archivo de salida": archivo_salida,
            "Incluir audio": "Sí" if audio else "No",
            "Incluir microfono": "Sí" if microfono else "No",
            "Codec de video": codec,
            "Calidad de video": calidad,
            "Tasa de bits de video": str(tasa_bits_video),
            "Tasa de bits de audio": str(tasa_bits_audio),
            "Tasa de bits de microfono": str(tasa_bits_microfono),
            "Codec de audio": codec_audio,
            "Codec de microfono": codec_microfono,
        },
        "config.txt",
    )

    print("\nListo para grabar. Presione Ctrl+C para detener.")
    input("Presione Enter para comenzar la grabación...")

    grabar_pantalla(
        resolucion,
        framerate,
        archivo_salida,
        audio,
        microfono,
        codec,
        calidad,
        tasa_bits_video,
        tasa_bits_audio,
        tasa_bits_microfono,
        codec_audio,
        codec_microfono,
        server_type,
    )


if __name__ == "__main__":
    main()
