import os
import django
import re

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")
django.setup()

# Importa tus modelos
from catalog.models import Producto, Type, Images, Idioma, Moneda

# Función para agregar un producto
def agregar_producto():
    while True:
        print("\nIngrese los detalles del producto. Ejemplo:\n"
              "Nombre Idioma URL\n"
              "Escriba 'SALIR' para finalizar.\n")

        entrada = input()
        if entrada.upper() == 'SALIR':
            break

        # Usar regex para separar los componentes de la entrada
        # Asumiendo que el idioma es una palabra y la URL tiene un formato estándar
        match = re.match(r"(.*?)\s+(\w+)\s+(https?://\S+)", entrada)
        if not match:
            print("Formato de entrada incorrecto. Inténtelo de nuevo.")
            continue

        nombre, idioma, url = match.groups()

        precio = 0  # Fijo, como indicaste

        moneda = input("Moneda (USD/JPY/CLP): ").upper()
        if moneda == 'SALIR':
            break

        # Buscar un producto existente con el mismo nombre para obtener TYPE, SET y COLOR
        producto_existente = Producto.objects.filter(nombre=nombre).first()
        if producto_existente:
            tipo_obj = producto_existente.type
            set_producto = producto_existente.set
            color = producto_existente.color
            imagen_obj = producto_existente.image
        else:
            # Valores por defecto o solicitar al usuario
            tipo_obj = Type.objects.get(type="BOOSTER PACK")
            set_producto = ""
            color = ""
            imagen_obj = None  # o asignar una imagen por defecto

        # Obtener el idioma y moneda desde la base de datos
        idioma_obj = Idioma.objects.get(idioma=idioma.upper())
        moneda_obj = Moneda.objects.get(moneda=moneda)

        # Crear y guardar el producto
        producto = Producto.objects.create(
            nombre=nombre,
            precio=precio,
            idioma=idioma_obj,
            descripcion="",
            url=url,
            type=tipo_obj,
            image=imagen_obj,
            moneda=moneda_obj,
            set=set_producto,
            color=color
        )

        print("Producto agregado a la base de datos.")

# Ejecutar la función para agregar un producto
agregar_producto()
