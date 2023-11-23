import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")
django.setup()

from catalog.models import Producto, Type, Images, Idioma, Moneda

productos_data = [

]

for producto_data in productos_data:
    producto = Producto.objects.create(
        nombre=producto_data["nombre"],
        precio=producto_data["precio"],
        idioma=producto_data["idioma"],
        descripcion=producto_data["descripcion"],
        url=producto_data["url"],
        type=producto_data["type"],
        image=producto_data["image"],
        moneda=producto_data["moneda"]

    )

print("Productos agregados a la base de datos.")
