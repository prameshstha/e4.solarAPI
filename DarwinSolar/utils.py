# to send email faster
import os
import threading

from DarwinSolar.settings import DEBUG, O365_Email


class EmailThread(threading.Thread):
    def __init__(self, send_email):
        self.send_email = send_email
        threading.Thread.__init__(self)

    def run(self):
        # self.send_email.send(fail_silently=False)
        self.send_email.send()


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


# def email_O365(to_email, email_subject, email_html_body, from_email='admin@darwinsolar.com.au',
# email_attachment=None, cc_email=None):
def email_O365(**kwargs):
    to_email = kwargs.get('to_email', '')
    email_subject = kwargs.get('email_subject', '')
    email_html_body = kwargs.get('email_html_body', '')
    from_email = kwargs.get('from_email', '')
    email_attachment = kwargs.get('email_attachment', '')
    cc_email = kwargs.get('cc_email', '')

    send_email = O365_Email.new_message(resource='admin@darwinsolar.com.au')
    send_email.to.add(to_email)
    send_email.cc.add(cc_email)
    send_email.subject = email_subject
    send_email.body = email_html_body
    if email_attachment:
        send_email.attachments.add(email_attachment)
    EmailThread(send_email).start()


# my_domain = 'https://e4.solar/'
# my_domain = 'http://localhost:3000/'

if DEBUG:
    my_domain = 'http://localhost:3000/'
else:
    my_domain = 'https://e4.solar/'

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