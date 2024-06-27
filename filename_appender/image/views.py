from django.forms import ValidationError
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.validators import FileExtensionValidator
from .models import Images
from PIL import Image 
from django.shortcuts import render, redirect, get_object_or_404
import os
from PIL.ExifTags import TAGS
from django.conf import settings


def upload_images(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        global prev_files
        prev_files = len(images)
        allowed_extensions = ['jpg', 'jpeg']
        with_exifdata = True
        for img in images:
            try:
                validator = FileExtensionValidator(allowed_extensions, message='Only  "jpeg or jpg" files are allowed.')
                validator(img)

                with_exifdata = has_exif_data(img)

                if with_exifdata:
                    image_file = Images(image=img)
                    image_file.save()

                else:
                    continue

            except (AttributeError, KeyError, IndexError, IOError, ValueError, FileNotFoundError, ValidationError) as e:
                error_message = str(e)
                return render(request, 'index.html', {'response_message': error_message})
            
        return redirect('../success/')

    return render(request, 'index.html')


def success(request):
    image_files = Images.objects.all()
    file_num = len(image_files)

    if request.session.get('action_processed', False):
        context = {
        'img_list': image_files,
        'unconverted': prev_files - file_num
         }
        return render(request, 'uploads.html', context) 
        
    
    if file_num != 0:
        try:
            for image in image_files:
                old_filename = os.path.basename(image.image.name)
                path = os.path.join(settings.MEDIA_ROOT, old_filename)
                opened_image = Image.open(path)
                exifdata = opened_image.getexif()


                x_id = 0x011a
                y_id = 0x011B
                x_resolution = exifdata.get(x_id)
                y_resolution = exifdata.get(y_id)

                # get width and height 
                width = opened_image.width 
                height = opened_image.height 

         
                # inches
                dimension_x = round(float(width/x_resolution), 2)
                dimension_y = round(float(height/y_resolution), 2)

                # ft
                dimension_fx = round(float(dimension_x/12), 2)
                dimension_fy = round(float(dimension_y/12), 2)

                #New Filename concantenating dimension
                dimension_resutl = f" ({dimension_x} in x {dimension_y} in)({dimension_fx} ft x {dimension_fy} ft)"
                lastDotIndex = path.index('.')
                new_file_name = path[0:lastDotIndex] + dimension_resutl + path[lastDotIndex:]

                opened_image.close()

                new_file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)

                try:
                    os.rename(path, new_file_path)
                    image.image.name = new_file_name
                    image.save()

                except (AttributeError, KeyError, IndexError, IOError, ValueError, FileNotFoundError, ValidationError):
                    value_error = "Something's wrong with the files"
                    return render(request, 'index.html', {'response_message': value_error})           
                
        except (AttributeError, KeyError, IndexError, IOError, ValueError):
            value_error = "Value error."
            return render(request, 'index.html', {'response_message': value_error})
    if file_num == 0:
        request.session.flush()
        return redirect('../upload')  

    context = {
        'img_list': image_files,
        'unconverted': prev_files - file_num
    }

    request.session['action_processed'] = True
        
    return render(request, 'uploads.html', context)     
             
        
def download_image(request, image_id):
    image = get_object_or_404(Images, pk=image_id)
    file_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
    file_name = os.path.basename(image.image.name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


def reset_image(request):
    path = settings.MEDIA_ROOT
    delete_images(path)
    image_files = Images.objects.all()
    image_files.delete()
    request.session.flush()
    return redirect('../upload/')


def has_exif_data(image_file):
    try:
        img = Image.open(image_file)
        exifdata =  img.getexif() 
        x_id = 0x011a
        if exifdata:
            for tagid, value in exifdata.items():
                if tagid == x_id:
                    return True
            return False
        else:
            return False
    except (AttributeError, KeyError, IndexError, IOError, ValueError, FileNotFoundError):
        return False

def delete_images(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            os.remove(filepath)
