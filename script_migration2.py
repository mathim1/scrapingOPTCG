import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")
django.setup()

from catalog.models import Producto, Type, Images, Idioma, Moneda

imagenes = [
    "https://m.media-amazon.com/images/I/81pEhtjSSVL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/91Agw8ffdUL._AC_SL1500_.jpg",
    "https://carduniverse.cl/cdn/shop/files/DoublePackSetVol.3_DP-03_2_600x.png?v=1698620478",
    "https://carduniverse.cl/cdn/shop/files/WingsoftheCaptainpng_600x.png?v=1698620241",
    "https://m.media-amazon.com/images/I/61AZext6huL._AC_.jpg",
    "https://m.media-amazon.com/images/I/61UwkNeROvL._AC_SL1200_.jpg",
    "https://m.media-amazon.com/images/I/61SgFEw2SUL._AC_.jpg",
    "https://m.media-amazon.com/images/I/71qvgIHlPcL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/51G78ZwYgFL._AC_.jpg",
    "https://m.media-amazon.com/images/I/61MdqVLDEdL._AC_SL1309_.jpg"
]
for imagen in imagenes:
    if not Images.objects.filter(image=imagen).exists():
        imagen_obj = Images.objects.create(image=imagen)
        print(f"Imagen {imagen_obj.image} agregada a la base de datos.")
    else:
        print(f"Imagen {imagen} ya existe en la base de datos.")

productos_data = [
    {
        "nombre": "MAZO YAMATO (ST-09)",
        "precio": 17990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-starter-deck-yamato",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "MAZO LUFFY (ST-08)",
        "precio": 17990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-starter-deck-monkey-d-luffy",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "MAZO BIG MOM AMARILLO (ST-07)",
        "precio": 17990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-starter-deck-big-mom",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81UG8MAcmeL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "Kingdoms of Intrigue - Booster Pack (OP-04)",
        "precio": 5000,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-kingdoms-of-intrigue-booster-pack",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81pEhtjSSVL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Kingdoms of Intrigue - Double Pack (DP-01)",
        "precio": 10990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-kingdoms-of-intrigue-double-pack",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81pEhtjSSVL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "Kingdoms of Intrigue - Booster Box (OP-04)",
        "precio": 104990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-kingdoms-of-intrigue-booster-box",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61UwkNeROvL._AC_SL1200_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    ,
    {
        "nombre": "Romance Dawn - Booster Pack (OP-01)",
        "precio": 6000,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-romance-dawn-booster-pack",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/51G78ZwYgFL._AC_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "Paramount War - Booster Pack (OP-02)",
        "precio": 5000,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-paramount-war-booster-pack",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/71qvgIHlPcL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "Pillars of Strength - Booster Pack (OP-03)",
        "precio": 5000,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.guildreams.com/product/one-piece-tcg-pillars-of-strength-booster-pack",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61SgFEw2SUL._AC_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "MAZO ZORO & SANJI (ST-12)",
        "precio": 14990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://elreinodelosduelos.cl/producto/starter-deck-12-zoro-and-sanji-st-12/",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81qcks9pL4L._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    ,
    {
        "nombre": "MAZO LUFFY (ST-08)",
        "precio": 19990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://elreinodelosduelos.cl/producto/starter-deck-8-monkey-d-luffy-st-08/",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    ,
    {
        "nombre": "MAZO YAMATO (ST-09)",
        "precio": 19990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://elreinodelosduelos.cl/producto/starter-deck-9-yamato-st-09/",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Kingdoms of Intrigue - Booster Box (OP-04)",
        "precio": 119990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://elreinodelosduelos.cl/producto/one-piece-card-game-kingdoms-of-intrigue-op-04/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61UwkNeROvL._AC_SL1200_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    ,
    {
        "nombre": "Paramount War - Booster Box (OP-02)",
        "precio": 124990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://elreinodelosduelos.cl/producto/one-piece-card-game-paramount-war-booster-box-op-02/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61MdqVLDEdL._AC_SL1309_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Gift Collection 2023 (GC01)",
        "precio": 39990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://elreinodelosduelos.cl/producto/one-piece-card-game-gift-collection-2023-gc01/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61AZext6huL._AC_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "MAZO ZORO & SANJI (ST-12)",
        "precio": 11990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://carduniverse.cl/collections/one-piece-card-game/products/reserva-starter-deck-zoro-and-sanji-st-12",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81qcks9pL4L._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "MAZO LUFFY (ST-08)",
        "precio": 17990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://carduniverse.cl/collections/one-piece-card-game/products/reserva-starter-deck-monkey-d-luffy-st-08",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "MAZO LUFFY (ST-08)",
        "precio": 17990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://carduniverse.cl/collections/one-piece-card-game/products/reserva-starter-deck-monkey-d-luffy-st-08",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61w12MF71yL._AC_SL1000_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Wings Of The Captain - Booster Box (OP-06)",
        "precio": 95990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://carduniverse.cl/collections/one-piece-card-game/products/reserva-display-wings-of-captain-op-06",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(
            image="https://carduniverse.cl/cdn/shop/files/WingsoftheCaptainpng_600x.png?v=1698620241"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Wings Of The Captain - Double Pack (DP-03)",
        "precio": 10990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://carduniverse.cl/collections/one-piece-card-game/products/reserva-double-pack-set-vol-3-dp03",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(
            image="https://carduniverse.cl/cdn/shop/files/DoublePackSetVol.3_DP-03_2_600x.png?v=1698620478"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "Paramount War - Booster Box (OP-02)",
        "precio": 131990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://carduniverse.cl/collections/one-piece-card-game/products/reserva-display-romance-dawn",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61MdqVLDEdL._AC_SL1309_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "MAZO YAMATO (ST-09)",
        "precio": 18990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.geekers.cl/one-piece-starter-deck-09-yamato",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }, {
        "nombre": "Paramount War - Booster Pack (OP-02)",
        "precio": 5490,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.geekers.cl/one-piece-pillars-of-strength-booster-pack-copiar",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/71qvgIHlPcL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }, {
        "nombre": "Pillars of Strength - Booster Pack (OP-03)",
        "precio": 5490,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.geekers.cl/one-piece-pillars-of-strength-booster-pack",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61SgFEw2SUL._AC_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "MAZO LUFFY (ST-08)",
        "precio": 16990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://thirdimpact.cl/producto/one-piece-card-game-st08-monkey-d-luffy/",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "Wings Of The Captain - Booster Box (OP-06)",
        "precio": 99990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://thirdimpact.cl/producto/one-piece-card-game-op06-wings-of-the-captain-booster-box/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(
            image="https://carduniverse.cl/cdn/shop/files/WingsoftheCaptainpng_600x.png?v=1698620241"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }, {
        "nombre": "Gift Collection 2023 (GC01)",
        "precio": 30990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://thirdimpact.cl/producto/one-piece-card-game-gb01-gift-box-2023/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61AZext6huL._AC_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Kingdoms of Intrigue - Double Pack (DP-01)",
        "precio": 11990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://thirdimpact.cl/producto/one-piece-card-game-kingdom-of-intrigue-dp01-double-pack-vol-1/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81pEhtjSSVL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    },
    {
        "nombre": "Pillars of Strength - Booster Box (OP-03)",
        "precio": 119990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://thirdimpact.cl/producto/one-piece-card-game-op03-pillars-of-strength/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/91Agw8ffdUL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    ,
    {
        "nombre": "Paramount War - Booster Box (OP-02)",
        "precio": 109990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://thirdimpact.cl/producto/one-piece-card-game-op02-paramount-war/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61MdqVLDEdL._AC_SL1309_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    ,
    {
        "nombre": "Kingdoms of Intrigue - Booster Box (OP-04)",
        "precio": 119990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://thirdimpact.cl/producto/one-piece-card-game-op04-kingdoms-of-intrigue-booster-box/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61UwkNeROvL._AC_SL1200_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Pillars Of Strength - Booster Box (OP-03)",
        "precio": 104990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.playset.cl/producto/display-24-sobres-one-piece-tcg-pillars-of-strength-op-03/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/91Agw8ffdUL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Kingdoms of Intrigue - Double Pack (DP-01)",
        "precio": 10990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://www.playset.cl/producto/one-piece-card-game-double-pack-set-vol-1-dp-01/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81pEhtjSSVL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "MAZO LUFFY (ST-08)",
        "precio": 16990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://drawn.cl/producto/preventa-juego-de-cartas-one-piece-st08-monkey-d-luffy/",
        "type": Type.objects.get(type="STARTER DECK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/715t8fd83LL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Gift Collection 2023 (GC01)",
        "precio": 34990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://drawn.cl/producto/one-piece-card-game-gift-collection-2023-gc-01/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61AZext6huL._AC_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    , {
        "nombre": "Kingdoms of Intrigue - Booster Box (OP-04)",
        "precio": 119990,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://drawn.cl/producto/preventa-2-one-piece-op04-kingdoms-of-intrigue-booster-box-preventa/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/61UwkNeROvL._AC_SL1200_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }
    ,
    {
        "nombre": "Kingdoms of Intrigue - Booster Pack (OP-04)",
        "precio": 5490,
        "idioma": Idioma.objects.get(idioma="INGLES"),
        "descripcion": "",
        "url": "https://drawn.cl/producto/booster-pack-op-04-kingdoms-of-intrigue/",
        "type": Type.objects.get(type="BOOSTER PACK"),
        "image": Images.objects.get(image="https://m.media-amazon.com/images/I/81pEhtjSSVL._AC_SL1500_.jpg"),
        "moneda": Moneda.objects.get(moneda="CLP")
    }

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
