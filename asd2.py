from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from urllib.parse import unquote
import time
import threading
import re  # Importando re para usar expresiones regulares


def extraer_cartas_desde_url_selenium(url, semaphore):
    with semaphore:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get(url)
        time.sleep(10)

        try:
            textarea = driver.find_element(By.TAG_NAME, 'textarea')
            texto_decodificado = unquote(textarea.text)
            cartas = eval(texto_decodificado)
            return cartas
        except Exception as e:
            print(f"Error al obtener datos de {url}: {e}")
            return []
        finally:
            driver.quit()


def extraer_cartas_en_thread(url, resultados, semaphore):
    cartas = extraer_cartas_desde_url_selenium(url, semaphore)
    resultados[url] = cartas


def clasificar_cartas(cartas):
    clasificacion = Counter()
    for carta in cartas:
        set_code = re.match(r'(.*?)-', carta)
        if set_code:
            clasificacion[set_code.group(1)] += 1
    return clasificacion


def calcular_porcentajes(clasificacion):
    total_cartas = sum(clasificacion.values())
    porcentajes = {set: (count / total_cartas) * 100 for set, count in clasificacion.items()}
    return porcentajes


urls = [
    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=11/19/2023&cn=Japan&au=Team%20Sanmaido&pl=1s%20Place&tn=3on3&hs=Corgi%20CS(60)&dg=1nOP05-098a4nOP03-112a4nOP03-113a4nOP03-116a4nOP03-123a4nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-105a4nP-042a4nOP05-102a4nOP03-121a2nOP05-115&cs=192",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/18/2023&cn=Japan&au=Pascal&pl=1st%20Place&tn=Prelims%20Round%202&hs=CS%20Aichi%20Area(500+)&dg=1nOP03-099a3nOP03-110a4nOP03-112a4nOP03-113a4nOP03-115a2nOP03-123a4nOP03-114a3nST07-010a4nOP04-100a4nOP04-104a4nP-042a2nOP05-102a4nOP05-105a4nOP05-114a4nOP05-115&cs=219",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/12/2023&cn=Japan&au=RPK_vg&pl=1st%20Place&tn=SB(11-0)&hs=Asu%20CS&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-115a2nOP03-123a4nOP03-114a4nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a4nOP05-102a4nOP05-105a4nOP03-121a4nOP05-115&cs=191",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/12/2023&cn=Japan&au=Baymax&pl=1st%20Place&tn=2on2&hs=Game_R_Zz&dg=1nOP03-099a4nOP03-112a4nOP03-113a2nOP03-123a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a4nP-042a4nOP05-105a4nOP03-121a4nOP05-115&cs=187",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/12/2023&cn=Japan&au=Danmatsu&pl=1st%20Place&tn=SB&hs=Girafull(49)&dg=1nOP03-099a4nOP03-108a4nOP03-112a4nOP03-113a4nOP03-116a4nOP03-114a4nOP04-100a4nOP04-104a4nOP04-105a4nP-042a4nOP04-099a4nOP05-105a4nOP05-114a2nOP05-115&cs=190",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=11/12/2023&cn=Japan&au=Junsaki&pl=1st%20Place&tn=SB&hs=gull_kesennuma&dg=1nOP05-098a4nOP03-102a4nOP03-112a4nOP03-116a3nOP03-123a4nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nP-042a4nOP05-102a4nOP03-121a2nOP05-114a2nOP05-115a3nOP05-116&cs=198",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/11/2023&cn=Japan&au=Chichan&pl=1st%20Place&tn=SB(4-0)&hs=Arashi%20Takamatsu(34)&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-115a2nOP03-116a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a2nOP04-112a4nOP04-104a4nOP04-105a4nOP05-102a4nOP03-121a2nOP05-115&cs=216",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Black%20Bigmom&date=11/10/2023&cn=Japan&au=Rosward&pl=1st%20Place&tn=SB&hs=FammyFukisima(9)&dg=1nOP03-077a4nOP03-114a4nOP04-100a4nOP04-104a4nOP05-102a4nST08-004a4nOP02-106a4nOP02-114a4nOP02-096a4nOP02-099a4nOP05-081a2nOP05-093a4nST06-015a4nOP02-117&cs=200",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/8/2023&cn=Japan&au=Uma&pl=1st%20Place&tn=Flagship&hs=PAO(62)&dg=1nOP03-099a4nOP03-102a4nOP03-112a4nOP03-113a3nOP03-116a2nOP03-123a4nOP03-114a2nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a3nOP05-100a4nOP05-102a4nOP05-105a2nOP03-121a2nOP05-115&cs=211",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=11/5/2023&cn=Philippines&au=Yoshiharu%20Higashi&pl=1st%20Place&tn=3on3&hs=Aqua%202023%20CS%20Prelims(243)&dg=1nOP05-098a4nOP03-102a4nOP03-112a4nOP03-116a4nOP03-123a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nOP04-107a4nOP05-100a4nOP05-102a4nOP03-121a2nST09-014a2nOP05-115&cs=230",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/5/2023&cn=Japan&au=Uma&pl=1st%20Place&tn=SB&hs=Cardshop&dg=1nOP03-099a4nOP03-102a4nOP03-112a4nOP03-113a1nOP03-115a3nOP03-116a3nOP03-123a4nOP03-114a2nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a2nOP05-100a4nOP05-102a4nOP05-105a3nOP03-121&cs=206",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/5/2023&cn=Japan&au=Uma&pl=1st%20Place&tn=SB&hs=Cardshop&dg=1nOP03-099a4nOP03-102a4nOP03-112a4nOP03-113a1nOP03-115a3nOP03-116a3nOP03-123a4nOP03-114a2nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a2nOP05-100a4nOP05-102a4nOP05-105a3nOP03-121&cs=206",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/4/2023&cn=Japan&au=Axela&pl=1st%20Place&tn=3on3&hs=Corgi%20Earl%20CS(60)&dg=1nOP03-099a4nOP03-102a4nOP03-112a4nOP03-113a2nOP03-115a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a4nOP04-114a4nOP04-104a4nOP04-105a4nP-042a4nOP03-121&cs=194",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/3/2023&cn=Japan&au=Foxzuki&pl=1st%20Place&tn=Flagship&hs=Tsutaya(21)&dg=1nOP03-099a4nOP03-102a4nOP03-112a4nOP03-113a2nOP03-115a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a4nOP04-104a2nOP04-105a4nP-042a4nOP05-102a2nOP05-105a4nOP03-121&cs=205",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=11/3/2023&cn=Japan&au=Rin&pl=1st%20Place&tn=SB&hs=Tsutaya(27)&dg=1nOP03-099a2nOP03-102a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a4nP-042a4nOP05-102a4nOP03-121&cs=184",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri(win%20Kata,%202xPluffy,%20Saka,%20RP%20Luffy)&date=10/29/2023&cn=Japan&au=Amu&pl=1st%20Place&tn=Flagship(5-0)&hs=Ichinomiya&dg=1nOP03-099a3nOP03-108a4nOP03-112a3nOP03-113a4nOP03-115a4nOP03-116a3nOP03-123a4nOP03-114a3nST07-010a3nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a3nOP05-102a4nOP03-121&cs=244",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=10/28/2023&cn=Japan&au=Joker&pl=2nd%20Place&tn=CS%203on3&hs=Bandai(500+)&dg=1nOP03-099a4nOP03-102a4nOP03-112a4nOP03-113a2nOP03-115a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a4nOP04-104a2nOP04-105a4nP-042a4nOP05-102a2nOP05-105a4nOP03-121&cs=203",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=10/15/2023&cn=Singapore&au=Jasmond%20Lim&pl=Top-16&tn=SG%20CS%20Qualifier(7-1-1)&hs=Dimension%20Gaming(400+)&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-116a3nOP03-123a4nOP03-114a2nST07-010a3nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a4nOP05-102a2nOP05-105a4nOP03-121&cs=238",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=10/15/2023&cn=Japan&au=Sugi&pl=1st%20Place&tn=Flagship&hs=Cross%20Store&dg=1nOP05-098a2nOP03-116a3nOP03-123a3nST07-010a3nST07-007a4nOP04-100a4nOP04-112a3nOP04-104a1nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a2nOP03-121a3nOP05-114&cs=223",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=10/15/2023&cn=Japan&au=Torako&pl=1st%20Place&tn=Flagship&hs=ds_akiba(32)&dg=1nOP05-098a3nOP03-116a4nOP03-123a3nST07-010a4nST07-007a4nOP04-100a4nOP04-112a1nOP05-100a4nOP05-101a4nOP05-102a4nOP05-105a4nOP05-106a4nOP05-110a4nOP03-121a3nOP05-114&cs=204",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=10/15/2023&cn=Japan&au=Eliodas&pl=1st%20Place&tn=Flagship&hs=fc_tenjin&dg=1nOP05-098a4nOP03-112a4nOP03-113a4nOP03-116a4nOP03-123a4nST07-010a4nST07-007a4nOP04-100a4nOP04-112a2nOP04-104a4nOP04-105a4nOP05-102a4nOP05-105a4nOP03-121&cs=191",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel%20(win%202Enel,%202kata,%20P%20Luffy,%20saka%20)&date=10/15/2023&cn=Japan&au=Jujiro&pl=1st%20Place&tn=Flagship(5-0)&hs=Kabukicho&dg=1nOP05-098a3nOP03-116a4nOP03-123a2nST07-010a3nST07-007a4nOP04-100a4nOP04-112a2nOP05-100a4nOP05-101a3nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a3nOP03-121a4nOP05-114&cs=252",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel%20(lost%202x%20Law)&date=10/14/2023&cn=Singapore&au=Zed(SG)&pl=Top-8&tn=SG%20CS%20Qualifier(8-2)&hs=Dimension%20Gaming(441)&dg=1nOP05-098a1nOP03-108a2nOP03-116a4nOP03-123a2nST07-010a2nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nOP04-105a3nOP05-100a4nOP05-101a4nOP05-102a4nOP05-105a4nOP05-110a4nOP03-121a2nOP05-114&cs=262",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel(win%20P%20Luffy,%20Saka,%20Kata,%20Nami,%20lost%20to%20Enel)&date=10/14/2023&cn=Japan&au=Uni&pl=1st%20Place&tn=SB(7-1)&hs=Makaiou%20Cup(30)&dg=1nOP05-098a2nOP03-116a4nOP03-123a1nST07-010a1nST07-003a4nST07-007a4nOP04-100a4nOP04-112a2nOP05-100a4nOP05-101a3nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP03-121a3nOP05-114&cs=270",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=10/14/2023&cn=Japan&au=Aire&pl=1st%20Place&tn=3on3&hs=Manji%20CS(130+)&dg=1nOP05-098a2nOP03-108a4nOP03-112a2nOP03-115a4nOP03-116a4nOP03-123a2nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a4nOP04-105a2nOP04-107a2nOP05-100a4nOP03-121a4nOP05-114&cs=211",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel(win%20Uta,%20Enel,%20Kata,%202x%20P%20Luffy)&date=10/9/2023&cn=Japan&au=SaikyoOp&pl=1st%20Place&tn=Flagship(5-0)&hs=Cardshop(25)&dg=1nOP05-098a2nOP03-116a4nOP03-123a2nST07-010a4nST07-007a4nOP04-100a4nOP04-112a2nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a2nOP03-121a4nOP05-114&cs=255",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Black%20Yellow%20Bigmon(2x%20Enel,%20blue%20Doffy,%20blue%20Croco)&date=10/8/2023&cn=Philippines&au=Jensen%20ignacio&pl=1st%20Place&tn=SB(4-0)&hs=Madcap%20Gaming(16)&dg=1nOP03-077a1nOP03-116a3nOP03-123a4nOP03-114a4nOP04-100a3nOP04-112a4nOP04-104a3nOP05-102a4nST06-006a4nOP02-114a2nOP02-096a4nOP03-088a4nOP04-083a4nOP05-081a4nOP05-088a2nOP03-121&cs=274",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=10/7/2023&cn=Japan&au=Kota&pl=2nd%20Place&tn=Junior%20Cup&hs=Bandai(100+)&dg=1nOP05-098a2nOP03-107a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-116a2nOP03-123a4nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a4nOP04-105a2nOP05-100a4nOP05-102&cs=204",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=10/7/2023&cn=Japan&au=Zako&pl=1st%20Place&tn=SB&hs=Card%20Mountain&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-116a4nOP03-123a4nOP03-114a2nST07-010a4nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a4nOP05-102a4nOP03-121&cs=190",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=10/7/2023&cn=Japan&au=Maeda&pl=1st%20Place&tn=3on3&hs=sippohai(120)&dg=1nOP05-098a1nOP03-116a4nOP03-123a3nST07-010a4nST07-007a4nOP04-100a4nOP04-112a1nOP05-100a4nOP05-101a4nOP05-102a3nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a2nOP05-113a4nOP03-121&cs=211",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel(win%202x%20P%20Luffy%20,RP%20Law,%20RG%20law,%20Enel,%20lost%20to%20P%20Luffy)&date=10/7/2023&cn=Indonesia&au=Audityo&pl=1st%20Place&tn=Flagship(7-1)&hs=Nexus%20Tabletop&dg=1nOP05-098a4nOP03-123a2nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nOP05-100a4nOP05-101a3nOP05-102a4nOP05-105a4nOP05-106a4nOP05-110a4nOP03-121a3nOP05-114&cs=271",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri(win%202x%20P%20Luffy,%20Kata,%20Saka)&date=10/6/2023&cn=Malaysia&au=AhLin&pl=1st%20Place&tn=SB(4-0)&hs=Apex%20Bladers(22)&dg=1nOP03-099a4nOP03-108a4nOP03-110a2nOP03-112a4nOP03-115a4nOP03-116a4nST07-010a4nST07-007a4nOP04-100a4nOP04-104a4nOP05-101a4nOP05-105a4nOP05-110a4nOP03-121&cs=230",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=10/2/2023&cn=Japan&au=Pokke&pl=1st%20Place&tn=SB&hs=5cardsakado&dg=1nOP05-098a4nOP03-123a4nST07-007a4nOP04-112a4nOP04-104a4nOP05-100a4nOP05-101a4nOP05-102a3nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-113a3nOP05-114&cs=185",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=10/1/2023&cn=Japan&au=Coco&pl=1st%20Place&tn=3on3&hs=Asu%20CS(159)&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-116a2nOP03-123a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a4nOP05-102a4nOP05-105a4nOP03-121&cs=190",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/30/2023&cn=Japan&au=Nuo&pl=1st%20Place&tn=2on2&hs=Tenryu%20Cup&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-116a3nOP03-123a4nOP03-114a3nST07-010a4nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a4nOP05-102a4nOP05-105a4nOP03-121&cs=188",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel%20(win%20Sakazuki,%203x%20Katakuri%20and%20P%20Luffy)&date=9/30/2023&cn=Japan&au=Kento&pl=2nd%20Place&tn=2on2(6-0)&hs=Tenryu%20Cup&dg=1nOP05-098a4nOP03-123a1nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a3nOP05-100a4nOP05-101a3nOP05-102a4nOP05-105a4nOP05-106a4nOP05-110a4nOP03-121a3nOP05-114&cs=242",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri%20(win%202x%20BlueBlack%20Sakazuki,%20Katakuri,%20Green%20Purple%20Doffy)%20&date=9/29/2023&cn=Indonesia&au=pikapaw&pl=1st%20Place&tn=TB(4-0)&hs=TwoStompas(12)&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-116a2nOP03-123a4nOP03-114a4nST07-010a4nST07-007a4nOP04-100a4nOP04-104a4nOP04-105a4nOP05-102a4nOP03-121&cs=262",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/26/2023&cn=Japan&au=Nia&pl=1st%20Place&tn=Store%20Prelims&hs=Cardbox(32)&dg=1nOP05-098a4nOP03-123a4nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-113a4nOP05-114&cs=194",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/25/2023&cn=Vietnam&au=Vu%20Nguyen&pl=1st%20Place&tn=SB&hs=GrandLind(26)&dg=1nOP03-099a3nOP03-108a4nOP03-112a3nOP03-113a4nOP03-115a3nOP03-116a1nOP03-123a4nOP03-114a3nST07-007a4nOP04-100a4nOP04-104a4nOP05-101a3nOP05-105a4nOP05-110a3nOP03-121a2nOP05-115&cs=219",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/25/2023&cn=Japan&au=Baymax&pl=1st%20Place&tn=SB(7-0)&hs=Tenryu%20Cup&dg=1nOP05-098a4nOP03-123a3nST07-010a4nST07-007a4nOP04-100a4nOP04-112a1nOP05-100a4nOP05-101a4nOP05-102a3nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-113a3nOP05-114&cs=201",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/24/2023&cn=Indonesia&au=Tedi%20Wijaya&pl=1st%20Place&tn=Flagship&hs=Pontianak&dg=1nOP05-098a4nOP03-123a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nP-042a4nOP04-099a4nOP05-101a4nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP03-121&cs=196",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/17/2023&cn=Singapore&au=SKYE&pl=Top-2&tn=Flagship(4-x)&hs=HappyLand&dg=1nOP05-098a4nOP03-115a4nOP03-116a4nOP03-123a4nOP04-100a4nOP04-112a4nOP04-104a4nOP04-099a3nOP05-100a4nOP05-101a4nOP05-102a4nOP05-105a4nOP05-110a3nOP05-114&cs=193",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/17/2023&cn=Singapore&au=Farhan&pl=1st%20Place&tn=SB&hs=Newtro%20Gaming%20Studios(14)&dg=1nOP05-098a4nOP03-108a2nOP03-116a3nOP03-123a2nST07-010a4nOP04-100a3nOP04-112a4nOP04-104a2nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-110a4nOP03-121a4nOP05-114&cs=226",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/17/2023&cn=Japan&au=Aru&pl=1st%20Place&tn=SB&hs=Card%20Mountain&dg=1nOP03-099a4nOP03-108a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-116a2nOP03-123a4nOP03-114a4nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a4nOP05-102a4nOP03-121&cs=189",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/16/2023&cn=Philippines&au=Kurt%20Ramirez&pl=1st%20Place&tn=SB&hs=Madcap%20Gaming(12)&dg=1nOP05-098a2nOP03-116a2nOP03-123a2nST07-010a4nOP04-100a4nOP04-112a4nOP04-104a3nOP04-107a4nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a3nOP05-114&cs=226",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/16/2023&cn=Malaysia&au=Jung&pl=1st%20Place&tn=Flagship&hs=Buddy%20Connection&dg=1nOP05-098a2nOP03-116a4nOP03-123a2nST07-010a4nOP04-100a4nOP04-112a4nOP04-104a2nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-114a2nOP05-115&cs=220",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/16/2023&cn=Japan&au=Harusan&pl=1st%20Place&tn=Store%20Prelims(5-0)&hs=Book%20Ace&dg=1nOP05-098a4nOP03-112a4nOP03-113a2nOP03-115a4nOP03-116a4nOP03-123a2nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a4nOP04-105a2nOP05-100a4nOP05-102a4nOP05-114&cs=211",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/16/2023&cn=Japan&au=NA&pl=1st%20Place&tn=3on3&hs=ds_ikebukuro(108)&dg=1nOP05-098a4nOP03-116a4nOP03-123a2nST07-010a3nST07-007a4nOP04-100a4nOP04-112a2nOP05-100a4nOP05-101a3nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a2nOP03-121a4nOP05-114&cs=212",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/16/2023&cn=Japan&au=Tanke&pl=3rd%20Place&tn=3on3(7-1)&hs=ds_ikebukuro(108)&dg=1nOP05-098a4nOP03-123a2nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-114&cs=209",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/15/2023&cn=Malaysia&au=Be%20Tein%20Chan&pl=1st%20Place&tn=Flagship&hs=Yume%20Hobby%20Station&dg=1nOP03-099a2nOP03-102a2nOP03-107a4nOP03-112a4nOP03-116a3nOP03-123a4nOP03-114a3nST07-010a4nST07-007a4nOP04-100a4nOP04-104a2nOP04-105a2nOP04-107a3nOP05-102a4nOP05-105a3nOP03-121a2nOP05-115&cs=245",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/15/2023&cn=Japan&au=Ritan&pl=1st%20Place&tn=Store%20Prelims&hs=Card_secret&dg=1nOP05-098a4nOP03-123a4nST07-010a4nOP04-100a4nOP04-112a4nOP04-104a2nOP05-100a4nOP05-101a4nOP05-102a3nOP05-104a4nOP05-105a3nOP05-106a4nOP05-110a4nOP05-114a2nOP05-115&cs=207",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/14/2023&cn=Japan&au=Juza&pl=1st%20Place&tn=SB&hs=Girafull(13)&dg=1nOP05-098a3nOP03-108a2nOP03-115a3nOP03-123a3nST07-010a3nST07-007a4nOP04-100a4nOP04-112a3nOP04-104a2nOP04-105a4nOP04-099a2nOP05-100a4nOP05-102a4nOP05-105a3nOP03-121a4nST07-015a2nST09-014&cs=218",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/12/2023&cn=Japan&au=Sakanoko&pl=1st%20Place&tn=SB&hs=CK_Mizonokuchi&dg=1nOP05-098a4nOP03-116a4nOP03-123a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a4nOP05-100a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP03-121a4nOP05-114&cs=191",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/11/2023&cn=Singapore&au=Jeremy&pl=1st%20Place&tn=Flagship(5-0)&hs=Duellers%20Point&dg=1nOP05-098a4nOP03-108a4nOP03-116a4nOP03-123a2nST07-010a4nOP04-100a4nOP04-112a4nOP04-104a4nP-042a4nOP04-099a4nOP05-100a4nOP05-102a4nOP05-105a4nOP03-121&cs=201",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/11/2023&cn=Japan&au=Hane&pl=1st%20Place&tn=SB(7-0)&hs=Tenryu%20Cup&dg=1nOP05-098a2nOP03-116a4nOP03-123a2nST07-010a2nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-114&cs=210",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/10/2023&cn=Japan&au=Mumumu&pl=1st%20Place&tn=SB&hs=Card%20Mountain&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-115a2nOP03-123a4nOP03-114a4nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a4nOP04-107a4nP-042a4nOP05-102a4nOP03-121&cs=189",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/10/2023&cn=Japan&au=Niru&pl=1st%20Place&tn=SB&hs=Card%20Mountain(16)&dg=1nOP05-098a3nOP03-112a4nOP03-115a4nOP03-116a4nOP03-123a2nST07-010a4nST07-007a4nOP04-100a4nOP04-112a3nOP04-114a3nOP04-104a2nOP04-107a3nOP05-100a2nOP05-102a4nOP03-121a4nOP05-114&cs=212",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/10/2023&cn=Japan&au=Bikzo&pl=1st%20Place&tn=Flagship(5-0)&hs=Cardshop(64)&dg=1nOP05-098a4nOP03-123a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a3nOP04-107a2nOP05-100a4nOP05-101a4nOP05-102a1nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-114&cs=208",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/10/2023&cn=Japan&au=Uni&pl=1st%20Place&tn=Store%20Prelims&hs=Cardstrike(24)&dg=1nOP05-098a2nOP03-116a4nOP03-123a2nST07-010a4nOP04-100a4nOP04-112a4nOP04-104a2nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a2nOP03-121a4nOP05-114&cs=219",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/9/2023&cn=Japan&au=Tsushi&pl=1st%20Place&tn=3on3&hs=Aoteru(108)&dg=1nOP03-099a4nOP03-112a4nOP03-113a4nOP03-115a3nOP03-116a3nOP03-123a4nOP03-114a3nST07-010a4nOP04-100a4nOP04-114a4nOP04-104a4nOP04-105a2nP-042a4nOP03-121a3nOP05-115&cs=200",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/9/2023&cn=Japan&au=Harumi&pl=1st%20Place&tn=Flagship(6-0)&hs=Cardshop&dg=1nOP05-098a4nOP03-112a4nOP03-115a4nOP03-116a4nOP03-123a2nST07-010a4nST07-007a4nOP04-100a4nOP04-112a4nOP04-114a2nOP04-104a3nOP04-107a3nOP05-100a4nOP03-121a4nOP05-114&cs=205",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/8/2023&cn=Malaysia&au=Troy&pl=1st%20Place&tn=SB&hs=Vincents%20Card(14)&dg=1nOP05-098a2nOP03-123a4nOP04-100a4nOP04-112a4nOP04-104a3nOP05-100a4nOP05-101a4nOP05-102a4nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a3nST09-014a3nOP05-114a3nOP05-115&cs=204",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/4/2023&cn=Japan&au=Tan&pl=1st%20Place&tn=Store%20Prelims&hs=Giraffull(25)&dg=1nOP05-098a4nOP03-108a4nOP03-112a2nOP03-115a2nOP03-123a3nST07-010a3nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nOP04-105a2nOP05-100a4nOP05-102a4nOP05-105a4nST07-015a2nOP05-114a2nOP05-115&cs=229",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/3/2023&cn=Japan&au=DK&pl=1st%20Place&tn=Flagship(5-0)&hs=Kichijoji&dg=1nOP03-099a4nOP03-112a4nOP03-113a3nOP03-116a3nOP03-123a4nOP03-114a3nST07-010a4nOP04-100a2nOP04-114a4nOP04-104a4nOP04-105a3nOP04-107a4nP-042a4nOP05-105a4nOP03-121&cs=203",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/2/2023&cn=Malaysia&au=Quan%20Ying&pl=1st%20Place&tn=Flagship&hs=Vincent%20Cards(30)&dg=1nOP05-098a4nOP03-112a4nOP03-113a3nOP03-115a3nOP03-116a3nOP03-123a3nST07-010a4nST07-007a4nOP04-100a3nOP04-112a4nOP04-104a4nOP04-105a2nOP05-100a4nOP05-102a4nOP05-114&cs=215",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=9/2/2023&cn=Japan&au=Oreo&pl=1st%20Place&tn=Nagano%20CS&hs=Cardshop&dg=1nOP03-099a4nOP03-112a4nOP03-113a3nOP03-116a2nOP03-123a4nOP03-114a3nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a4nP-042a4nOP05-102a4nOP05-105a4nOP03-121a2nOP05-115&cs=200",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/2/2023&cn=Japan&au=K&pl=2nd%20Place&tn=2on2&hs=Shumai%20Cup(96)&dg=1nOP05-098a1nOP03-102a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-116a3nOP03-123a4nST07-010a3nST07-007a4nOP04-100a4nOP04-112a4nOP04-104a2nOP04-105a3nOP04-107a4nOP05-102a1nOP05-105a1nOP05-114&cs=219",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=9/2/2023&cn=Japan&au=Unagi&pl=1st%20Place&tn=SB(5-0)&hs=Tsutaya&dg=1nOP05-098a4nOP03-123a4nOP04-100a4nOP04-112a4nOP04-104a4nOP04-107a3nOP05-100a4nOP05-101a4nOP05-102a2nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a3nOP05-114a2nOP05-115&cs=197",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=8/30/2023&cn=Malaysia&au=Akira&pl=1st%20Place&tn=SB&hs=Vincents%20Card(14)&dg=1nOP03-099a3nOP03-106a4nOP03-108a3nOP03-110a4nOP03-112a4nOP03-113a2nOP03-115a3nOP03-123a4nOP03-114a2nST07-010a2nST07-007a4nOP04-100a4nOP04-104a3nOP04-105a3nOP04-107a1nOP03-118a4nOP03-121&cs=231",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=8/30/2023&cn=Japan&au=Nyao&pl=1st%20Place&tn=SB&hs=Cardshop&dg=1nOP05-098a4nOP03-108a4nOP03-112a4nOP03-123a4nOP04-112a4nOP04-104a4nOP04-105a4nOP04-107a3nOP05-100a4nOP05-102a4nOP05-105a4nOP05-106a2nOP05-114a3nOP05-115a2nOP05-117&cs=192",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=8/29/2023&cn=Japan&au=Seto&pl=1st%20Place&tn=SB&hs=Shumai%20Cup&dg=1nOP05-098a4nOP03-116a2nOP03-123a4nOP04-100a4nOP04-112a4nOP04-104a4nOP05-100a4nOP05-101a4nOP05-102a4nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a2nOP05-114a2nOP05-115&cs=194",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=8/28/2023&cn=Japan&au=Tokoroten&pl=1st%20Place&tn=SB&hs=Game_R_zz&dg=1nOP05-098a3nOP03-123a4nOP04-100a4nOP04-112a4nOP04-104a4nOP05-100a4nOP05-101a4nOP05-102a4nOP05-104a4nOP05-105a4nOP05-106a4nOP05-110a4nOP05-114a3nOP05-115&cs=187",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Katakuri&date=8/26/2023&cn=Japan&au=wataQ06&pl=1st%20Place&tn=Flagship&hs=Battleroco%20Kawagoe&dg=1nOP03-099a2nOP03-110a4nOP03-112a4nOP03-113a4nOP03-115a1nOP03-123a4nOP03-114a4nST07-010a4nOP04-100a4nOP04-104a4nOP04-105a4nOP04-107a4nP-042a4nOP05-102a3nOP05-115&cs=212",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=8/26/2023&cn=Japan&au=Akaba&pl=1st%20Place&tn=Standard%20Battle&hs=Takoyaki%20CS&dg=1nOP05-098a4nOP03-112a4nOP03-113a4nOP03-115a4nOP03-116a3nOP03-123a4nST07-010a4nOP04-100a4nOP04-112a4nOP04-104a4nOP04-105a4nOP05-105a3nOP03-121a4nST09-014&cs=198",

    "https://onepiecetopdecks.com/deck-list/jp-format-op05-awakening-of-the-new-era/deckgen/?dn=Yellow%20Enel&date=8/26/2023&cn=Japan&au=Poyo&pl=1st%20Place&tn=Standard%20Battle&hs=TCG%20Bar(16)&dg=1nOP05-098a4nOP03-108a3nOP03-123a4nOP04-100a4nOP04-112a4nOP04-104a4nOP05-100a4nOP05-102a4nOP05-104a4nOP05-105a4nOP05-106a2nST09-014a4nOP05-114a3nOP05-115a2nOP05-117&cs=208"

]

resultados = {}
hilos = []
semaphore = threading.Semaphore(5)

# Crear y comenzar los hilos
for url in urls:
    hilo = threading.Thread(target=extraer_cartas_en_thread, args=(url, resultados, semaphore))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos los hilos terminen
for hilo in hilos:
    hilo.join()

clasificacion_global = Counter()
urls_destacadas_con_porcentajes = []

# Procesar los resultados de cada hilo
for url, cartas in resultados.items():
    clasificacion_deck = clasificar_cartas(cartas)
    porcentajes_deck = calcular_porcentajes(clasificacion_deck)

    if porcentajes_deck:
        set_max_porcentaje, max_porcentaje = max(porcentajes_deck.items(), key=lambda x: x[1])
        op05_porcentaje = porcentajes_deck.get("OP05", 0)
        p_porcentaje = porcentajes_deck.get("P", 0)

        if set_max_porcentaje == "OP05" and op05_porcentaje == max_porcentaje and p_porcentaje == 0:
            info_url = f"Porcentajes para el deck de la URL {url}:\n{porcentajes_deck}"
            urls_destacadas_con_porcentajes.append(info_url)
    else:
        print(f"No hay datos de porcentajes para la URL {url}")

    clasificacion_global.update(clasificacion_deck)

# Unir las URL con sus porcentajes usando un salto de línea
resultado_final = "\n\n".join(urls_destacadas_con_porcentajes)

# Calcular y mostrar los porcentajes globales
porcentajes_globales = calcular_porcentajes(clasificacion_global)

print("\nClasificación global de cartas por set:", clasificacion_global)
print("Porcentajes globales de cartas por set:", porcentajes_globales)
print("\nURLs con mayor porcentaje en OP05 y 0% en P:\n", resultado_final)
