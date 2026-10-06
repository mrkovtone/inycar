#!/usr/bin/env python3
"""Сборка мобильных одностраничников «20» и «25».
Данные — из рабочих копий ЛИДМАГНИТ_20_до20К_01.10.md и ЛИДМАГНИТ_25_до25К_03.10.md (состояние на 06.10).
BASE_URL: когда страницы будут выложены, впишите адрес сайта, чтобы og:image стал абсолютным."""
import html, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://mrkovtone.github.io/inycar"  # напр. "https://example.github.io/inycar-leadmagnets"
TG = "https://t.me/inycar_import"
TEL = "tel:88007002315"; TEL_TXT = "8 800 700-23-15"
SITE = "https://inycar.ru"

# (название, год, детали из поста, пробег, цена, платёж клиенту, пост, фото, пометка)
D20 = [
 ("Из ролика про Кугу, Джетту и Кашкай", [
  ("Форд Куга", 2014, "Полный привод, один владелец", "142 009", "920 899", "19 000", 11934, "ford-kuga-2014.jpg", None),
  ("Фольксваген Джетта", 2016, "Два владельца", "141 273", "829 217", "17 000", 11820, "vw-jetta-2016.jpg", None),
  ("Ниссан Кашкай", 2012, "Два владельца", "136 263", "629 100", "13 000", 11862, "nissan-qashqai-2012.jpg", None),
  ("Рено Дастер", 2016, "Полный привод, один владелец", "166 600", "441 246", "9 000", 11985, "renault-duster-2016.jpg", "Та самая четвёртая из ролика"),
 ]),
 ("Из ролика про Ауди, Оптиму и Октавию", [
  ("Ауди A4", 2011, "Автомат, три владельца", "156 780", "870 224", "18 000", 12056, "audi-a4-2011.jpg", None),
  ("Киа Оптима", 2015, "Автомат, один владелец", "100 701", "851 400", "17 000", 11995, "kia-optima-2015.jpg", None),
  ("Шкода Октавия", 2016, "Универсал, автомат, три владельца", "143 337", "791 700", "16 000", 12087, "skoda-octavia-2016.jpg", None),
  ("Равон Нексия", 2017, "Два владельца", "129 235", "393 000", "8 000", 11872, "ravon-nexia-2017.jpg", "Та самая четвёртая из ролика"),
 ]),
 ("Из ролика про Аутлендер, Каптиву и Рио", [
  ("Мицубиси Аутлендер", 2012, "Полный привод, вариатор, три владельца", "151 581", "833 800", "17 000", 12159, "mitsubishi-outlander-2012.jpg", None),
  ("Шевроле Каптива", 2011, "Полный привод, механика, два владельца", "108 762", "632 500", "13 000", 12118, "chevrolet-captiva-2011.jpg", None),
  ("Киа Рио", 2020, "Седан, автомат, один владелец", "107 253", "748 811", "15 000", 12139, "kia-rio-2020.jpg", None),
  ("Лада Гранта", 2019, "Универсал, робот, один владелец", "48 107", "340 600", "6 900", 11645, "lada-granta-2019.jpg", "Та самая четвёртая из ролика"),
 ]),
 ("Из ролика про мотор", [
  ("Хендай Солярис", 2021, "Седан, автомат, один владелец", "11 000", "903 700", "18 000", 11017, "hyundai-solaris-2021.jpg", None),
  ("Хендай Солярис", 2015, "Седан, автомат, один владелец", "170 617", "587 800", "12 000", 11738, "hyundai-solaris-2015.jpg", None),
  ("Киа Рио", 2015, "Хэтчбек, автомат, один владелец", "72 649", "541 530", "11 000", 11216, "kia-rio-2015.jpg", "Та самая третья, которую я придержал"),
 ]),
]
D25 = [
 ("Из ролика про Бэстюн, Пассат и L200", [
  ("FAW Бэстюн T77", 2023, "Два владельца", "8 816", "1 098 600", "22 000", 12097, "faw-bestune-t77-2023.jpg", None),
  ("Фольксваген Пассат", 2017, "Полный привод, три владельца", "120 501", "1 158 600", "23 000", 11913, "vw-passat-2017.jpg", None),
  ("Мицубиси L200", 2018, "Полный привод, два владельца", "99 715", "1 116 500", "22 000", 11883, "mitsubishi-l200-2018.jpg", None),
  ("Киа Сид", 2014, "Два владельца", "126 305", "573 500", "11 000", 12066, "kia-ceed-2014.jpg", "Та самая четвёртая из ролика"),
 ]),
 ("Из ролика про Хайлендер, Соренто и Крету", [
  ("Тойота Хайлендер", 2010, "Автомат, два владельца", "187 486", "1 024 000", "20 000", 11954, "toyota-highlander-2010.jpg", None),
  ("Киа Соренто", 2017, "Полный привод, автомат, один владелец", "121 800", "1 190 503", "24 000", 11728, "kia-sorento-2017.jpg", None),
  ("Хендай Крета", 2020, "Автомат, один владелец", "55 084", "1 203 369", "24 000", 12128, "hyundai-creta-2020.jpg", None),
  ("Джили Эмгранд X7", 2015, "Автомат, три владельца", "150 000", "394 322", "8 000", 11799, "geely-emgrand-x7-2015.jpg", "Тот самый четвёртый из ролика"),
 ]),
 ("Из ролика про Аутлендер, Атлас Про и Туарег", [
  ("Мицубиси Аутлендер", 2017, "Полный привод, вариатор, три владельца", "88 419", "1 168 600", "23 000", 11831, "mitsubishi-outlander-2017.jpg", None),
  ("Джили Атлас Про", 2022, "Полный привод, робот, один владелец", "38 698", "1 175 962", "24 000", 10635, "geely-atlas-pro-2022.jpg", None),
  ("Фольксваген Туарег", 2015, "Полный привод, автомат, три владельца", "200 162", "1 199 500", "24 000", 11604, "vw-touareg-2015.jpg", None),
  ("Сузуки Гранд Витара", 2010, "Полный привод, автомат, три владельца", "223 571", "603 800", "12 000", 11903, "suzuki-grand-vitara-2010.jpg", "Тот самый четвёртый из ролика"),
 ]),
 ("Из ролика про Мазду, Хонду и ПроСид", [
  ("Мазда CX-5", 2014, "Полный привод, автомат, два владельца", "125 737", "1 002 286", "20 000", 11573, "mazda-cx5-2014.jpg", None),
  ("Хонда CR-V", 2013, "Полный привод, автомат, один владелец", "237 312", "1 045 000", "21 000", 11779, "honda-crv-2013.jpg", None),
  ("Киа ПроСид", 2021, "Универсал, робот, два владельца", "92 294", "1 075 900", "21 000", 11524, "kia-proceed-2021.jpg", None),
  ("Фольксваген Поло", 2013, "Седан, автомат, два владельца", "105 000", "564 300", "11 000", 12179, "vw-polo-2013.jpg", "Та самая четвёртая из ролика"),
 ]),
 ("Из ролика про Jolion", [
  ("Хавал Джолион", 2023, "Полный привод, робот, один владелец", "22 552", "1 171 896", "23 000", 7634, "haval-jolion-2023.jpg", "Тот самый третий Jolion"),
 ]),
]

def nb(x):
    return str(x).replace(" ", "\u00a0")

def word(n):
    return "машин"  # 15, 17 — род. падеж мн. ч.

CSS = open(os.path.join(ROOT, "tools", "style.css"), encoding="utf-8").read()

def page(limit, data):
    e = html.escape
    n = sum(len(c) for _, c in data)
    first = data[0][1][0][7]
    title = f"{n} машин с платежом до {limit} в месяц"
    desc = "Машины из роликов INYCAR: фото, год, пробег, цена и платёж от. Смотреть в Telegram."
    og_img = (BASE_URL.rstrip("/") + "/assets/" + first) if BASE_URL else "../assets/" + first
    cards = []
    num = 0
    for head, cars in data:
        cards.append(f'<h2 class="block">{e(head)}</h2>')
        for (name, year, det, km, price, pay, post, img, mark) in cars:
            num += 1
            badge = f'<span class="mark">★ {e(mark)}</span>' if mark else ""
            cards.append(f'''<a class="card{' card--mark' if mark else ''}" href="{TG}/{post}" target="_blank" rel="noopener">
  <div class="ph"><img src="../assets/{img}" alt="{e(name)} {year}" width="800" height="600" loading="{'eager' if num<=2 else 'lazy'}" decoding="async"><span class="num n{(num-1)%5}">{num}</span></div>
  <div class="body">
    {badge}
    <h3>{e(name)} {year}</h3>
    <p class="meta">{e(det)}</p>
    <dl><div><dt>Пробег</dt><dd>{nb(km)}\u00a0км</dd></div><div><dt>Цена</dt><dd>{nb(price)}\u00a0₽</dd></div></dl>
    <p class="pay"><span>Платёж</span> от\u00a0{nb(pay)}\u00a0₽/мес</p>
    <span class="go">Смотреть в Telegram →</span>
  </div>
</a>''')
    cards_html = "\n".join(cards)
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1a1a1a">
<title>{e(title)} | INYCAR</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="INYCAR">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="600">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="preload" as="image" href="../assets/{first}">
<style>{CSS}</style>
</head>
<body>
<main class="wrap">
<header class="top">
  <span class="tag">РАСЧЁТ СТОИМОСТИ</span>
  <h1>{n} машин с платежом до {nb(limit)} в месяц</h1>
  <p class="lead">Обещал десять, получилось {n}: машины из всех роликов, вместе с теми, которые я придержал. Платёж у каждой «от», точную цифру под тебя посчитаем отдельно.</p>
  <a class="btn btn--y" href="{TG}" target="_blank" rel="noopener">📲 Подписаться на канал INYCAR</a>
  <a class="btn btn--o" href="{TEL}">📞 {nb(TEL_TXT)}</a>
</header>
{cards_html}
<section class="end">
  <p class="note">Это то, что есть прямо сейчас. Авто с пробегом уходят быстро, поэтому свежий список и новые поступления смотри в Telegram.</p>
  <p class="note">Понравилась машина? Позвони или напиши, посчитаем платёж лично под тебя.</p>
  <a class="btn btn--y" href="{TG}" target="_blank" rel="noopener">📲 Канал с машинами</a>
  <a class="btn btn--o" href="{TEL}">📞 Позвонить</a>
  <a class="btn btn--o" href="{SITE}" target="_blank" rel="noopener">🌐 Сайт inycar.ru</a>
  <p class="brand"><a href="{SITE}" target="_blank" rel="noopener">INYCAR</a></p>
</section>
</main>
<nav class="bar" aria-label="Быстрые действия">
  <a href="{TEL}" class="bar__b"><span aria-hidden="true">📞</span> Позвонить</a>
  <a href="{TG}" target="_blank" rel="noopener" class="bar__b bar__b--y"><span aria-hidden="true">📲</span> Канал</a>
</nav>
</body>
</html>
'''

def index():
    css = CSS
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1a1a1a">
<title>Расчёт стоимости | INYCAR</title>
<meta name="robots" content="noindex">
<style>{css}</style></head>
<body><main class="wrap"><header class="top">
<span class="tag">РАСЧЁТ СТОИМОСТИ</span>
<h1>Машины с платежом в месяц</h1>
<a class="btn btn--y" href="20/">Платёж до 20 000 ₽</a>
<a class="btn btn--y" href="25/">Платёж до 25 000 ₽</a>
<a class="btn btn--o" href="{TG}" target="_blank" rel="noopener">📲 Канал с машинами</a>
<p class="brand"><a href="{SITE}" target="_blank" rel="noopener">INYCAR</a></p>
</header></main></body></html>
'''

if __name__ == "__main__":
    for lim, d, folder in (("20 000", D20, "20"), ("25 000", D25, "25")):
        with open(os.path.join(ROOT, folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(lim, d))
        for _, cars in d:
            for c in cars:
                assert os.path.exists(os.path.join(ROOT, "assets", c[7])), c[7]
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index())
    print("ok")
