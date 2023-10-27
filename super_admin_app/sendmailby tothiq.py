try:
    oldemail = Users.objects.filter(id=id)
    for i in oldemail:
        oldmail = i.email
    subject = " Account unblocked by TOTHIQ."
    message = 'Your account has been blocked by TOTHIQ. Please contact TOTHIQ Support at [Support Email Address] or [Support Phone Number] for assistance.'
    
    recipient = oldmail

    send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
except Exception as e:
    # Return an error response
    return HttpResponse(f'<h3>Error sending email: {e}</h3>')


try:
    oldemail = Users.objects.filter(id=id)
    for i in oldemail:
        oldmail = i.email
    subject = " Account Blocked by TOTHIQ."
    message = 'Your account has been blocked by TOTHIQ. Please contact TOTHIQ Support at [Support Email Address] or [Support Phone Number] for assistance.'
    
    recipient = oldmail

    send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
except Exception as e:
    # Return an error response
    return HttpResponse(f'<h3>Error sending email: {e}</h3>')