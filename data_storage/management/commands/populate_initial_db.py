"""
Initial PostgreSQL DB Population
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth.models import User

# Resource models
from resources.models import Attribute, Location, State, Address, Organization, Person, Project

# Data Storage models
from data_storage.models import Trial, TrialYear, TrialAttribute, TrialEvent
from data_storage.models import Treatment, TreatmentLevel, TrialTreatment
from data_storage.models import CommonName, Germplasm, GermplasmAlias
from data_storage.models import Plot, PlotCrop, PlotTreatment, PlotType

# Ontology models
from ontology.models import TraitEntity, TraitAttribute, VarTrait, VarScale, VarMethod, Variable, SopDocument, AgroProcess

# Imaging Models
from imaging.models import Image, ImageOperation, AwsModel


from faker import Faker
import random
import pandas as pd
import polars as pl

faker = Faker()

class Command(BaseCommand):
    help = 'Populate initial data into PostgreSQL'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Handle the initial data creation

        # Create an admin user
        username = 'admin'
        password = 'password'
        email = 'admin@example.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {username}'))
        
        US_STATES_AND_ABBREVIATIONS = [
            ("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"),
            ("California", "CA"), ("Colorado", "CO"), ("Connecticut", "CT"), ("Delaware", "DE"),
            ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"), ("Idaho", "ID"),
            ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"), ("Kansas", "KS"),
            ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"), ("Maryland", "MD"),
            ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"), ("Mississippi", "MS"),
            ("Missouri", "MO"), ("Montana", "MT"), ("Nebraska", "NE"), ("Nevada", "NV"),
            ("New Hampshire", "NH"), ("New Jersey", "NJ"), ("New Mexico", "NM"), ("New York", "NY"),
            ("North Carolina", "NC"), ("North Dakota", "ND"), ("Ohio", "OH"), ("Oklahoma", "OK"),
            ("Oregon", "OR"), ("Pennsylvania", "PA"), ("Rhode Island", "RI"), ("South Carolina", "SC"),
            ("South Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"),
            ("Vermont", "VT"), ("Virginia", "VA"), ("Washington", "WA"), ("West Virginia", "WV"),
            ("Wisconsin", "WI"), ("Wyoming", "WY")
        ]

        # Creating all states
        if not State.objects.exists():
            for state in US_STATES_AND_ABBREVIATIONS:
                State.objects.create(name=state[0], abbreviation=state[1])

        # Populate Addresses
        if not Address.objects.exists():
            # Corteva
            Address.objects.create(
                name = "Corteva - Johnston",
                address_line_1 = "7000 NW 62nd Ave.",
                city = "Johnston",
                state_id = State.objects.get(abbreviation="IA"),
                postal_code = "50131"
            )

            # TLI
            Address.objects.create(
                name = "The Land Institute - Salina",
                address_line_1 = "2440 E. Water Well Rd.",
                city = "Salina",
                state_id = State.objects.get(abbreviation="KS"),
                postal_code = "67401"
            )

            # ISU-abe
            Address.objects.create(
                name = "Iowa State University ABE - Ames",
                address_line_1 = "605 Bissell Rd.",
                building_name = 'Elings Hall',
                building_suite_number = '1340',
                city = "Ames",
                state_id = State.objects.get(abbreviation="IA"),
                postal_code = "50011"
            )

            # UNL
            Address.objects.create(
                name = "University of Nebraska - Lincoln",
                address_line_1 = "1400 R St.",
                city = "Lincoln",
                state_id = State.objects.get(abbreviation="NE"),
                postal_code = "68588"
            )

            # UWM
            Address.objects.create(
                name = "University of Wisconsin - Madison",
                address_line_1 = "500 Lincoln Dr.",
                city = "Madison",
                state_id = State.objects.get(abbreviation="WI"),
                postal_code = "53706"
            )

        # Populate organizations
        if not Organization.objects.exists():
            # Corteva
            Organization.objects.create(
                name='Corteva Agriscience',
                abbreviation='CTV',
                address_id=Address.objects.get(name="Corteva - Johnston"),
                ror_id='https://ror.org/02pm1jf23',
                logo_url='assets/corteva_agriscience.png'
            )

            # TLI
            Organization.objects.create(
                name='The Land Institute',
                abbreviation='TLI',
                address_id=Address.objects.get(name="The Land Institute - Salina"),
                ror_id='https://ror.org/00jxaym78',
                logo_url='assets/the_land_institute.png'
            )

            # ISU-abe
            Organization.objects.create(
                name='Iowa State University',
                abbreviation='ISU',
                address_id=Address.objects.get(name="Iowa State University ABE - Ames"),
                ror_id='https://ror.org/04rswrd78',
                logo_url='assets/iowa_state_university.png'
            )

            # UNL
            Organization.objects.create(
                name='University of Nebraska - Lincoln',
                abbreviation='UNL',
                address_id=Address.objects.get(name="University of Nebraska - Lincoln"),
                ror_id='https://ror.org/043mer456',
                logo_url='assets/university_of_nebraska_lincoln.jpg'
            )

            # UWM
            Organization.objects.create(
                name='University of Wisconsin - Madison',
                abbreviation='UWM',
                address_id=Address.objects.get(name="University of Wisconsin - Madison"),
                ror_id='https://ror.org/01y2jtd41',
                logo_url='assets/university_of_wisconsin.jpg'
            )
            
        # Populate Persons
        if not Person.objects.exists():
            for _, org in enumerate(Organization.objects.all()):
                for _ in range(10):
                    Person.objects.create(
                        first_name = faker.first_name(),
                        last_name = faker.last_name(),
                        middle_initial =  faker.random_uppercase_letter(),
                        affiliation_id = org,
                        email = faker.email(),
                        phone_number = faker.phone_number(),
                        orcid = '1234-1244-1233-1224'
                    )

        # Populate Project
        if not Project.objects.exists():
            # RegenPGC
            Project.objects.create(
                name = 'Regen PGC',
                description = "Regenerating America's landscape through perennial groundcovers",
                funding = "USDA-AFRI 123456789",
                website = "https://www.regenpgc.org/"
            )

            # Fab PGC
            Project.objects.create(
                name = 'FAB PGC',
                description = "A project that generates lots of data through keystone field experiments",
                funding = "DOE 123456789",
                website = ""
            )

        # Populate Locations
        if not Location.objects.exists():
            for _ in range(10):
                Location.objects.create(
                    name = 'trial_' + faker.word(),
                    latitude = faker.latitude(),
                    longitude = faker.longitude(),
                    type = 'trial'
                )

        # Populate FieldTrial
        if not Trial.objects.exists():
            for _ in range(4):
                org = Organization.objects.order_by('?').first()
                Trial.objects.create(
                    name = org.abbreviation + "_trial_" + str(faker.random_number()),
                    location_id = Location.objects.filter(type='trial').order_by('?').first(),
                    manager_id = Person.objects.filter(affiliation_id=org).order_by('?').first(),
                    project_id = Project.objects.order_by('?').first(),
                    affiliation_id = org,
                    establishment_year = faker.year(),
                    multi_year = bool(random.randint(0, 1))
                )
            
            org = Organization.objects.get(name='The Land Institute')
            project = Project.objects.get(name='FAB PGC')
            Trial.objects.create(
                name = 'FABPGC_TLI_keystone', 
                location_id = Location.objects.filter(type='trial').order_by('?').first(),
                manager_id = Person.objects.filter(affiliation_id=org).order_by('?').first(),
                project_id = project,
                affiliation_id = org,
                establishment_year = 2024,
                multi_year = True
            )

        # Populate Trial years
        if not TrialYear.objects.all():
            fab_trial = Trial.objects.get(name='FABPGC_TLI_keystone')
            years = [2024, 2025, 2026, 2027]
            for year in years:
                trial_year = TrialYear(
                    trial_id=fab_trial, 
                    year=year)
                trial_year.full_clean()
                trial_year.save()

        # Populate Treatment Groups
        if not Treatment.objects.exists():
            Treatment.objects.create(
                name='FABPGC Crop Rotation',
                type='planting',
                description='A crop rotation treatment that consists of three levels: corn-corn, corn-soybean, and soybean-corn'
            )
            Treatment.objects.create(
                name='FABPGC PGC',
                type='germplasm',
                description='A PGC treatment group that consists of three levels: kbg (Kentucky Bluegrass), poa bulbosa (Radix Poa bulbosa), and no pgc (Control)'
            )
            Treatment.objects.create(
                name='FABPGC Harvest',
                type='operations',
                description='A harvest treatment group that consists of two different levels: corn-harvest, and corn-stover-harvest'
            )
            Treatment.objects.create(
                name='FABPGC Cash Crop',
                type='germplasm',
                description='A cash crop germplasm treatment group that consists of several different corn and soybean treatment levels: H1 and H2 (corn hybrids), and V1 and V2 (soybean varieties)'
            )

        # Populate Treatment Levels
        if not TreatmentLevel.objects.exists():
            # Crop Rotation
            levels = ['corn-corn', 'corn-soybean', 'soybean-corn']
            treatment_group = Treatment.objects.get(name='FABPGC Crop Rotation')
            for level in levels:
                TreatmentLevel.objects.create(
                    treatment_id=treatment_group,
                    level=level
                )
            # PGC
            levels = ['kbg', 'poa bulbosa', 'no pgc']
            treatment_group = Treatment.objects.get(name='FABPGC PGC')
            for level in levels:
                TreatmentLevel.objects.create(
                    treatment_id=treatment_group,
                    level=level
                )
            # Havest Treatment Levels
            levels = ['corn-harvest', 'corn-stover-harvest']
            treatment_group = Treatment.objects.get(name='FABPGC Harvest')
            for level in levels:
                TreatmentLevel.objects.create(
                    treatment_id=treatment_group,
                    level=level
                )
            # Cash Crop
            levels = ['H1', 'H2', 'V1', 'V2']
            treatment_group = Treatment.objects.get(name='FABPGC Cash Crop')
            for level in levels:
                TreatmentLevel.objects.create(
                    treatment_id=treatment_group,
                    level=level
                )
        
        # Populate TrialTreatments
        if not TrialTreatment.objects.exists():
            trial = Trial.objects.get(name='FABPGC_TLI_keystone')
            treatments = Treatment.objects.all()
            for tr in treatments:
                TrialTreatment.objects.create(
                    trial_id = trial,
                    treatment_id = tr
                )

        # Populate Plots
        if not Plot.objects.exists():
            trial = Trial.objects.get(name='FABPGC_TLI_keystone')
            plot_list = pd.read_csv('data_storage/keystone_plot_list.csv')
            nrow = len(plot_list)
            for i in range(nrow):
                row = plot_list.loc[i]
                try:
                    parent_plot = Plot.objects.get(label=row.parent_plot_id)
                except Plot.DoesNotExist:
                    parent_plot = None
                Plot.objects.create(
                    trial_id=trial, 
                    block=row.block,
                    label=row.label,
                    type=row.type,
                    width_m=row.width_m,
                    length_m=row.length_m,
                    parent_plot_id=parent_plot
                )
        
        # Populate SOP Table
        if not SopDocument.objects.exists():
            sop_df = pl.read_csv('data_storage/sop_documents.csv')
            for i in range(len(sop_df.rows())):
                SopDocument.objects.create(
                    document_name = sop_df[i]['document_name'].item(),
                    label = sop_df[i]['label'].item(),
                    version = sop_df[i]['version'].item(),
                    doi = sop_df[i]['doi'].item(),
                    doc_url = sop_df[i]['doc_url'].item(),
                    description = sop_df[i]['description'].item()
                )

        # Populate CommonName
        if not CommonName.objects.exists():
            names = ['Corn', 'Soybean', 'Kentucky Bluegrass', 'Poa bulbosa', 'Kura clover']
            
            for name in names:
                CommonName.objects.create(
                    name=name
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))