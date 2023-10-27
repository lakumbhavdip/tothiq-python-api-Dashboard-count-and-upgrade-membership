from masterapp.models import languages_label
from tothiq.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import requests
import json

def get_label_by_code_and_language(label_code, language='English'):
    try:
        label = languages_label.objects.get(code=label_code)
        if language == 'Arabic':
            return label.arabic
        else:
            return label.english
    except languages_label.DoesNotExist:
        return f'Label with code {label_code} not found'
    

# for deefault emial set
def send_email_test_backup(subject, body, recipient_email):
    message = body
    recipient = recipient_email
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,  # Use your email host user here
        [recipient],
        fail_silently=False,
        html_message=body  # Use 'html_message' to send an HTML email
    )
    
    
# for custom email for brevo
def send_email_test(subject, body, recipient_email):
    url = "https://api.brevo.com/v3/smtp/email"
    payload = json.dumps({
      "sender": {
        "name": "Tothiq",
        "email": "noreply@tothiq.com"
      },
      "to": [
        {
          "email": recipient_email,
        }
      ],
      "subject": subject,
      "htmlContent": body
    })
    headers = {
      'api-key': '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',
      'Content-Type': 'application/json',
      'Cookie': '__cf_bm=h7OQ6u9m7RwyhXYuExSxVav6OBOnPpA.7wp1an7eK1E-1697095193-0-AblXmoKDOzzCLnHm7evpNu6NdhPkKc5JhihI0jiBk3khh1W8z0stLMgaoy6G5dxUu49ymUsJLreY9dfaidyj5cc='
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return "Email sent successfully"
    else:
        return "Email sending failed"