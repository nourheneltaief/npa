from models import Park, Trail, Wildlife, Announcement, User
from werkzeug.security import generate_password_hash
import requests, json, datetime

def seed_parks(app, db):
    with app.app_context():
        parks_data = [
            {
                'name': "Bou-Hedma National Park",
                'description': """
                The Bouhedma National Park is located in the governorates of Sidi Bouzid and Gafsa. It is situated 85 km
                east of Gafsa, 100 km south of Sidi Bouzid, 105 km west of Sfax, 100 km northwest of Gabès, 30 km from 
                Maknassy, and 27 km from Mezzouna. Established in 1980, the park covers an area of 16,488 hectares, of 
                which 8,804 hectares are under strict protection. The park has been part of UNESCO's network of 
                biosphere reserves since 1977. The park includes three zones of strict protection. It also contains a 
                temporary occupation zone of 2,400 hectares where about 200 families live, as well as a buffer zone 
                located between the temporary occupation area and the strict protection zones. The park spans arid 
                lower bioclimates with temperate and cool variations, extending into semi-arid lower bioclimates with
                cool variations. Precipitation is estimated at 140 mm in the plains and 300 mm at the summit of the 
                mountain.
                """,
                'location': "Gafsa/Bouzid",
                'image_url': "bouhedma.jpg"
            },
            {
                'name': "El Feidja National Park",
                'description': """
                The park of El Feidja is situated in the North West of Tunisia, 17 kilometers from Ghardimou and 49 
                kilometers from Jendouba. It is the natural and unspoilt region of Khroumirie which is the most humid in
                Tunisia. During the Neolithic era, 10,000 years ago man left his trace in El Feidja. There are also
                vestiges of the berber civilisation such as fortresses, tombstones etc… The park of El Feidja is a huge
                area, 2765 hectares, formed about 38 million years ago. There are superb, panoramic views over the dense
                forests especially from Mount “Kef El Nagcha”. The park of El Feidja is unique, considered one of the
                most beautiful in the world. It is rich in oak with a huge variety of flora and fauna such as stags,
                wild boar, jackals, etc.
                """,
                'location': "Jendouba",
                'image_url': "el_feidja.jpg"
            },
            {
                'name': "Boukornine National Park",
                'description': """
                Located just 15 kilometres north of the capital city of Tunisia, the peri-urban Boukornine National Park
                is a renowned tourist destination. The park is brimming with magnificent scenes of landscapes dotted
                with orchids and wild tulips. The Bou Kornine Mountain rises some 576 metres from the sublime
                vegetation-covered landscapes and hovers over the spectacular sapphire waters of the Gulf of Tunisia.
                The peaceful, biodiverse park is an idyllic place for cycling, walking and hiking. Visitors exploring
                the park are encouraged to look out for the adorable Etruscan Shrew, the world’s smallest mammal.
                Hiking up to the elevated viewpoints offer rewarding panoramic views of the Mediterranean’s bays and
                coastline. The closest town is the coastal area of Hammam-Lif which is easily accessible from Tunis, the
                capital. Most international visitors fly-into Tunis and either stay in the capital or the quaint town of
                Hammam-Lif. The national park is ideal for families and is great for day visits from the surrounding
                coastal towns.
                """,
                'location': "Ben Arous",
                'image_url': "boukornine.jpg"
            },
            {
                'name': "Lake Ichkeul",
                'description': """
                Lake Ichkeul is the last great freshwater lake of a chain that once stretched the length of North
                Africa. Characterised by a very specific hydrological functioning based on a double seasonal alternance
                of water levels and salinity, the lake and the surrounding marshes constitute an indispensible stop-over
                for the hundreds of thousands of migratory birds that winter at Ichkeul. Ichkeul National Park contains
                important natural habitats as an essential wintering site for western Palaearctic birds. Each winter,
                the property provides shelter to an exceptional density of water fowl with, in certain years, numbers
                reaching more than 300,000 ducks, geese and coots at the same time. Among these birds, the presence of
                three species of worldwide interest for their protection: the white-headed duck (Oxyura leucocephala),
                the ferruginous duck (Aythya nyroca) and the marbled duck (Marmaronetta angustirostris). With such a
                diversity of habitats, the property possesses a very rich and diversified fauna and flora with more than
                200 animal species and more than 500 plant species.
                """,
                'location': "Mateur",
                'image_url': "ichkeul.jpg"
            },
            {
                'name': "Chambi National Park",
                'description': """
                Chaambi National Park protects Tunisia’s highest mountain, Mount Chaambi. The spectacular peak forms
                part of the famous Atlas Mountains and is located close to the border of Algeria. The Aleppo
                pine-covered slopes are the last Tunisian forested parts before entering desert landscapes. The area is
                not a major tourist hotspot, but it does hold great appeal for die-hard hikers and climbers wanting to
                experience an untamed adventure in an unpredictable environment. Visitors to the park are rewarded with
                rare sightings of regal Peregrine falcons taking to the skies, and wild curly-horned Barbary sheep on
                the jagged mountain slopes. Located three hours from the capital of Tunis, the closest village is
                Kasserine. The village isn’t geared toward tourism, so staying there is not recommended. If Chaambi
                is on the bucket list, then visitors are encouraged to stay in the capital city of Tunis.
                """,
                'location': "Kasserine",
                'image_url': "chaambi.jpg"
            },
            {
                'name': "Sidi Toui National Park",
                'description': """
                Sidi Toui National Park is a national park in southern Tunisia opened in 1991, about fifty kilometers
                south of Ben Gardane and about twenty kilometers northwest of the Tunisian-Libyan border. The park
                extends over 6,315 hectares entirely fenced on the edge of the Sahara; a djebel culminating at 172
                meters, steppes and sand dunes constitute its characteristic landscape. The vegetation is composed of
                various species including white sagebrush. It is home to different Saharan species including mammals,
                such as the oryx, golden jackal, starving fox, gloved cat and fennec fox, but also different types of
                reptiles such as whiptail, common chameleon and snakes. Some migratory birds stop there from the Kneiss
                Islands. Others, sedentary, stay there all year round. We can cite the houbara bustard, the gambra
                partridge, the sandgrouse, the skylark, the common raven and the isabelle course. The park was in the
                past a place frequented by the African ostrich and the red hartebeest. The latter continued to exist
                between Dehiba and Hamada al-Hamra in Libya until 1912. Nowadays, both taxa are considered extinct in
                Tunisia. However, the red-necked ostrich is the subject of a reintroduction project in the national
                parks of Dghoumès and Bouhedma from individuals brought back from Morocco. As for the hartebeest, the
                North African subspecies (Alcelaphus buselaphus buselaphus) completely disappeared from the surface of
                the Earth at the beginning of the 20th century following intensive hunting. Proposals for the
                reintroduction of the closest subspecies, that of West Africa (Alcelaphus buselaphus major) have been
                made, but no concrete action has been taken to date.
                """,
                'location': "Medenine",
                'image_url': "toui.JPG"
            },
            {
                'name': "Jebel Chitana National Park",
                'description': """
               Jbel Chitana National Park (Cap Negro) is a national park located on the northern coast of Tunisia,
               between Cape Serrat and the Sidi El Barrak dam . It is made up of the Jebel Chitana forest series, which
               falls under the Bizerte forest district , and that of Bellif, which falls under the Béja forest district.
               It covers a total area of 10,122 hectares constituting a fenced integral protection zone, intended for
               the protection of the Mejen Ech Chitan peat bog, the Mhibès forest and the Sidi El Barrak dam as well as
               the preservation of endemic and rare plant and animal species, such as the white water lily among the
               flora and the Barbary deer among the fauna2. The park is located in the lower humid bioclimatic level
               with mild winters. For several generations, a few families have been practicing agriculture, livestock
               breeding and beekeeping in the Park. Aware of the great natural and cultural wealth of the Park, these
               families have set themselves the goal of enhancing its potential by developing the production and
               marketing of organic fruits, vegetables and honey, as well as an offer of agritourism and eco-tourism.
                """,
                'location': "Beja",
                'image_url': "chitana.JPG"
            }
        ]

        # Loop through each park data
        for park_data in parks_data:
            existing_park = Park.query.filter_by(name=park_data['name']).first()

            if not existing_park:
                new_park = Park(
                    name=park_data['name'],
                    description=park_data['description'],
                    location=park_data['location'],
                    image_url=park_data['image_url']
                )
                db.session.add(new_park)

        db.session.commit()


def create_fictive_trails(app, db):
    with app.app_context():
        # Fictive parks and trails
        parks = {
            "Bou-Hedma National Park": [
                {"name": "Bou-Hedma Trail", "difficulty": "Medium", "distance": 7.5,
                 "description": "A scenic trail in Bou-Hedma National Park"},
                {"name": "Bou-Hedma Desert Trail", "difficulty": "Hard", "distance": 10.0,
                 "description": "A desert trail with stunning views"}
            ],
            "El Feidja National Park": [
                {"name": "El Feidja Nature Walk", "difficulty": "Easy", "distance": 4.2,
                 "description": "A gentle walk through the lush forests of El Feidja"},
                {"name": "El Feidja Forest Trail", "difficulty": "Medium", "distance": 6.5,
                 "description": "A forest trail with moderate difficulty"}
            ],
        }

        for park_name, trails_data in parks.items():
            park = Park.query.filter_by(name=park_name).first()
            if park:
                for trail_data in trails_data:
                    existing_trail = Trail.query.filter_by(description=trail_data['description']).first()
                    if not existing_trail:
                        new_trail = Trail(
                            name=trail_data['name'],
                            park_id=park.id,
                            difficulty=trail_data['difficulty'],
                            distance=trail_data['distance'],
                            description=trail_data['description']
                        )
                        db.session.add(new_trail)

        db.session.commit()

def create_fictive_wildlife(app, db):
    with app.app_context():
        wildlife_entries = {
            "Bou-Hedma National Park": [
                {"species_name": "Barbary Sheep", "description": "A wild sheep native to North Africa",
                 "image_url": "https://example.com/barbary_sheep.jpg"},
                {"species_name": "Desert Fox", "description": "A small fox found in desert regions",
                 "image_url": "https://example.com/desert_fox.jpg"}
            ],
            "El Feidja National Park": [
                {"species_name": "Wild Boar", "description": "A wild boar, common in forested areas",
                 "image_url": "https://example.com/wild_boar.jpg"},
                {"species_name": "European Hedgehog", "description": "A small hedgehog species native to Europe",
                 "image_url": "https://example.com/european_hedgehog.jpg"}
            ],
        }

        for park_name, wildlife_data in wildlife_entries.items():
            park = Park.query.filter_by(name=park_name).first()
            if park:
                for wildlife in wildlife_data:
                    existing_wildlife = Wildlife.query.filter_by(park_id=park.id,
                                                                 species_name=wildlife["species_name"]).first()
                    if not existing_wildlife:
                        new_wildlife = Wildlife(
                            species_name=wildlife['species_name'],
                            park_id=park.id,
                            description=wildlife['description'],
                            image_url=wildlife['image_url']
                        )
                        db.session.add(new_wildlife)

        db.session.commit()

def create_fictive_announcements(app, db):
    with app.app_context():
        new_announcement = Announcement(
            park_id=1,
            title="New Trail Opened",
            content="A new trail has been opened in the park. Come and explore!"
        )
        existing_announcement = Announcement.query.filter_by(park_id=new_announcement.park_id,
                                                             title=new_announcement.title,
                                                             content=new_announcement.content).first()
        if not existing_announcement:
            db.session.add(new_announcement)

        db.session.commit()

def create_admin_user(app, db):
    with app.app_context():
        with open('../credentials/creds.json', 'r') as file:
            creds = json.load(file)

        admin_creds = creds["admin_creds"]
        hashed_password = generate_password_hash(admin_creds["password"])

        admin = User(
            username=admin_creds["username"],
            email=admin_creds["email"],
            password=hashed_password,
            role='admin'
        )

        existing_admin = User.query.filter_by(username=admin.username, email=admin.email).first()
        if not existing_admin:
            db.session.add(admin)
        db.session.commit()


def fetch_weather_data(location, date):
    with open('../credentials/creds.json', 'r') as file:
        creds = json.load(file)
    api_key = creds["weather_api_key"]
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    today = datetime.datetime.strptime(today, '%Y-%m-%d')
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    diff = (date - today).days
    url = f'https://api.weatherapi.com/v1/forecast.json?q={location}&days={diff}&key={api_key}'
    response = requests.get(url)
    return response.json()