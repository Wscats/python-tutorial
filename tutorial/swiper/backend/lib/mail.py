from django.core.mail import send_mail, send_mass_mail, mail_admins

from worker import call_by_worker


async_send_mail = call_by_worker(send_mail)
async_send_mass_mail = call_by_worker(send_mass_mail)
async_mail_admins = call_by_worker(mail_admins)
