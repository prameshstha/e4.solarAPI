from apscheduler.schedulers.background import BackgroundScheduler

# from customer_portal.views import check_files_uploaded
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from DarwinSolar.utils import EmailThread
from accounts.models import CustomUser
from customer_portal.models import CustomerFiles, FileType


def check_files():
    checker = BackgroundScheduler()
    checker.add_job(check_files_uploaded, 'interval', seconds=15, id='files_001', replace_existing=True)
    checker.start()


def check_files_uploaded():
    print('checking in databasesss')
    # check if files are uploaded and send email for not uploaded files.
    qs = CustomUser.objects.all()
    files = FileType.objects.all()
    print(files.count())
    no_single_file = []
    no_complete_file = {}
    for a in qs:
        # print(a.id)
        f = CustomerFiles.objects.filter(customer_id=a.id)
        # print('user files', f.count())
        if f.count() == 0:
            # print('Please upload all necessary files')
            # send all data as email to upload all the files because zero files is uploaded
            no_single_file.append(a.email)

        elif f.count() == files.count():
            print('all files uploaded!!')
        else:
            no_files = []
            for y in files:
                # print(y.file_type)
                try:
                    x = CustomerFiles.objects.get(customer_id=a.id, file_type=y.id)
                    # print('exist', y.file_type)
                # if file doesn't exists
                except CustomerFiles.DoesNotExist:
                    # print('does not exist', y.file_type, 'of customer', a.first_name, a.last_name, a.email)
                    no_files.append(y.file_type)
            fullname = a.first_name + ' ' + (a.last_name if a.last_name is not None else '')
            email = a.email
            no_complete_file[email] = no_files

            # print('email sent', no_single_file, no_complete_file)
            # print('nofiles', no_complete_file)
            # send email from here
            customer = fullname
            merge_data = {
                'customer': customer,
                'customer_email': email,
                'fullname': fullname,
                'no_files': no_files,
                'no_complete_file': no_complete_file,
                'no_single_file': no_single_file,
            }

            email_subject = "File upload."
            email_html_body = render_to_string("file_upload_email.html", merge_data)
            from_email = "file-upload@darwinsolar.com.au"
            to_email = ['pramesh@darwinsolar.com.au']
            send_email = EmailMultiAlternatives(
                email_subject,
                email_html_body,
                from_email,
                to_email,

            )
            send_email.attach_alternative(email_html_body, "text/html")
            EmailThread(send_email).start()  # to send email faster
    merge_data = {
        'no_single_file': no_single_file,
    }
    send_email_for_all_not_uploaded(merge_data)
    print('email sent')

    # end send email code


def send_email_for_all_not_uploaded(data):
    email_subject = "File upload."
    email_html_body = render_to_string("all_list_not_uploaded.html", data)
    from_email = "file-upload@darwinsolar.com.au"
    to_email = ['pramesh@darwinsolar.com.au']
    send_email = EmailMultiAlternatives(
        email_subject,
        email_html_body,
        from_email,
        to_email,

    )
    send_email.attach_alternative(email_html_body, "text/html")
    EmailThread(send_email).start()  # to send email faster
