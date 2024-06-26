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
        allowed_extensions = ['jpg', 'jpeg']
        for img in images:
            try:     
                validator = FileExtensionValidator(allowed_extensions, message='Only  "jpeg or jpg" files are allowed.')
                validator(img)
                image_file = Images.objects.create(image=img)
                image_file.save()
                
                raise Exception("Something went wrong")
            
            except Exception as e:
                error_message = f"Error: {str(e)}"
                context = {
                 'error_message': error_message
                }
        return redirect('../success/')

    return render(request, 'index.html')

def success(request):
    image_files = Images.objects.all()

    
    file_counter=0
    file_num = len(image_files)
    
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
                    
    
                except FileNotFoundError:
                    return HttpResponseNotFound('File not found')
                
                except TypeError:
                    return HttpResponse("Metadata error")                
                
        except TypeError:
             return redirect('../success/')
        
        context = {
            'img_list': image_files
        }
            
        return render(request, 'uploads.html', context)     
                     
        
        
        
def download_image(request, image_id):
    image = get_object_or_404(Images, pk=image_id)
    file_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
    file_name = os.path.basename(image.image.name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

def delete(request):
    image_files = Images.objects.all()
    image_files.delete()
    return redirect('../upload/')

def filename_mask(image_file):
    file = image_file.split('\\')
    filesplit = image_file.split('/')
    filename = filesplit[2]
    return filename


