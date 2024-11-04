from datetime import date, timedelta
import pathlib

#○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○#
# Funcion que guarda la ruta de la img
#○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○#
def guardar_images(instance, filename):
    fpath = pathlib.Path(filename)
    name = (instance.username).replace(":","")
    #new_fname = str(instance.nombre)
    return f"static/user/img-{instance.username}/{name}{fpath.suffix}"
