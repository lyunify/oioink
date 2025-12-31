import os
import random

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont
from .tokens import account_activation_token


# Send activation email
def send_activation_email(request, user):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    current_site = get_current_site(request)
    email_subject = 'Activate your account.'
    email_body = render_to_string('accounts/activate.html', {
        'user': user,
        'protocol': protocol,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email_from = settings.EMAIL_FROM_USER
    email_to = [user.email]
    email = EmailMessage(email_subject, email_body, email_from, email_to)
    email.send(fail_silently=False)
    return


# Generate profile image
def generate_profile_image(user, uid):
    username = user.username
    bg_color = "#"+''.join([random.choice('6789ABCDEF')
                           for i in range(6)])
    fg_color = "#"+''.join([random.choice('0123456789')
                           for i in range(6)])
    image_width = 80  # 80 pixels wide
    image_height = 80  # 80 pixels high
    # img = Image.new('RGB', (image_width, image_height), color=(51, 144, 255))
    img = Image.new('RGB', (image_width, image_height), color=bg_color)
    # create the canvas
    canvas = ImageDraw.Draw(img)
    # use a truetype font
    font_type = 'arial.ttf'
    font_size = 48  # about half of text box
    font = ImageFont.truetype(font_type, font_size)
    # use text size
    letter = username[0]
    text_width, text_height = canvas.textsize(letter, font=font)
    # adjust x, y positions
    x_offset, y_offset = font.getoffset(letter)
    text_width += x_offset
    text_height += y_offset
    x_pos = int((image_width - text_width) / 2)
    y_pos = int((image_height - text_height) / 2)
    # generate text
    canvas.text((x_pos, y_pos), letter, font=font, fill=fg_color)
    # construct url and save img
    img_url = 'profile_image.png'
    img.save(img_url)
    return img_url


# Resize profile image
def resize_profile_image(profile):
    img = Image.open(profile.profile_image.url)
    if img.height > 80 or img.width > 80:
        output_size = (80, 80)
        img.thumbnail(output_size)
        img.save(profile.profile_image.url)
