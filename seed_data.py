import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from trips.models import Trip, TripImage
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
                image_urls
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
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/santorini_4.jpg",
            "https://raw.githubusercontent.com/piotrgolebiewski07/travel_agency/main/media/trips/santorini_3.jpg"
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
        ]
    )


if __name__ == "__main__":
    run()

