from stegano import lsb
from io import BytesIO
#hiding data on image
def hide(c):
    secret = lsb.hide("images/2.png", str(c))
    arr = BytesIO()
    secret = secret.save(arr, format='PNG')
    arr.seek(0)
    return arr
#decoding data from the image 
def unhide(secret):
     return lsb.reveal(secret)
