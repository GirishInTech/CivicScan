from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reports.models import Report
from django.utils import timezone
import json

class Command(BaseCommand):
    help = 'Add sample report data to the database'

    def handle(self, *args, **options):
        # Sample data to add
        sample_data = [
            {
                "lat": 12.9173123410381,
                "lng": 77.4963587995404,
                "status": "clean",
                "review": "checking after migrating to postgresql",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Vijayashree Layout, Kengeri, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751310421/fpldkev0i39wbll1uzvg.jpg"
            },
            {
                "lat": 12.982023,
                "lng": 77.558288,
                "status": "dirty",
                "review": "testing different places from google map",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Rajajinagar 4M Block, Rajajinagar, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560010, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751315256/he6bkvssppowdt2avkau.jpg"
            },
            {
                "lat": 12.9174506,
                "lng": 77.4964224,
                "status": "clean",
                "review": "It is the room",
                "user": "Anonymous",
                "email": "N/A",
                "address": "Vijayashree Layout, Kengeri, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751374506/wntcrstdrmocs2uvtsqf.jpg"
            },
            {
                "lat": 12.9171523,
                "lng": 77.4976208,
                "status": "clean",
                "review": "Idk",
                "user": "Anonymous",
                "email": "N/A",
                "address": "Vijayashree Layout, Kengeri, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751442662/dfj4gl7yyiyqch1lc7ow.jpg"
            },
            {
                "lat": 12.9227106,
                "lng": 77.4989401,
                "status": "clean",
                "review": "It is the auditorium that's all",
                "user": "Anonymous",
                "email": "N/A",
                "address": "exit from IEM auditorium, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751604165/tyhv8rsaxf9eibxjaiht.jpg"
            },
            {
                "lat": 12.9739575,
                "lng": 77.6233058,
                "status": "dirty",
                "review": "It is metro and clean",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Kumbakonam Traditional Coffee, E 4th Street, Someshwarpura, Halasuru, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560008, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751634537/m35hwhaix2veavsjlora.jpg"
            },
            {
                "lat": 12.92261,
                "lng": 77.498558,
                "status": "dirty",
                "review": "Yes it is dirty",
                "user": "Anonymous",
                "email": "N/A",
                "address": "R. V. College of Engineering, Patanagere Main Road, BHEL Layout, Rajarajeshwari Nagar, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560098, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751658150/gng4tsyykhfomad305vp.png"
            },
            {
                "lat": 12.9174301,
                "lng": 77.4964189,
                "status": "clean",
                "review": "It is clean",
                "user": "Anonymous",
                "email": "N/A",
                "address": "Vijayashree Layout, Kengeri, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751658430/tqpvldt2vwl3tv4lfovt.jpg"
            },
            {
                "lat": 12.9715987,
                "lng": 77.5945627,
                "status": "clean",
                "review": "testing 1",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "St. Joseph's Indian High School, Vittal Mallya Road, D'Souza Layout, Richmond Town, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560001, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759364/t1daqw4fjz4gzaekddjl.png"
            },
            {
                "lat": 12.9352232,
                "lng": 77.6141655,
                "status": "dirty",
                "review": "testing 2",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Gramin, 80 Feet Road, Jogi Colony, Koramangala, Bangalore South, Bengaluru Urban, Karnataka, 560095, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759393/slanc0peywplgz7n5tbf.png"
            },
            {
                "lat": 12.9352232,
                "lng": 77.6141655,
                "status": "clean",
                "review": "testing 2",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Gramin, 80 Feet Road, Jogi Colony, Koramangala, Bangalore South, Bengaluru Urban, Karnataka, 560095, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759657/kspmhjlc0rdyaneklvkw.jpg"
            },
            {
                "lat": 13.0352022,
                "lng": 77.5974356,
                "status": "clean",
                "review": "testing 3",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Amarjyothi Nagara, Hebbal, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560032, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759689/y940thkzrkjcxcrjqc8n.jpg"
            },
            {
                "lat": 12.9858091,
                "lng": 77.6095796,
                "status": "dirty",
                "review": "testing 4",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Sivanchetti Gardens, Shivajinagar, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560001, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759740/jqvtfyieong4o05yotrh.jpg"
            },
            {
                "lat": 12.9012941,
                "lng": 77.5470174,
                "status": "dirty",
                "review": "testing 5",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Vasanthapura, Uttarahalli, Bangalore South, Bengaluru Urban, Karnataka, 560061, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759765/xjqrsjsddosj9p42ym07.jpg"
            },
            {
                "lat": 12.9081357,
                "lng": 77.6476072,
                "status": "clean",
                "review": "testing 6",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Parangipalya, Sector 2, HSR Layout, Bangalore South, Bengaluru Urban, Karnataka, 560102, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759801/jkihd2xjha6yh5bgwgcz.jpg"
            },
            {
                "lat": 13.0115271,
                "lng": 77.5520035,
                "status": "dirty",
                "review": "testing 7",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Narayana Nethralaya, Chord Road, Rajajinagara 1st R Block, Mahalakshmi Layout, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560010, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759819/kcbpvvaf5b8p8l2qsthi.jpg"
            },
            {
                "lat": 12.8442947,
                "lng": 77.6634488,
                "status": "dirty",
                "review": "testing 8",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "International Institute of Information Technology Bangalore, 26/C Opposite Infosys Gate, 1st Cross Road, Electronics City Phase 1, Bengaluru, Bangalore South, Bengaluru Urban, Karnataka, 560100, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759842/bmugeceardyimtupha0t.jpg"
            },
            {
                "lat": 13.0863483,
                "lng": 77.5747504,
                "status": "dirty",
                "review": "testing 9",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "GKVK Campus, 13th Main Road, Judicial Layout, Yelahanka taluku, Bengaluru Urban, Karnataka, 560065, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759865/cymznrrmgrpldjikswj2.jpg"
            },
            {
                "lat": 13.0863483,
                "lng": 77.5747504,
                "status": "dirty",
                "review": "testing 9",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "GKVK Campus, 13th Main Road, Judicial Layout, Yelahanka taluku, Bengaluru Urban, Karnataka, 560065, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759898/uaei1ib772ypohdziaum.jpg"
            },
            {
                "lat": 12.9496235,
                "lng": 77.6998652,
                "status": "dirty",
                "review": "testing 10",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "ICICI Bank, Outer Ring Road, MSR Layout, Marathahalli, Bangalore East, Bengaluru Urban, Karnataka, 560037, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759921/oamvwdujn7ai8hge8sru.jpg"
            },
            {
                "lat": 12.9981442,
                "lng": 77.5922001,
                "status": "clean",
                "review": "testing 11",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Palace Greens, Jayamahal Road, Jayamahal, Vasanth Nagar, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560006, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759986/h73znsota4bzvmilcwih.jpg"
            },
            {
                "lat": 12.91957,
                "lng": 77.6101163,
                "status": "dirty",
                "review": "testing 12",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "HOPCOMS, 16th Main Road, BTM Layout 1st Stage, BTM Layout, Bangalore South, Bengaluru Urban, Karnataka, 560029, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751759801/jkihd2xjha6yh5bgwgcz.jpg"
            },
            {
                "lat": 12.8750432,
                "lng": 77.6407894,
                "status": "dirty",
                "review": "testing 13",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Bangalore South, Bengaluru Urban, Karnataka, 560114, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760033/ky7hqrtgnkie8yygdech.jpg"
            },
            {
                "lat": 13.0281309,
                "lng": 77.6347396,
                "status": "dirty",
                "review": "testing 14",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "282/1, 1st Cross Road, Grace Town, HBR Layout, Bengaluru, Bangalore North, Bengaluru Urban, Karnataka, 560043, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760057/zfpjetc9tlykdtwt3wkk.jpg"
            },
            {
                "lat": 12.9181911,
                "lng": 77.5022937,
                "status": "dirty",
                "review": "testing 15",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Global Village Road, Sattva Global City, Rajarajeshwari Nagar, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560098, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760084/fntmzq56yydmjh9qqkjq.jpg"
            },
            {
                "lat": 12.9356923,
                "lng": 77.5351421,
                "status": "clean",
                "review": "testing 16",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "PES University, Outer Ring Road, Veerabhadra Nagara, Bengaluru, Bangalore South, Bengaluru Urban, Karnataka, 560085, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760115/xw9jsvihm4a1dteiyhqt.jpg"
            },
            {
                "lat": 13.049437,
                "lng": 77.6846278,
                "status": "dirty",
                "review": "testing 17",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Ramapura, Bangalore East, Bengaluru Urban, Karnataka, 560016, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760143/m4nrufsg78krwb28q0wo.jpg"
            },
            {
                "lat": 12.8889331,
                "lng": 77.5857356,
                "status": "clean",
                "review": "testing 18",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "6th Main Road, Nataraja Layout, Bangalore South, Bengaluru Urban, Karnataka, 560078, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760172/ec0c49dfc9ztbgiruyz1.jpg"
            },
            {
                "lat": 12.9752273,
                "lng": 77.7000642,
                "status": "dirty",
                "review": "testing 19",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Ferns City, Bangalore East, Bengaluru Urban, Karnataka, 560048, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760201/fdbyek7vniwj5gx6dhby.jpg"
            },
            {
                "lat": 12.8602881,
                "lng": 77.5773645,
                "status": "clean",
                "review": "testin 20",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Gottigere, Bangalore South, Bengaluru Urban, Karnataka, 560083, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751760222/excmw3ivpcjrql6veczp.jpg"
            },
            {
                "lat": 12.922633,
                "lng": 77.498566,
                "status": "dirty",
                "review": "dffiguhsdaiufsduf",
                "user": "Anonymous",
                "email": "N/A",
                "address": "R. V. College of Engineering, exit from IEM auditorium, Mailasandra, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1751880931/mszh2a7xnc8mva9yfwxc.jpg"
            },
            {
                "lat": 12.9173905,
                "lng": 77.4964564,
                "status": "clean",
                "review": "Pg",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "Vijayashree Layout, Kengeri, Mailasandra, Bengaluru, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1752395832/c1klbgzit5oipgvfkmbb.jpg"
            },
            {
                "lat": 12.9167635,
                "lng": 77.4999526,
                "status": "dirty",
                "review": "Near bihari message no dustbin",
                "user": "Anonymous",
                "email": "N/A",
                "address": "Vijayashree Layout, Kengeri, Mailasandra, Bengaluru, Bangalore South, Bengaluru Urban, Karnataka, 560060, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1752498683/jcszvk6sgmsfpyygiagf.jpg"
            },
            {
                "lat": 12.9222877,
                "lng": 77.4983505,
                "status": "clean",
                "review": "Laptop",
                "user": "admin",
                "email": "Girish4936@gmail.com",
                "address": "R. V. College of Engineering, Global Village Road, Sattva Global City, Mailasandra, Bengaluru, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1752560257/kbsnufngwqgqgxuzdmvi.jpg"
            },
            {
                "lat": 12.9226436402116,
                "lng": 77.4986039584656,
                "status": "dirty",
                "review": "this place is dirty because the dustbins are not emptied properly",
                "user": "aman",
                "email": "aman@gmail.com",
                "address": "R. V. College of Engineering, Way to admission office, Dubasi Palya, Mailasandra, Bengaluru, Bangalore South, Bengaluru Urban, Karnataka, 560059, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1752743971/yavlclqbkx8oxwdrm6st.png"
            },
            {
                "lat": 12.9226687,
                "lng": 77.500133,
                "status": "clean",
                "review": "Because the girl in this picture is dirty 🤢",
                "user": "Anonymous",
                "email": "N/A",
                "address": "R. V. College of Engineering, Patanagere Main Road, BHEL Layout, Rajarajeshwari Nagar, Mailasandra, Bengaluru, Bangalore South, Bengaluru Urban, Karnataka, 560098, India",
                "photo_url": "http://res.cloudinary.com/dgqm61eqb/image/upload/v1752843030/vkddro87rdox66r0nmvb.jpg"
            }
        ]

        created_count = 0
        skipped_count = 0

        for data in sample_data:
            try:
                # Get or create user
                if data['user'] == 'Anonymous':
                    user = None
                else:
                    user, created = User.objects.get_or_create(
                        username=data['user'],
                        defaults={
                            'email': data['email'],
                            'first_name': data['user'],
                            'is_active': True
                        }
                    )

                # Check if report already exists (based on coordinates and review)
                existing_report = Report.objects.filter(
                    location=f"{data['lat']},{data['lng']}",
                    review=data['review']
                ).first()

                if existing_report:
                    self.stdout.write(f"Skipped: Report already exists for {data['address']}")
                    skipped_count += 1
                    continue

                # Create the report
                report = Report.objects.create(
                    user=user,
                    photo=data['photo_url'],
                    status=data['status'],
                    location=f"{data['lat']},{data['lng']}",
                    review=data['review'],
                    address=data['address']
                )

                created_count += 1
                self.stdout.write(f"Created: {data['status']} report at {data['address']}")

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating report: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {created_count} new reports. Skipped {skipped_count} existing reports.'
            )
        ) 