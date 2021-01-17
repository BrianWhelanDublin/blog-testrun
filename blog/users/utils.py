import cloudinary.uploader
import cloudinary.api


def save_picture(form_picture):
    response = cloudinary.uploader.upload(form_picture)
    print(response)
    url_start = "https://res.cloudinary.com/dmgevdb7w/"
    image_sizing = "image/upload/w_200,h_200,c_fill,g_face/"
    version = response["version"]
    public_id = response["public_id"]
    image_format = response["format"]

    return f"{url_start}{image_sizing}v{version}/{public_id}.{image_format}"
