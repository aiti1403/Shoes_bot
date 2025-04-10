from database import Database
import config

def add_sample_products():
    db = Database()
    
    # Очистим таблицу товаров перед добавлением новых
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products")
    conn.commit()
    
    # Список примерных товаров по категориям
    sample_products = [
        # Мужская обувь (5 товаров)
        {
            'name': 'Мужские кеды',
            'category': 'Мужская обувь',
            'description': 'Натуральная кожа.',
            'price': 5994,
            'image_url': "https://market.yandex.ru/product--muzhskie-vysokie-kedy/1913156269?sku=101993079969&uniqueId=2560087&do-waremd5=QNktBXkKAoABwUzKe-u0lw&utm_term=68191852%7C1913156269&clid=1601&utm_source=yandex&utm_medium=search&utm_campaign=ymp_offer_dp_odezhda_model_mrkscr_bko_dyb_search_rus&utm_content=cid%3A113170438%7Cgid%3A5494886094%7Caid%3A1854091899053504439%7Cph%3A53112880039%7Cpt%3Apremium%7Cpn%3A1%7Csrc%3Anone%7Cst%3Asearch%7Crid%3A53112880039%7Ccgcid%3A0&yclid=10637444519249838079"
        },
        {
            'name': 'ROOMAN',
            'category': 'Мужская обувь',
            'description': 'Натуральная кожа.',
            'price': 5994,
            'image_url': "https://main-cdn.sbermegamarket.ru/big2/hlr-system/-20/823/349/705/181/446/100028569391b0.jpg"
        },
        {
            'name': 'Мужские туфли классические',
            'category': 'Мужская обувь',
            'description': 'Элегантные туфли для официальных мероприятий.',
            'price': 6500,
            'image_url': "https://ae01.alicdn.com/kf/HTB1eFC1XZ_vK1RkSmRyq6xwupXa7/2018-New-Men-Dress-Shoes-Men-Formal-Shoes-Classic-Business-Luxury-Men-Oxfords-Footwear-Suit-Shoes.jpg"
        },
        {
            'name': 'Мужские ботинки зимние',
            'category': 'Мужская обувь',
            'description': 'Теплые зимние ботинки с натуральным мехом.',
            'price': 7800,
            'image_url': "https://wlooks.ru/images/article/orig/2017/01/zimnie-muzhskie-botinki-columbia-42.jpg"
        },
        {
            'name': 'Мужские мокасины',
            'category': 'Мужская обувь',
            'description': 'Удобные мокасины для повседневной носки.',
            'price': 4200,
            'image_url': "https://sun9-33.userapi.com/s/v1/if1/0FYMMq29WewV9BX9j-qDd69QdNOk1QNEtYKS1fDVsbYKjuQNpBbGBnGsGEmCB7Tx5ySQAj94.jpg?quality=96&as=32x24,48x36,72x54,108x81,160x120,240x180,360x270,480x360,540x405,640x480,720x540,800x600&from=bu&u=ab9FKHXLvRSxks8EZPnflFn8KYkOpFJ9tk-P6C-NsFQ&cs=800x600"
        },
        
        # Женская обувь (5 товаров)
        {
            'name': 'Черные или коричневые полуботинки',
            'category': 'Женская обувь',
            'description': 'Натуральная кожа, удобная колодка, мягкая стелька.',
            'price': 5994,
            'image_url': "https://yandex.ru/maps/org/shoes_club/238929936319/gallery/?ll=44.981327%2C53.217046&photos%5Bbusiness%5D=238929936319&photos%5Bid%5D=urn%3Ayandex%3Asprav%3Aphoto%3AznyFpyKnzfT88kL8MSStrMhiTZ9ZuAjK&utm_content=add_review&utm_medium=reviews&utm_source=maps-reviews-widget&z=17"
        },
        {
            'name': 'Ботильоны',
            'category': 'Женская обувь',
            'description': 'Ботильоны из натуральной кожи.',
            'price': 7194,
            'image_url': "https://market.yandex.ru/product--botilony-zhenskie-demisezonnye-milana-212311-1-110v-chernyi/1777440363?sku=101854913957&uniqueId=2666474&do-waremd5=BtcfOdRcZYynUEQdD9E2YA&sponsored=1&cpc=VEOAPY_DMV3qpgRGJV4UONfghz0LftyKHVri0bLzrgoV5OPs2f7x7f0KTTTsPl7ZmqFHz6I8TH_X_XgTKiuI8vpEX1pIQg_Mrj5YtGS4nOZnY7qYPib3E0-Dr_Rd2az6pRZ-Mxzk2X7cTc46CwN0IpuTHVneyK9Cf_NHRJoPaQ9cTE2kFIoTe0BKQ_S2NJWifznyoFfH8m3LFhqttjHcYrd6ZQ15y-KFL51ZTsw8x7pY9ShunnG1N-AhYGueEfhblEZbbVgusDTwqBwn1VZet0codvPZeNbHn7ABaya3Mw-3FYgiKmnkwe11hBIQvSFy1bQP4cqzKYRv_8y0EugcBWJCZcrXGTp1OUJe5lpd1EQV4Qtcdy9PalSDYg_2m5pT6f-Nfi-Dx2m40datC24QV6r8c0ceWf4fQ-xL5rCWTJOvPSo6qNigZ6Bb9Yiegh-50dKrrzqvOnwgVfVk1W1XA_nqD2B-5hipc8Zy7_4gyaw1_z4kz7Ejes-9dPMV-_NXY7Edr541_TFxqIU3moT-sWcIMVbVEwI01zeX7gUhipc%2C"
        },
        {
            'name': 'Женские туфли на каблуке',
            'category': 'Женская обувь',
            'description': 'Элегантные туфли на устойчивом каблуке 7 см.',
            'price': 5500,
            'image_url': "https://avatars.mds.yandex.net/i?id=9a509ce40497c19427ef74bca8d9abfb_l-4599550-images-thumbs&n=13"
        },
        {
            'name': 'Женские сапоги зимние',
            'category': 'Женская обувь',
            'description': 'Теплые зимние сапоги с натуральным мехом.',
            'price': 8200,
            'image_url': "https://avatars.mds.yandex.net/i?id=d45bfc60dfa228a959a50c46ba9c58b6_l-8201364-images-thumbs&n=13"
        },
        {
            'name': 'Женские балетки',
            'category': 'Женская обувь',
            'description': 'Удобные балетки для повседневной носки.',
            'price': 3800,
            'image_url': "https://ae01.alicdn.com/kf/HTB1Pj.qlLiSBuNkSnhJq6zDcpXa0/Spring-Summer-Ladies-Shoes-Ballet-Flats-Women-Flat-Shoes-Woman-Ballerinas-Black-Large-Size-43-44.jpg"
        },
        
        # Кроссовки (5 товаров)
        {
            'name': 'Adidas Climacool',
            'category': 'Кроссовки',
            'description': 'Максимальная свежесть и сухость.',
            'price': 7794,
            'image_url': "https://images-eu.ssl-images-amazon.com/images/I/51jvZ-8mTML.jpg"
        },
        {
            'name': 'Nike',
            'category': 'Кроссовки',
            'description': 'Легендарные кроссовки с видимой воздушной подушкой.',
            'price': 6594,
            'image_url': "https://cdn1.ozone.ru/s3/multimedia-1-h/7015943033.jpg"
        },
        {
            'name': 'Puma RS-X',
            'category': 'Кроссовки',
            'description': 'Стильные кроссовки с технологией Running System.',
            'price': 7200,
            'image_url': "https://i8.amplience.net/i/jpl/jd_345786_e"
        },
        {
            'name': 'New Balance 574',
            'category': 'Кроссовки',
            'description': 'Классические кроссовки с отличной амортизацией.',
            'price': 6800,
            'image_url': "https://i.ebayimg.com/00/s/Nzg1WDE2MjI=/z/TbIAAOSwAttk0MiB/$_57.PNG"
        },
        {
            'name': 'Reebok Classic',
            'category': 'Кроссовки',
            'description': 'Культовые кроссовки в ретро-стиле.',
            'price': 5900,
            'image_url': "https://images-na.ssl-images-amazon.com/images/I/71Qe3W19LnL._AC_.jpg"
        },
        
        # Сумки муж и жен (5 товаров)
        {
            'name': 'Сумка женская кожаная',
            'category': 'Сумки муж и жен',
            'description': 'Элегантная женская сумка из натуральной кожи. Вместительная и стильная.',
            'price': 4201,
            'image_url': "https://avatars.mds.yandex.net/i?id=87d2e582aca1797167a754f801d89271_l-8237885-images-thumbs&n=13"
        },
        {
            'name': 'Сумка женская кожаная, Турция',
            'category': 'Сумки муж и жен',
            'description': 'Натуральная кожа. Лучшая для деловых встреч.',
            'price': 5592,
            'image_url': "https://avatars.mds.yandex.net/i?id=cee67ef55db3cebb7713b655328cd433_l-11502102-images-thumbs&n=13"
        },
        {
            'name': 'Мужской портфель',
            'category': 'Сумки муж и жен',
            'description': 'Классический кожаный портфель для деловых встреч.',
            'price': 6500,
            'image_url': "https://www.batohyatasky.cz/jpg/panska-kozena-aktovka-arabic-barka-hneda-vintage-a-vice-barev_original.jpg"
        },
        {
            'name': 'Рюкзак городской',
            'category': 'Сумки муж и жен',
            'description': 'Вместительный рюкзак для повседневного использования.',
            'price': 3800,
            'image_url': "https://avatars.mds.yandex.net/get-mpic/12505310/2a0000018f3a23527a12b650a080d7b863c6/orig"
        },
        {
            'name': 'Клатч женский',
            'category': 'Сумки муж и жен',
            'description': 'Элегантный клатч для вечерних мероприятий.',
            'price': 2900,
            'image_url': "https://manozo.cz/83359-thickbox_default/elegantni-semisove-damske-psanicko-cerne-barvy-s-retizkovym-raminkem.jpg"
        },
        
        # Ремни (5 товаров)
        {
            'name': 'Ремень мужской кожаный',
            'category': 'Ремни',
            'description': 'Классический мужской ремень из натуральной кожи. Ширина 3.5 см.',
            'price': 1500,
            'image_url': "https://i1.wp.com/xn--e1aaufl0f.com/wp-content/uploads/2019/02/B40-693.jpg?fit=1300%2C975&ssl=1"
        },
        {
            'name': 'Ремень женский узкий',
            'category': 'Ремни',
            'description': 'Элегантный женский ремень из экокожи. Ширина 2 см.',
            'price': 1200,
            'image_url': "https://remni-store.ru/wa-data/public/shop/products/72/86/28672/images/17845/17845.750.jpg"
        },
        {
            'name': 'Ремень мужской плетеный',
            'category': 'Ремни',
            'description': 'Стильный плетеный ремень для мужчин. Натуральная кожа.',
            'price': 1800,
            'image_url': "https://avatars.mds.yandex.net/i?id=7ab07e21cdb4992fc3a8dccefa7b7c84_l-5297681-images-thumbs&n=13"
        },
        {
            'name': 'Ремень мужской с автоматической пряжкой',
            'category': 'Ремни',
            'description': 'Современный ремень с автоматической пряжкой.',
            'price': 2200,
            'image_url': "https://img.joomcdn.net/3f5739badf360d09ff7865f6fee4e6a32f9c76c1_original.jpeg"
        },
        {
            'name': 'Ремень женский декоративный',
            'category': 'Ремни',
            'description': 'Стильный декоративный ремень для женщин.',
            'price': 1600,
            'image_url': "https://avatars.mds.yandex.net/i?id=ba64ddadf35026fed3ab6aa5ffcbe97e_l-7012253-images-thumbs&n=13"
        },
        
        # Перчатки (5 товаров)
        {
            'name': 'Перчатки женские кожаные',
            'category': 'Перчатки',
            'description': 'Элегантные женские перчатки из натуральной кожи. Подкладка из флиса.',
            'price': 1700,
            'image_url': "https://cdn1.ozone.ru/s3/multimedia-1-c/7205521512.jpg"
        },
        {
            'name': 'Перчатки мужские кожаные',
            'category': 'Перчатки',
            'description': 'Классические мужские перчатки из натуральной кожи. Утепленная подкладка.',
            'price': 1900,
            'image_url': "https://avatars.mds.yandex.net/get-mpic/4501142/img_id6265069324202592244.jpeg/orig"
        },
        {
            'name': 'Перчатки женские трикотажные',
            'category': 'Перчатки',
            'description': 'Теплые трикотажные перчатки с сенсорными вставками для работы с сенсорными экранами.',
            'price': 700,
            'image_url': "https://s.gpcdn.ru/products/000/317/218/original_tkyf8shnnqwu.jpg"
        },
        {
            'name': 'Перчатки спортивные',
            'category': 'Перчатки',
            'description': 'Спортивные перчатки для фитнеса и тренировок.',
            'price': 1200,
            'image_url': "https://market.yandex.ru/product--gonochnye-perchatki-s-paltsami-velosipednye-perchatki-dlia-motokrossa-am-velosipeda-mtb-mx-gornyi-velosiped-mototsikletnye-mototsikletnye-velosipednye-perchatki-2022/256592630?sku=103819604530&uniqueId=134799842&do-waremd5=0dEjeLfs9-pcM_FFEIUSBg&utm_term=13876352%7C256592630&clid=1601&utm_source=yandex&utm_medium=search&utm_campaign=ymp_offer_dp_auto_model_mrkscr_bko_dyb_search_rus&utm_content=cid%3A113177676%7Cgid%3A5474977503%7Caid%3A16367426659%7Cph%3A53090714028%7Cpt%3Apremium%7Cpn%3A2%7Csrc%3Anone%7Cst%3Asearch%7Crid%3A53090714028%7Ccgcid%3A0&yclid=13992497432197857279"
        },
        {
            'name': 'Перчатки мужские вязаные',
            'category': 'Перчатки',
            'description': 'Теплые вязаные перчатки для мужчин.',
            'price': 800,
            'image_url': "https://i1.proimagescdn.ru/images/b2images/1077/03122013-676-2_1.jpg"
        },
        
        # Очки (5 товаров)
        {
            'name': 'Очки солнцезащитные женские',
            'category': 'Очки',
            'description': 'Стильные солнцезащитные очки для женщин. Защита от UV-лучей.',
            'price': 1500,
            'image_url': "https://market.yandex.ru/product--rb3025-001-51-55-14/1780222984?sku=835946020&uniqueId=189503427&do-waremd5=srLpxwpFZv9qf1kxZ6sSEA&utm_term=433018%7C1780222984&clid=1601&utm_source=yandex&utm_medium=search&utm_campaign=ymp_offer_dp_odezhda_model_mrkscr_bko_dyb_search_rus&utm_content=cid%3A113170438%7Cgid%3A5474889494%7Caid%3A16366592505%7Cph%3A53112899386%7Cpt%3Apremium%7Cpn%3A1%7Csrc%3Anone%7Cst%3Asearch%7Crid%3A53112899386%7Ccgcid%3A0&yclid=18001931722333880319"
        },
        {
            'name': 'Очки солнцезащитные мужские',
            'category': 'Очки',
            'description': 'Классические солнцезащитные очки для мужчин. Поляризационные линзы.',
            'price': 1700,
            'image_url': "https://market.yandex.ru/product--muzhskie-poliarizovannye-solntsezashchitnye-ochki-youpin-05/946765103?sku=103732824683&uniqueId=134799842&do-waremd5=LrFFpLM_dKigrnu61aCmQg&utm_term=433018%7C946765103&clid=1601&utm_source=yandex&utm_medium=search&utm_campaign=ymp_offer_dp_odezhda_model_mrkscr_bko_dyb_search_rus&utm_content=cid%3A113170438%7Cgid%3A5474889494%7Caid%3A16366592505%7Cph%3A53112899386%7Cpt%3Apremium%7Cpn%3A5%7Csrc%3Anone%7Cst%3Asearch%7Crid%3A53112899386%7Ccgcid%3A0&yclid=10907049831847428095"
        },
        {
            'name': 'Очки солнцезащитные спортивные',
            'category': 'Очки',
            'description': 'Спортивные солнцезащитные очки с прочной оправой. Идеально для активного отдыха.',
            'price': 2100,
            'image_url': "https://market.yandex.ru/product--ochki-solntsezashchitnye-sportivnye-chernoe-more/1002315920?sku=103064552822&uniqueId=1996313&do-waremd5=w40ZW7TGRClvTGTvguWbbw&utm_term=433018%7C1002315920&clid=1601&utm_source=yandex&utm_medium=search&utm_campaign=ymp_offer_dp_odezhda_model_mrkscr_bko_dyb_search_rus&utm_content=cid%3A113170438%7Cgid%3A5474889494%7Caid%3A16366592505%7Cph%3A53112899386%7Cpt%3Apremium%7Cpn%3A2%7Csrc%3Anone%7Cst%3Asearch%7Crid%3A53112899386%7Ccgcid%3A0&yclid=16760506534239928319"
        },
        {
            'name': 'Очки для компьютера',
            'category': 'Очки',
            'description': 'Очки с защитой от синего света для работы за компьютером.',
            'price': 1800,
            'image_url': "https://avatars.mds.yandex.net/get-mpic/4977072/img_id2901799963527114243.jpeg/orig"
        },
        {
            'name': 'Очки-авиаторы',
            'category': 'Очки',
            'description': 'Классические очки в стиле авиатор',
            'price': 1600,
            'image_url': "https://e.allegroimg.com/original/0116ef/ec828f8047b9bb14425b49474cee/OKULARY-AVIATORY-PILOTKI-PRZECIWSLONECZNE-Damskie"
        }
    ]
    
    # Добавляем товары в базу данных
    for product in sample_products:
        db.add_product(
            product['name'],
            product['category'],
            product['description'],
            product['price'],
            product['image_url']
        )
    
    print(f"Добавлено {len(sample_products)} товаров в базу данных.")

if __name__ == "__main__":
    add_sample_products()

