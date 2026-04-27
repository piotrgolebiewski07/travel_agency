import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from trips.models import Trip, TripImage, Review
from datetime import date


def create_trip(title_pl,
                title_en,
                description_pl,
                description_en,
                start_date,
                end_date,
                country,
                location,
                price,
                image_urls,
                reviews=None
                ):
    trip, created = Trip.objects.get_or_create(
        title_en=title_en,
        defaults={
            "title_pl": title_pl,
            "description_pl": description_pl,
            "description_en": description_en,
            "price": price,
            "start_date": start_date,
            "end_date": end_date,
            "country": country,
            "location": location,
            "max_people": 10,
            "available": True,
        },
    )

    if created:
        for i, url in enumerate(image_urls):
            TripImage.objects.create(
                trip=trip,
                image_url=url,
                is_main=(i == 0),  # main photo
            )

        if reviews:
            for r in reviews:
                Review.objects.create(
                    trip=trip,
                    name=r["name"],
                    rating=r["rating"],
                    comment=r["comment"]
                )


def run():
    create_trip(
        "Wakacje na Santorini",
        "Santorini Holiday",
        """Odkryj piękno Santorini podczas starannie zaplanowanej wycieczki po wyspie.
                    Ta podróż obejmuje najbardziej charakterystyczne miejsca, w tym urokliwą miejscowość Oia,
                    gdzie można podziwiać jeden z najpiękniejszych zachodów słońca w Europie.
                    
                    Podczas wycieczki odkryjesz unikalną architekturę wyspy — białe domy z niebieskimi kopułami
                    położone na spektakularnych, wulkanicznych klifach.
                    
                    W programie przewidziano również czas na relaks, degustację kuchni śródziemnomorskiej
                    oraz udział w opcjonalnych atrakcjach, takich jak degustacja wina czy rejs po Morzu Egejskim.
                    
                    Idealna propozycja dla par, małych grup oraz osób szukających komfortowego wypoczynku.""",
        """Discover the beauty of Santorini on a carefully planned island getaway.
                    This trip takes you through the most iconic spots, including the charming village of Oia,
                    where you will experience one of the most breathtaking sunsets in Europe.
                    
                    During the tour, you will explore the island’s unique architecture — white houses with blue domes
                    set along dramatic volcanic cliffs.
                    
                    The itinerary also includes time to relax, enjoy Mediterranean cuisine,
                    and take part in optional activities such as wine tasting or a scenic cruise on the Aegean Sea.
                    
                    This short escape is perfect for couples and small groups.""",
        date(2026, 7, 1),
        date(2026, 7, 8),
        "Greece",
        "Santorini",
        600,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/santorini_1.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/santorini_2.jpg"
        ],
        reviews=[
            {
                "name": "Anna",
                "rating": 5,
                "comment": "To była absolutnie wyjątkowa podróż, a widoki na białe domy i błękitne morze sprawiały, że człowiek nie chciał wracać do rzeczywistości."
            },
            {
                "name": "John",
                "rating": 4,
                "comment": "The island is stunning and very well organized for tourists, although in some places it felt a bit crowded during the peak hours."
            },
            {
                "name": "Kasia",
                "rating": 5,
                "comment": "Świetna wycieczka, wszystko dopięte na ostatni guzik i naprawdę można było odpocząć."
            }
        ]
    )

    create_trip(
        "City Break Barcelona",
        "Barcelona City Break",
        """Barcelona to wyjątkowe połączenie śródziemnomorskiego klimatu i miejskiej energii.
                    Miasto zachwyca architekturą, plażami i doskonałą kuchnią.
                    
                    Najważniejsze atrakcje:
                    - Sagrada Família
                    - Park Güell
                    - Dzielnica Gotycka
                    - La Rambla
                    - Plaża Barceloneta
                    
                    Miasto, w którym historia, sztuka i morze tworzą niezapomnianą atmosferę.""",
        """Barcelona is a perfect blend of Mediterranean charm and urban energy.
                    
                    Top attractions:
                    - Sagrada Família
                    - Park Güell
                    - Gothic Quarter
                    - La Rambla
                    - Barceloneta Beach
                    
                    Discover a city where history, art, and the sea create an unforgettable atmosphere.""",
        date(2026, 9, 1),
        date(2026, 9, 5),
        "Spain",
        "Barcelona",
        350,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/barcelona_1.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/barcelona_2.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/barcelona_6.jpg"
        ],
        reviews=[
            {
                "name": "Marek",
                "rating": 4,
                "comment": "Barcelona zrobiła na mnie ogromne wrażenie swoją architekturą i klimatem, a połączenie zwiedzania i odpoczynku na plaży było idealne."
            },
            {
                "name": "Emily",
                "rating": 5,
                "comment": "Amazing experience with beautiful architecture, great food and a vibrant atmosphere that made every day feel exciting and unique."
            }
        ]
    )

    create_trip(
        "Kanion Verdon",
        "Verdon Canyon Adventure",
        """Kanion Verdon, często nazywany europejskim Grand Canyonem,
                    to jedno z najbardziej spektakularnych miejsc we Francji.
                    
                    Wysokie klify, turkusowa rzeka i liczne możliwości aktywnego wypoczynku
                    czynią to miejsce idealnym dla miłośników natury i przygód.""",
        """Gorges du Verdon, often called the French Grand Canyon,
                    is one of the most spectacular natural sites in Europe.
                    
                    It is a paradise for nature lovers, offering kayaking, hiking, and breathtaking views.""",
        date(2026, 8, 1),
        date(2026, 8, 4),
        "France",
        "Verdon",
        200,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/gorges_1.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/gorges_2.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/gorges_6.jpg",
        ],
        reviews=[
            {
                "name": "Tom",
                "rating": 5,
                "comment": "Niesamowite miejsce dla osób, które kochają naturę, ciszę i spektakularne widoki, bo kanion naprawdę robi ogromne wrażenie na żywo."
            }
        ]
    )

    create_trip(
        "Madera - aktywny wypoczynek",
        "Madeira Adventure Escape",
        """Madera to wyspa wiecznej wiosny, idealna dla osób aktywnych.
                    Zachwyca klifami, górami i bujną roślinnością.
                    
                    Najważniejsze atrakcje:
                    - szlaki levadas
                    - Funchal
                    - Cabo Girão
                    - Porto Moniz""",
        """Madeira is the island of eternal spring, perfect for active travelers.
                    
                    Top attractions:
                    - levada trails
                    - Funchal
                    - Cabo Girão
                    - Porto Moniz""",
        date(2026, 10, 21),
        date(2026, 10, 28),
        "Portugal",
        "Madeira",
        800,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/madera_1.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/madera_2.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/madera_3.jpg"
        ],
        reviews=[
            {
                "name": "Piotr",
                "rating": 5,
                "comment": "Madera zachwyciła mnie swoją naturą i spokojem, a piesze trasy wzdłuż levad były jednymi z najpiękniejszych jakie widziałem."
            },
            {
                "name": "Laura",
                "rating": 4,
                "comment": "Great destination for active holidays with beautiful landscapes and fresh air, although some hikes were more demanding than expected."
            }
        ]
    )

    create_trip(
        "Wyspy Kanaryjskie",
        "Canary Islands Holiday",
        """Wyspy Kanaryjskie to archipelag wiecznego lata,
                    gdzie każda wyspa oferuje inne doświadczenia.
                    
                    Od wulkanicznych krajobrazów po piaszczyste wydmy i oceaniczne widoki.""",
        """The Canary Islands are a paradise of eternal summer.
                    
                    From volcanic landscapes to golden dunes and ocean views,
                    each island offers something unique.""",
        date(2026, 7, 25),
        date(2026, 7, 31),
        "Spain",
        "Canary Islands",
        600,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/wyspy_kanaryjskie_1.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/wyspy_kanaryjskie_2.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/wyspy_kanaryjskie_3.jpg",
        ]
    )

    create_trip(
        "Malaga i Costa del Sol",
        "Malaga City & Beach Escape",
        """Malaga to słoneczne miasto łączące historię i nowoczesność.
                    Znajdziesz tu zabytki, plaże i wyjątkową atmosferę.
                    
                    Najważniejsze atrakcje:
                    - Alcazaba
                    - Gibralfaro
                    - Muzeum Picassa
                    - plaża La Malagueta""",
        """Malaga is a sunny city blending history and modern life.
                    
                    Top attractions:
                    - Alcazaba
                    - Gibralfaro Castle
                    - Picasso Museum
                    - La Malagueta Beach""",
        date(2026, 6, 3),
        date(2026, 6, 10),
        "Spain",
        "Malaga",
        450,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/malaga_6.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/malaga_3.jpg",
        ],
        reviews=[
            {
                "name": "Tomasz",
                "rating": 4,
                "comment": "Bardzo przyjemne miasto z piękną pogodą, dobrą kuchnią i ciekawymi zabytkami, idealne na spokojny city break."
            },
            {
                "name": "Michał",
                "rating": 3,
                "comment": "Miasto jest ładne i ma swój klimat, ale momentami było dość tłoczno i nie wszystko zrobiło na mnie takie wrażenie jak się spodziewałem."
            },
            {
                "name": "Laura",
                "rating": 2,
                "comment": "Weather was great but overall the trip felt a bit too touristy and crowded, which made it harder to really enjoy the place."
            },
            {
                "name": "Paweł",
                "rating": 3,
                "comment": "Wyjazd był w porządku, ale niektóre atrakcje okazały się mniej interesujące niż oczekiwałem i brakowało mi czegoś wyjątkowego."
            }
        ]
    )

    create_trip(
        "Szwajcaria - góry i jeziora",
        "Swiss Alps & Lakes Adventure",
        """Szwajcaria to raj dla miłośników gór i natury.
                
                    Zachwyca majestatycznymi Alpami, krystalicznie czystymi jeziorami i perfekcyjnie zadbanymi miasteczkami.
                
                    Najważniejsze atrakcje:
                    - Matterhorn
                    - Jezioro Genewskie
                    - Interlaken
                    - kolejki górskie i panoramy Alp
                
                    Idealna destynacja dla aktywnego wypoczynku i niezapomnianych widoków.""",
        """Switzerland is a paradise for mountain and nature lovers.
                
                    It offers breathtaking Alps, crystal-clear lakes, and charming towns.
                
                    Top attractions:
                    - Matterhorn
                    - Lake Geneva
                    - Interlaken
                    - mountain railways and panoramic views
                
                    Perfect for active holidays and unforgettable landscapes.""",
        date(2026, 6, 10),
        date(2026, 6, 17),
        "Switzerland",
        "Alps",
        800,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/szwajcaria_1.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/szwajcaria_2.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/szwajcaria_3.jpg"
        ],
        reviews=[
            {
                "name": "Andrzej",
                "rating": 4,
                "comment": "Widoki w Alpach są niesamowite, a organizacja wyjazdu sprawiła, że można było w pełni cieszyć się naturą."
            },
            {
                "name": "Emma",
                "rating": 4,
                "comment": "Beautiful scenery and very clean environment, although prices were quite high compared to other destinations."
            }
        ]
    )

    create_trip(
        "Wybrzeże Dorset",
        "Dorset Coast Escape",
        """Dorset to jedno z najpiękniejszych wybrzeży Anglii, słynące z Jurassic Coast wpisanego na listę UNESCO.
    
                    Znajdziesz tu spektakularne klify, naturalne formacje skalne i malownicze zatoki.
                
                    Najważniejsze atrakcje:
                    - Durdle Door
                    - Lulworth Cove
                    - Jurassic Coast
                    - klify i szlaki spacerowe
                
                    Idealne miejsce dla miłośników natury i spokojnego wypoczynku.""",
        """Dorset is one of the most beautiful coastal regions in England, famous for the Jurassic Coast (UNESCO).
                
                    You will find dramatic cliffs, natural rock formations, and picturesque bays.
                
                    Top attractions:
                    - Durdle Door
                    - Lulworth Cove
                    - Jurassic Coast
                    - coastal hiking trails
                
                    A perfect destination for nature lovers and peaceful escapes.""",
        date(2026, 7, 15),
        date(2026, 7, 20),
        "United Kingdom",
        "Dorset",
        420,
        image_urls=[
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/dorset_1.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/dorset_2.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/dorset_3.jpg"
        ],
        reviews=[
            {
                "name": "Oliver",
                "rating": 5,
                "comment": "The coastline is absolutely stunning and walking along the cliffs was one of the most relaxing experiences I have had in a long time."
            },
            {
                "name": "Anna",
                "rating": 4,
                "comment": "Bardzo piękne widoki i spokojna atmosfera, choć miejscami brakowało mi większej liczby atrakcji poza spacerami."
            },
            {
                "name": "James",
                "rating": 3,
                "comment": "Nice place for a quiet getaway with great views, but overall it felt a bit repetitive after a couple of days."
            },
            {
                "name": "Katarzyna",
                "rating": 2,
                "comment": "Miejsce ładne, ale pogoda była zmienna i momentami ciężko było w pełni cieszyć się wyjazdem."
            },
            {
                "name": "Daniel",
                "rating": 4,
                "comment": "Great scenery and peaceful environment, although transport between locations could have been a bit more convenient."
            }
        ]
    )


if __name__ == "__main__":
    run()

