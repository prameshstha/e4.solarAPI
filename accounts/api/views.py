import threading
import threading

from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DarwinSolar.utils import EmailThread, my_domain
from accounts.api.serializer import CustomUserSerializer, RegistrationSerializer, AllCustomUserSerializer, \
    ChangePasswordSerializer, CustomUserSerializer1, ElectricityRetailersSerializer
from accounts.models import CustomUser, InstallerUser, InstallerToken
from company.api.installer_api.authentication import InstallerTokenAuthentication
from company.models import Company
from customer_portal.api.serializer import CustomerFilesSerializer, JobDetailsSerializer, FileTypeSerializer
from customer_portal.models import JobDetails, FileFieldSetting, ElectricityRetailers, FileType


class CustomerListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = AllCustomUserSerializer


class CustomerEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # print(self.kwargs)
        customer_id = self.kwargs['pk']

        queryset = CustomUser.objects.filter(id=customer_id)
        return queryset

    serializer_class = CustomUserSerializer


retailers = [
    {
        "retailer": "1st Energy",
        "website": "www.1stenergy.com.au",
        "phone": "1300 426 594"
    },
    {
        "retailer": "ActewAGL Retail",
        "website": "www.actewagl.com.au",
        "phone": "131 450"
    },
    {
        "retailer": "Active Utilities",
        "website": "www.activeutilities.com.au",
        "phone": "1300 587 623"
    },
    {
        "retailer": "AGL",
        "website": "www.agl.com.au",
        "phone": "131 245"
    },
    {
        "retailer": "Alinta Energy",
        "website": "www.alintaenergy.com.au",
        "phone": "133 702"
    },
    {
        "retailer": "Amber Electric&nbsp;",
        "website": "www.amber.com.au&nbsp;",
        "phone": "1800 531 907"
    },
    {
        "retailer": "Apex Energy",
        "website": "www.apexenergy.com.au",
        "phone": "1300 273 969"
    },
    {
        "retailer": "Arc Energy&nbsp;",
        "website": "www.arcenergygroup.com.au",
        "phone": "1300 025 965"
    },
    {
        "retailer": "Aurora Energy",
        "website": "www.auroraenergy.com.au",
        "phone": "1300 132 003"
    },
    {
        "retailer": "Balance Commodities and Energy",
        "website": "www.balance.energy",
        "phone": "03 9021 8857"
    },
    {
        "retailer": "Blue NRG",
        "website": "www.bluenrg.com.au",
        "phone": "1300 599 888"
    },
    {
        "retailer": "Bright Spark Power",
        "website": "www.brightsparkpower.com.au",
        "phone": "1300 010 277"
    },
    {
        "retailer": "CleanCo Queensland",
        "website": "www.cleancoqld.com.au",
        "phone": "07 3328 3708"
    },
    {
        "retailer": "CleanPeak Energy",
        "website": "www.cleanpeakenergy.com.au",
        "phone": "1300 038 069"
    },
    {
        "retailer": "CPE Mascot",
        "website": "www.cleanpeakmascot.com.au",
        "phone": "1300 057 405"
    },
    {
        "retailer": "CleanTech Energy",
        "website": "www.cleantechenergy.com.au",
        "phone": "08 6147 7555"
    },
    {
        "retailer": "Cogent Energy&nbsp;",
        "website": "www.cogentenergy.com.au",
        "phone": "(03) 9652 5025"
    },
    {
        "retailer": "Commander Power and Gas&nbsp;",
        "website": "www.commander.com.au",
        "phone": "1300 012 726"
    },
    {
        "retailer": "Cova U",
        "website": "www.covau.com.au",
        "phone": "1300 689 866"
    },
    {
        "retailer": "CS Energy",
        "website": "www.csenergy.com.au",
        "phone": "1800 950 595"
    },
    {
        "retailer": "Diamond Energy",
        "website": "www.diamondenergy.com.au",
        "phone": "1300 838 009"
    },
    {
        "retailer": "Discover Energy",
        "website": "www.discoverenergy.com.au",
        "phone": "1300 946 898"
    },
    {
        "retailer": "Dodo Power &amp; Gas",
        "website": "www.dodo.com.au",
        "phone": "133 636"
    },
    {
        "retailer": "EA Connect&nbsp;",
        "website": "www.eaconnect.com",
        "phone": "1300 121 603&nbsp;"
    },
    {
        "retailer": "EDL Retail",
        "website": "www.edlenergy.com",
        "phone": "(07) 3541 3000"
    },
    {
        "retailer": "Electricity in a Box",
        "website": "www.electricityinabox.com.au",
        "phone": "1300 933 039"
    },
    {
        "retailer": "Elysian Energy",
        "website": "www.elysianenergy.com.au",
        "phone": "1300 870 300"
    },
    {
        "retailer": "Energy Australia",
        "website": "www.energyaustralia.com.au",
        "phone": "133 466"
    },
    {
        "retailer": "Energy Australia Yallourn",
        "website": "www.energyaustralia.com.au",
        "phone": "133 466"
    },
    {
        "retailer": "Energy Locals",
        "website": "www.energylocals.com.au",
        "phone": "1300 693 637"
    },
    {
        "retailer": "Energy On",
        "website": "www.energyon.com.au",
        "phone": "1300 323 263"
    },
    {
        "retailer": "Enova Energy",
        "website": "www.enovaenergy.com.au",
        "phone": "02 5622 1700"
    },
    {
        "retailer": "Ergon Energy",
        "website": "www.ergon.com.au",
        "phone": "131 046"
    },
    {
        "retailer": "Evergy",
        "website": "www.evergy.com.au",
        "phone": "1300 383 749"
    },
    {
        "retailer": "EZI Power",
        "website": "www.ezipower.com.au",
        "phone": "1300 599 008"
    },
    {
        "retailer": "Altogether Group (formerly Flow Systems)",
        "website": "www.altogethergroup.com.au",
        "phone": "1300 806 806"
    },
    {
        "retailer": "Future X Power (Online Power &amp; Gas)",
        "website": "www.futurexpower.com.au",
        "phone": "1300 599 008"
    },
    {
        "retailer": "GEE Power &amp; Gas",
        "website": "www.gee.com.au",
        "phone": "1300 707 042"
    },
    {
        "retailer": "GloBird Energy",
        "website": "www.globirdenergy.com.au",
        "phone": "&nbsp;133 456"
    },
    {
        "retailer": "Glow Power (Energy Services Management)",
        "website": "www.myglowpower.com.au&nbsp;",
        "phone": "1300 092 572"
    },
    {
        "retailer": "Humenergy",
        "website": "www.humenergy.com.au&nbsp;",
        "phone": "1300 622 322"
    },
    {
        "retailer": "Iberdrola Australia Holdings Pty Limited",
        "website": "www.iberdrola.com",
        "phone": "1800 514 843"
    },
    {
        "retailer": "Locality Planning Energy",
        "website": "www.localityenergy.com.au",
        "phone": "1800 040 168"
    },
    {
        "retailer": "Localvolts",
        "website": "www.localvolts.com",
        "phone": "02 8006 8052"
    },
    {
        "retailer": "Lumo Energy",
        "website": "www.lumoenergy.com.au",
        "phone": "1300 115 866"
    },
    {
        "retailer": "Macquarie Bank",
        "website": "www.macquarie.com",
        "phone": "(02) 8232 3333"
    },
    {
        "retailer": "Metered Energy Holdings",
        "website": "www.meteredenergy.com.au",
        "phone": "1300 633 637"
    },
    {
        "retailer": "Microgrid Power",
        "website": "www.microgridpower.com.au",
        "phone": "1300 647 888"
    },
    {
        "retailer": "Mojo Power",
        "website": "www.mojopower.com.au",
        "phone": "1300 019 649"
    },
    {
        "retailer": "Momentum Energy",
        "website": "www.momentum.com.au",
        "phone": "1800 627 228"
    },
    {
        "retailer": "MTA Energy",
        "website": "www.mtaenergy.com",
        "phone": "02 8363 1310"
    },
    {
        "retailer": "Necr (Hanwha Energy Retail)",
        "website": "www.nectr.com.au",
        "phone": "1300 111 211"
    },
    {
        "retailer": "Neighbourhood Energy (Alinta)&nbsp;",
        "website": "www.neighbourhood.com.au",
        "phone": "1300 764 860"
    },
    {
        "retailer": "Next Business Energy",
        "website": "www.nextbusinessenergy.com.au",
        "phone": "1300 466 398"
    },
    {
        "retailer": "OC Energy",
        "website": "www.ocenergy.com.au",
        "phone": "1800 684 993"
    },
    {
        "retailer": "Origin Energy",
        "website": "www.originenergy.com.au",
        "phone": "132 461"
    },
    {
        "retailer": "OVO Energy",
        "website": "www.ovoenergy.com.au",
        "phone": "1300 937 686"
    },
    {
        "retailer": "OzGen Retail",
        "website": "www.intergen.com",
        "phone": "07 3001 7177"
    },
    {
        "retailer": "People Energy",
        "website": "www.peopleenergy.com.au",
        "phone": "1300 788 970"
    },
    {
        "retailer": "Pooled Energy",
        "website": "www.pooledenergy.com",
        "phone": "1300 364 703"
    },
    {
        "retailer": "Positive Energy",
        "website": "www.positivenergy.com.au",
        "phone": "1300 083 083"
    },
    {
        "retailer": "Powerclub",
        "website": "www.powerclub.com.au",
        "phone": "1300 294 459"
    },
    {
        "retailer": "Powerdirect",
        "website": "www.powerdirect.com.au",
        "phone": "1300 307 966"
    },
    {
        "retailer": "PowerHub",
        "website": "www.powerhub.net.au&nbsp;",
        "phone": "1300 196 673"
    },
    {
        "retailer": "Powershop Australia",
        "website": "www.powershop.com.au",
        "phone": "1800 462 668"
    },
    {
        "retailer": "Progressive Green (trading as Flow Power)",
        "website": "www.flowpower.com.au",
        "phone": "1300 080 608"
    },
    {
        "retailer": "QEnergy",
        "website": "www.qenergy.com.au",
        "phone": "1300 448 535"
    },
    {
        "retailer": "Radian Energy",
        "website": "www.radian.com.au&nbsp;",
        "phone": "1300 805 925"
    },
    {
        "retailer": "Real Utilities",
        "website": "www.realutilities.com.au",
        "phone": "1300 161 668"
    },
    {
        "retailer": "ReAmped Energy",
        "website": "www.reampedenergy.com.au",
        "phone": "1800 841 627"
    },
    {
        "retailer": "Red Energy",
        "website": "www.redenergy.com.au",
        "phone": "131 806"
    },
    {
        "retailer": "Sanctuary Energy",
        "website": "www.sanctuaryenergy.com.au",
        "phone": "1300 109 099"
    },
    {
        "retailer": "Savant Energy Power Networks",
        "website": "www.savantenergy.com.au",
        "phone": "1300 117 376"
    },
    {
        "retailer": "Shell Energy Retail",
        "website": "www.shellenergy.com.au",
        "phone": "13 23 76"
    },
    {
        "retailer": "Smartest Energy&nbsp;",
        "website": "www.smartestenergy.com.au",
        "phone": "1300 176 031"
    },
    {
        "retailer": "Smart Energy",
        "website": "www.smartenergygroup.com.au",
        "phone": "1300 133 055"
    },
    {
        "retailer": "Stanwell Corporation",
        "website": "www.stanwellenergy.com",
        "phone": "1800 300 351"
    },
    {
        "retailer": "Simply Energy",
        "website": "www.simplyenergy.com.au",
        "phone": "138 808"
    },
    {
        "retailer": "Social Energy&nbsp;",
        "website": "www.social.energy",
        "phone": "1300 322 059"
    },
    {
        "retailer": "Starcorp Energy",
        "website": "www.starcorpenergy.com.au",
        "phone": "1300 337 827"
    },
    {
        "retailer": "Sumo",
        "website": "www.sumo.com.au",
        "phone": "13 88 60"
    },
    {
        "retailer": "Sunset Power International (trading as Delta Electricity)",
        "website": "www.de.com.au",
        "phone": "02 4352 6468"
    },
    {
        "retailer": "Sustainable Savings",
        "website": "www.utilityshop.com.au",
        "phone": "08 7127 1510"
    },
    {
        "retailer": "Tango Energy",
        "website": "www.tangoenergy.com",
        "phone": "1800 010 648"
    },
    {
        "retailer": "Tas Gas Retail",
        "website": "www.tasgas.com.au",
        "phone": "1800 750 750"
    },
    {
        "retailer": "The Embedded Networks Company Pty Ltd (trading as seene)",
        "website": "www.seene.com.au",
        "phone": "1300 609 387"
    },
    {
        "retailer": "Tilt Renewables",
        "website": "www.tiltrenewables.com",
        "phone": "1300 660 623"
    },
    {
        "retailer": "Weston Energy",
        "website": "www.westonenergy.com.au",
        "phone": "02 9011 7674"
    },
    {
        "retailer": "WINconnect",
        "website": "www.winconnect.com.au",
        "phone": "1300 791 970"
    },
    {
        "retailer": "Y.E.S. Energy",
        "website": "www.yesenergy.net.au",
        "phone": "(08) 8119 0771"
    },
    {
        "retailer": "ZEN Energy (formerly&nbsp;SIMEC ZEN Energy Retail)",
        "website": "www.zenenergy.com.au",
        "phone": "1300 936 466"
    }
]


class Login(APIView):
    def post(self, request):
        # serializer = LoginSerializer(data=request.data)
        # print(request.data)
        email = request.data['email']
        password = request.data['password']

        if email and password:
            try:
                # Try to find a user matching your username
                user = CustomUser.objects.get(email=email)
                pwd_valid = check_password(password, user.password)
                print(pwd_valid)
                #  Check the password is the reverse of the username
                # something wrong here need to check asap
                if pwd_valid:
                    # Yes? return the Django user object
                    token = Token.objects.get_or_create(user=user)
                    # change according to the needs
                    # if customer are client single company

                    # company = Company.objects.filter(company_customers=user).first()
                    # if customer are client of multiple company
                    company = Company.objects.filter(company_customers=user).values()
                    user_dict = (model_to_dict(user))
                    user_dict.pop('last_login')
                    user_dict.pop('date_joined')
                    user_dict.pop('groups')
                    user_dict.pop('user_permissions')
                    user_dict.pop('password')
                    user_dict['token'] = str(token[0])
                    user_dict['company'] = company  # if customer are client of multiple company
                    # user_dict['company_name'] = company.company_name
                    return Response(user_dict, 200)
                else:
                    # No? return None - triggers default login failed
                    return Response({'Error': 'Email or Password wrong'}, 403)
            except CustomUser.DoesNotExist:
                # No user was found, return None - triggers default login failed
                return Response({'Error': 'User Does not exist'}, 404)

        # to insert retailsers details in database
        # print(retailers[0]['retailer'])
        # for a in retailers:
        #     print(a['retailer'])
        #     print(a['website'])
        #     print(a['phone'])
        #     ElectricityRetailers.objects.create(retailer_name=a['retailer'], website=a['website'], phone=a['phone'])
        # return Response({'Error': 'User Does not exist'}, 404)


# def modify_input_for_multiple_files(password, company_id, customer_crm_id, first_name, last_name, phone, email,
#                                     street, city, postcode, state, country, job_number, solar_panel,
#                                     system_size, inverter, no_of_battery, hotwater, aircon,
#                                     no_of_panels, installation_date, system_cost):
#
#     customer_details = {'customer_crm_id': customer_crm_id, 'first_name': first_name, 'last_name': last_name,
#                         'phone': phone, 'email': email, 'street': street, 'city': city, 'postcode': postcode,
#                         'state': state, 'country': country, 'password': password}
#     # company = Company.objects.filter(id=company_id).first()
#     job_details = {'company': company_id, 'street': street, 'city': city, 'postcode': postcode, 'state': state, 'country': country,
#                    'job_number': job_number, 'aircon': aircon, 'no_of_panels': no_of_panels, 'solar_panel': solar_panel,
#                    'system_size': system_size, 'inverter': inverter, 'no_of_battery': no_of_battery,
#                    'hotwater': hotwater, 'installation_date': installation_date, 'system_cost': system_cost}
#     customer_files = {'customer_crm_id': customer_crm_id, 'job_number': job_number}
#     return customer_details, job_details, customer_files


class RegistrationView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        # req = request.data
        # dummy data
        req = {'company': 1, 'customer_crm_id': '12009051', 'first_name': 'pramesh', 'last_name': 'SolarTest',
               'phone': '+610424011797',
               'job_number': 'DSD1172', 'email': 'prameshnp@gmail.com', 'street': '1/35 De Latour Street',
               'city': 'Coconut Grove', 'postcode': '0810', 'state': 'NT', 'country': 'Australia',
               'solar_panel': 'REC',
               'system_size': '9900', 'inverter': 'Soltaro AIO 10kW Inverter + 10kW Battery', 'no_of_battery': '2x',
               'hotwater': '12 Panel;270L', 'aircon': 'Deye 5kW', 'no_of_panels': '30',
               'installation_date': 'Nov 06 2021', 'system_cost': '18650'}
        company_id = req.get('company', '')  # this is most required!!!
        email = req.get('email', '')
        # customer_crm_id = req.get('customer_id', '')
        # first_name = req.get('first_name', '')
        # last_name = req.get('last_name', '')
        # phone = req.get('phone', '')
        # street = req.get('street', '')
        # city = req.get('city', '')
        # postcode = req.get('postcode', '')
        # state = req.get('state', '')
        # country = req.get('country', '')
        # job_number = req.get('job_number', '')
        # solar_panel = req.get('solar_panel', '')
        # system_size = req.get('system_size', '')
        # inverter = req.get('inverter', '')
        # no_of_battery = req.get('no_of_battery', '')
        # hotwater = req.get('hotwater', '')
        # aircon = req.get('aircon', '')
        # no_of_panels = req.get('no_of_panels', '')
        # installation_date = req.get('installation_date', '')
        # system_cost = req.get('system_cost', '')

        company = Company.objects.get(id=company_id)
        company__name = company.company_name.replace(' ', '')
        password = f'{company__name}@2022'
        req['password'] = password

        try:
            customer_already_exists = CustomUser.objects.get(email=email)
            return Response('Customer with email "{}" already exists'.format(email), 403)
        except CustomUser.DoesNotExist:
            # customer_details, job_details, customer_files = modify_input_for_multiple_files(password, company_id,
            # customer_crm_id, first_name, last_name, phone, email, street, city, postcode, state, country,
            # job_number, solar_panel, system_size, inverter, no_of_battery, hotwater, aircon, int(no_of_panels),
            # installation_date, system_cost)
            account_serializer = RegistrationSerializer(data=req)
            print('check valid and errors', account_serializer.is_valid(), account_serializer.errors)
            data = {}
            try:
                with transaction.atomic():
                    if account_serializer.is_valid():
                        user = account_serializer.save()
                        token = Token.objects.create(user=user)
                        if user:
                            # to send email faster
                            # EmailThread(send_email).start() # paused
                            # job_details['customer_id'] = user.id
                            req['customer_id'] = user.id
                            job_details_serializer = JobDetailsSerializer(data=req)
                            print(job_details_serializer.is_valid(), job_details_serializer.errors)
                            print('user added')
                            if job_details_serializer.is_valid():
                                company = Company.objects.get(id=company_id)
                                company.company_customers.add(user)
                                try:
                                    job = job_details_serializer.save()
                                    print('job', job)
                                    # sent = sendNmiRequest(user, company)
                                    # send notification to sales and reception => all users
                                except Exception as e:
                                    print('err', e)

                            print(job_details_serializer.errors)
                        else:
                            return Response('Jobs creation error', 201)

                        return Response('User created', 200)
                    else:
                        data = account_serializer.errors
                        print(data)
            except Exception as e:
                print('eee', e)
                return Response('Something went wrong', 409)
            return Response(data, 403)


class GetLoggedInUser(APIView):
    # print(APIView)
    authentication_classes = [InstallerTokenAuthentication]
    # permission_classes =  [IsAuthenticated]

    def get(self, request, pk):
        user = InstallerUser.objects.get(id=pk)
        token = InstallerToken.objects.get_or_create(user=user)
        # if users are installer or admin single company
        company = Company.objects.filter(company_users=user)
        all_company = Company.objects.filter(company_users=user).values()
        # print('company', company, 'all company', all_company)
        user_dict = (model_to_dict(user))
        user_dict.pop('last_login')
        user_dict.pop('date_joined')
        user_dict.pop('password')
        # print(token[0])
        user_dict['token'] = str(token[0])
        # user_dict['company_id'] = company.id
        # user_dict['company_name'] = company.company_name
        user_dict['company'] = all_company  # if user are installer of multiple company
        # user_dict['company_name'] = company.company_name
        admin = []
        for a in company:
            if user in a.company_admin.all():
                admin.append(a.company_name)
            user_dict['admin'] = admin

        return Response(user_dict, 200)


class AllRetailers(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ElectricityRetailers.objects.all()
    serializer_class = ElectricityRetailersSerializer


class EditDeleteAllRetailersView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ElectricityRetailers.objects.all()
    serializer_class = ElectricityRetailersSerializer


class AllRetailerForms(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs['retailer_id']
        queryset = FileType.objects.filter(retailer=retailer_id)
        return queryset
    serializer_class = FileTypeSerializer


class EditDeleteAllRetailersForms(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FileType.objects.all()
    serializer_class = FileTypeSerializer


# @receiver(post_save, sender=FileType)
# def save_email(sender, instance, created, **kwargs):
#     FileType.objects.filter(retailer=instance.retailer).update(to_email=instance.retailer.email)


from PyPDF2 import PdfReader, PdfWriter


class TestPdf(APIView):
    def post(self, request):
        reader = PdfReader("bcc.pdf")
        writer = PdfWriter()
        page = reader.pages[0]

        fields = reader.get_form_text_fields()
        # fields = {"key": "value", "key2": "value2"}
        # print(fields['First name'])
        # for i, j in fields.items():
        #     print(i, j)
        form_field = [i for i, j in fields.items()]
        print(form_field)
        # writer.add_page(page)
        # writer.update_page_form_field_values(
        #     writer.pages[0], {"First name": "pramesh"}
        # )
        # # fields = CustomUser._meta.get_fields()

        jd_remove = ['id', 'customer_id', 'back_panel', 'front_of_property', 'switch_board', 'installer_image',
                     'created_at', 'updated_at', 'finalized_by']
        cust_filter = ['id', 'first_name', 'last_name', 'email', 'phone']
        # inst_filter = ['id', 'first_name', 'last_name', 'email', 'phone']
        comp_filter = ['company_name', 'company_phone', 'company_creator']

        job_details_fields = [f.name for f in JobDetails._meta.fields if f.name not in jd_remove]
        customer_fields = [f.name for f in CustomUser._meta.fields if f.name in cust_filter]
        installer_fields = [f.name for f in InstallerUser._meta.fields if f.name in cust_filter]
        company_fields = [f.name for f in Company._meta.fields if f.name in comp_filter]

        print('j')
        print(job_details_fields)
        print('c')
        print(customer_fields)
        print('if')
        print(installer_fields)
        print('comp')
        print(company_fields)

        # write "output" to PyPDF2-output.pdf
        # with open("filled-out.pdf", "wb") as output_stream:
        #     writer.write(output_stream)
        return Response('Tested Pdf', 200)


def createBcfPDf():
    pass


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user)
        print(request.data)
        logout(request)
        return Response({'message': 'User Logged out'})


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        print('changepassowerddaf', request.data)
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response("Bad credentials!", 400)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response('Password updated successfully!', 200)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def sendNmiRequest(user, company):
    print('test email pass')
    password = company.company_name.replace(' ', '') + '@2022'
    encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)
    # link = "{}{}?token={}&&em={}".format('my_domain', 'nmi-form', token, encoded_pk) # production level
    link = "{}{}?token={}&&em={}".format(my_domain, 'nmi-form', token, encoded_pk)
    customer = user.first_name + ' ' + user.last_name
    if user.first_name == '':
        customer = user.email
    merge_data = {
        'customer': customer,
        'customer_email': user.email,
        'company_name': company.company_name,
        'link': link,  # change in production level
        'password': password,
    }
    # test-form-email/

    email_subject = "Email with form "
    email_html_body = render_to_string("Test_email_form.html", merge_data)
    from_email = company.company_creator.email
    to_email = [user.email]
    send_email = EmailMultiAlternatives(
        email_subject,
        email_html_body,
        from_email,
        to_email,

    )
    send_email.attach_alternative(email_html_body, "text/html")
    EmailThread(send_email).start()  # to send email faster

    return True


class UpdateNmiFromLink(APIView):

    def patch(self, request):
        print(request.data)
        data = request.data
        token = data.get("token")
        encoded_pk = data.get("em")
        nmi = data.get("nmi")

        if token is None or encoded_pk is None:
            return Response('Broken link!!!', 203)

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = CustomUser.objects.get(pk=pk)
        print(user)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response("The given link is expired. Contact your service provider.", 203)
        customer_job = JobDetails.objects.filter(customer_id=user).first()
        print(customer_job)
        customer_job.nmi = nmi
        customer_job.save()
        return Response('NMI updated', 200)
