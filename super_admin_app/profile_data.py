from masterapp.models import tothiq_super_user,GeneralSettings
import os

def profile_detail(request):
    user_id = request.session.get('userid')
    if user_id:
        stng = GeneralSettings.objects.all()
        for i in stng:
            hlg = i.web_panel_header_logo
            wptx = i.webpanel_title_text
            crtx = i.webPanel_copyright_text
            web_panel_header_logo = i.web_panel_header_logo
            media_path = web_panel_header_logo.path if web_panel_header_logo else None
            web_panel_header_logo_file_exists = os.path.exists(media_path)
        a = tothiq_super_user.objects.filter(pk=user_id)
        for i in a:
            name = i.full_name
            email = i.email
            number = i.phone_number
            img = i.image
            media_path = img.path if img else None
            file_exists = os.path.exists(media_path)
            password = i.password
        
        data = {
            "name" :  name,
            "email" : email,
            "number" : number,
            "img" : img,
            "hlg":hlg,"wptx":wptx,"crtx":crtx,
        }
        footer_data = {
            "password" :password,
        }
        return {"profile_data":data, "footer_data": footer_data, "file_exists": file_exists, "web_panel_header_logo_file_exists": web_panel_header_logo_file_exists}
    else:
        return {"a":"a"}