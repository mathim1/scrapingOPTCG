import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")
django.setup()

from catalog.models import Producto, Type, Images, Idioma, Moneda

tipos = ["STARTER DECK", "BOOSTER PACK"]
for tipo in tipos:
    tipo_obj, created = Type.objects.get_or_create(type=tipo)
    if created:
        print(f"Tipo {tipo_obj.type} agregado a la base de datos.")
    else:
        print(f"Tipo {tipo_obj.type} ya existe en la base de datos.")

imagenes = [
    "https://m.media-amazon.com/images/I/612Tn48L90L._AC_SL1200_.jpg",
    "https://m.media-amazon.com/images/I/611-iR6cfpL._AC_SL1200_.jpg",
    "https://m.media-amazon.com/images/I/61Ztrh6aFuL._AC_SL1200_.jpg",
    "https://m.media-amazon.com/images/I/71ksCUbPIuL._AC_SL1200_.jpg",
    "https://m.media-amazon.com/images/I/81UG8MAcmeL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg",
    "https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81fNYpxI1pL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81muMg7eGeL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81ZIvaR-uPL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/718n-IGcYdL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81qcks9pL4L._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/91E45IrnyDL._AC_SL1500_.jpg",
]
for imagen in imagenes:
    imagen_obj, created = Images.objects.get_or_create(image=imagen)
    if created:
        print(f"Imagen {imagen_obj.image} agregada a la base de datos.")
    else:
        print(f"Imagen {imagen_obj.image} ya existe en la base de datos.")

idiomas = ["INGLES", "JAPONES"]
for idioma in idiomas:
    idioma_obj, created = Idioma.objects.get_or_create(idioma=idioma)
    if created:
        print(f"Idioma {idioma_obj.idioma} agregado a la base de datos.")
    else:
        print(f"Idioma {idioma_obj.idioma} ya existe en la base de datos.")

monedas = ["USD", "JPY", "CLP"]
for moneda in monedas:
    moneda_obj, created = Moneda.objects.get_or_create(moneda=moneda)
    if created:
        print(f"Tipo {moneda_obj.moneda} agregado a la base de datos.")
    else:
        print(f"Tipo {moneda_obj.moneda} ya existe en la base de datos.")

productos_data = [
    {"nombre": "MAZO SH LUFFY ROJO (ST-01)", "precio": 37.57, "idioma": Idioma.objects.get(idioma="INGLES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/TCG-una-pieza-Sombrero-Starter/dp/B0BNLQ6QX4/ref=sr_1_4?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-4",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/612Tn48L90L._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO KIDD VERDE (ST-02)", "precio": 42.61, "idioma": Idioma.objects.get(idioma="INGLES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/TCG-una-pieza-Baraja-generaci%C3%B3n/dp/B0BNLKF4QT/ref=sr_1_3?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-3",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/611-iR6cfpL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO CROCODILE AZUL (ST-03)", "precio": 40.12, "idioma": Idioma.objects.get(idioma="INGLES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/One-Piece-TCG-Cubierta-Iniciaci%C3%B3n/dp/B0BNLKVHY8/ref=sr_1_7?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-7",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61Ztrh6aFuL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO ONE PIECE RED (ST-05)", "precio": 53.61, "idioma": Idioma.objects.get(idioma="INGLES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-NAMCO-Entertainment-Cubierta-inicio/dp/B0BTKKKRJ7/ref=sr_1_5?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-5",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/71ksCUbPIuL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO BIG MOM AMARILLO (ST-07)", "precio": 32.00, "idioma": Idioma.objects.get(idioma="INGLES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/One-Piece-TCG-Pirates-BCL2677501/dp/B0C7VKY132/ref=sr_1_29?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-29",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81UG8MAcmeL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO LUFFY (ST-08)", "precio": 27.45, "idioma": Idioma.objects.get(idioma="INGLES"), "descripcion": "",
     "url": "https://www.amazon.com/-/es/One-Piece-TCG-Monkey-D-Luffy-Starter/dp/B0C7VFJ8LB/ref=sr_1_6?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-6",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO YAMATO (ST-09)", "precio": 32.43, "idioma": Idioma.objects.get(idioma="INGLES"), "descripcion": "",
     "url": "https://www.amazon.com/-/es/One-Piece-TCG-Cubierta-inicio/dp/B0C7VGHF3J/ref=sr_1_48?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-48",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO SH LUFFY ROJO (ST-01)", "precio": 25.56, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-One-Piece-TCG-Sombrero/dp/B09VKTBKMS/ref=sr_1_19?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-19",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/612Tn48L90L._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO KIDD VERDE (ST-02)", "precio": 24.48, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-One-Piece-TCG-generaci%C3%B3n/dp/B09VKVFQMD/ref=sr_1_45?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-45",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/611-iR6cfpL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO CROCODILE AZUL (ST-03)", "precio": 24.42, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-One-Piece-TCG-Cubierta/dp/B09VKX8N65/ref=sr_1_20?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-20",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61Ztrh6aFuL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO KAIDO (ST-04)", "precio": 27.56, "idioma": Idioma.objects.get(idioma="JAPONES"), "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-Cubierta-iniciaci%C3%B3n-piratas-japon%C3%A9s/dp/B09VKWZJWZ/ref=sr_1_12?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-12",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81fNYpxI1pL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO ONE PIECE RED (ST-05)", "precio": 32.31, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/Bandai-One-Piece-Edici%C3%B3n-pel%C3%ADcula/dp/B09VKS64CD/ref=sr_1_50?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619764&sprefix=one+piece+tc%2Caps%2C198&sr=8-50",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/71ksCUbPIuL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO BIG MOM AMARILLO (ST-07)", "precio": 23.87, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-NAMCO-Entertainment-One-Piece/dp/B0BKKSYCB4/ref=sr_1_16?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-16",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81UG8MAcmeL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO LUFFY (ST-08)", "precio": 22.31, "idioma": Idioma.objects.get(idioma="JAPONES"), "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-Entertainment-Monkey-%E3%80%90ST-8%E3%80%91-Japon%C3%A9s/dp/B0BNPDYVD8/ref=sr_1_58?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-58",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO YAMATO (ST-09)",
     "precio": 21.49,
     "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/One-Piece-TCG-Cubierta-inicio/dp/B0C7VGHF3J/ref=sr_1_48?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2MEAQZU1QT7WL&keywords=One+Piece+TCG&qid=1698619615&sprefix=one+piece+tc%2Caps%2C198&sr=8-48",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO AKAINU (ST-06)", "precio": 3674, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-ST-06-PIECE-Card-Start/dp/B0B588N7NW/ref=sr_1_26?crid=1Z6AZ7CJIOJ7I&keywords=One+Piece+TCG&qid=1698621165&sprefix=one+piece+tcg%2Caps%2C313&sr=8-26",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81muMg7eGeL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

    {"nombre": "MAZO 3 CAPITANES (ST-10)", "precio": 5826, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-ST-10-Ultimate-Captains-Gathering/dp/B0BV136NMY/ref=sr_1_12?crid=1Z6AZ7CJIOJ7I&keywords=One+Piece+TCG&qid=1698621165&sprefix=one+piece+tcg%2Caps%2C313&sr=8-12",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81ZIvaR-uPL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

    {"nombre": "MAZO UTA (ST-11)", "precio": 3992, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-ST-11-PIECE-Card-Start/dp/B0CFX88NSQ/ref=sr_1_10?crid=1Z6AZ7CJIOJ7I&keywords=One+Piece+TCG&qid=1698621165&sprefix=one+piece+tcg%2Caps%2C313&sr=8-10",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/718n-IGcYdL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

    {"nombre": "MAZO ZORO & SANJI (ST-12)", "precio": 4507, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-ST-12-PIECE-Start-Sanji/dp/B0CFWYBXZZ/ref=sr_1_7?crid=1Z6AZ7CJIOJ7I&keywords=One+Piece+TCG&qid=1698621165&sprefix=one+piece+tcg%2Caps%2C313&sr=8-7",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81qcks9pL4L._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

    {"nombre": "FAMILY DECK BOX", "precio": 5620, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-PIECE-Card-Game-Family/dp/B0BV13PTNF/ref=sr_1_16?crid=1Z6AZ7CJIOJ7I&keywords=One+Piece+TCG&qid=1698621165&sprefix=one+piece+tcg%2Caps%2C313&sr=8-16",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/91E45IrnyDL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

    {"nombre": "MAZO YAMATO (ST-09)", "precio": 0, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/BANDAI-Entertainment-Cartas-Cubierta-Japon%C3%A9s/dp/B0BNPFQV8J/ref=sr_1_50?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=one+piece+tcg&qid=1699303854&sr=8-50",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO ONE PIECE RED (ST-05)", "precio": 0, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.com/-/es/Bandai-One-Piece-Edici%C3%B3n-pel%C3%ADcula/dp/B09VKS64CD/ref=sr_1_59?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=one+piece+tcg&qid=1699303854&sr=8-59",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/71ksCUbPIuL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="USD")},

    {"nombre": "MAZO CROCODILE AZUL (ST-03)", "precio": 0, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-ST-03-PIECE-Start-Nanabuumi/dp/B09VKX8N65/ref=sr_1_47?crid=3NE2ILLSLWGU8&keywords=one+piece+tcg&qid=1699304092&sprefix=%2Caps%2C565&sr=8-47",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61Ztrh6aFuL._AC_SL1200_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

    {"nombre": "MAZO LUFFY (ST-08)", "precio": 0, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-ST-8-PIECE-Start-Monkey/dp/B0BNPDYVD8/ref=sr_1_7?crid=28HEMNG197NVP&keywords=one+piece+tcg+Start+Deck&qid=1699304167&sprefix=one+piece+tcg+start+deck%2Caps%2C258&sr=8-7",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

    {"nombre": "MAZO BIG MOM AMARILLO (ST-07)", "precio": 0, "idioma": Idioma.objects.get(idioma="JAPONES"),
     "descripcion": "",
     "url": "https://www.amazon.co.jp/-/en/BANDAI-ST-07-Piece-Start-Pirates/dp/B0BKKSYCB4/ref=sr_1_2?crid=28HEMNG197NVP&keywords=one+piece+tcg+Start+Deck&qid=1699304167&sprefix=one+piece+tcg+start+deck%2Caps%2C258&sr=8-2",
     "type": Type.objects.get(type="STARTER DECK"),
     "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81UG8MAcmeL._AC_SL1500_.jpg"),
     "moneda": Moneda.objects.get(moneda="JPY")},

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
