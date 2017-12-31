import re, sys, myenv, glob, os, hashlib, piexif, codecs, datetime
from PIL import Image
import MySQLdb as my
from functools import partial

db = my.connect(host=myenv.MYSQL_IP,
user=myenv.MYSQL_USERNAME,
passwd=myenv.MYSQL_PASSWORD,
db="pictures"
)

db.set_character_set('utf8')

cursor = db.cursor()

cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')


def md5sum(filename):
    if os.path.isfile(filename):
     with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
     return d.hexdigest()
    else:
     return ""


for filename in glob.iglob('/backup/Pictures/**/*', recursive=True):
    if os.path.isfile(filename):
     statinfo = os.stat(filename)
     md5hash = md5sum(filename)
     directory = os.path.dirname(os.path.abspath(filename))
     datetimedigitized = ""
     datetimeoriginal = ""

     filetimestamp = datetime.datetime.fromtimestamp(statinfo.st_mtime)
     if not filetimestamp:
      filetimestamp = datetime.datetime.fromtimestamp(statinfo.st_ctime)

     if filename.lower().endswith('jpg'):
        try:
         im = Image.open(filename)
         exif_dict = piexif.load(im.info["exif"])
         for tag in exif_dict["Exif"]:
             #print(piexif.TAGS["Exif"][tag]["name"])
             if piexif.TAGS["Exif"][tag]["name"] == "DateTimeDigitized":
               datetimedigitized = exif_dict["Exif"][tag].decode('UTF-8')
             if piexif.TAGS["Exif"][tag]["name"] == "DateTimeOriginal":   
               datetimeoriginal = exif_dict["Exif"][tag].decode('UTF-8')
             #print(piexif.TAGS["Exif"][tag]["name"], exif_dict["Exif"][tag])
        except:
         print("Exception reading exif on image: " + filename) 
     

     filename = os.path.basename(filename)
     print(filename)
     
     data = (filename, directory, statinfo.st_size, md5hash, datetimedigitized, datetimeoriginal, filetimestamp)
     number_of_rows = cursor.execute("INSERT INTO `pictures` (`filename`, `filepath`, `size`, `md5`, `datetimedigitized`, `datetimeoriginal`, `filetimestamp`) VALUES (%s, %s, %s, %s, %s, %s, %s)", data )
     db.commit()

db.close()



