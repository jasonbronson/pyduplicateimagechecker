import re, sys, myenv, glob, os, datetime, string, array, hashlib
import MySQLdb as my
from shutil import copyfile
from functools import partial

def md5sum(filename):
    if os.path.isfile(filename):
     with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
     return d.hexdigest()
    else:
     return ""


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


select_stmt = """
SELECT `id`, `filename`, `filepath`, `size`, `md5`, STR_TO_DATE(SUBSTRING(filetimestamp,1,11), '%Y-%m-%d') as filetimestamp, STR_TO_DATE(SUBSTRING(datetimeoriginal,1,11), '%Y:%m:%d') as datetimeoriginal, datetimedigitized, SUBSTRING(filename,-4) as extension from pictures where filename like '%.jpeg' or filename like '%.jpg' 
 or filename like '%.png'  or filename like '%.bmp'  or filename like '%.mov'  or filename like '%.MP4'  or filename like '%.avi'  
 or filename like '%.crw'  or filename like '%.THM'  or filename like '%.3gp' or filename like '%.tif'  or filename like '%.mpg' 
  or filename like '%.raf'  or filename like '%.mts'  or filename like '%.xmp'  or filename like '%.psd'  or filename like '%.gif'  
  or filename like '%.aae%'  and filepath not like '%/APriv'  and filepath not like '%/nsfw_model'
"""

cursor.execute(select_stmt)
md5List = {}

for item in cursor.fetchall():
    filename = item[2] + "/" + item[1]
    size = item[3]
    md5 = item[4]
    filetimestamp = item[5]
    datetimeoriginal = item[6]
    datetimedigitized = item[7]
    extension = item[8]
    if os.path.isfile(filename):
       if datetimeoriginal:
         year = datetimeoriginal.strftime("%Y")
         month = datetimeoriginal.strftime("%m")
         day = datetimeoriginal.strftime("%d")
       else:
         year = filetimestamp.strftime("%Y")
         month = filetimestamp.strftime("%m")
         day = filetimestamp.strftime("%d")

       newfile = month + "_" + day + "_" + md5 + extension.lower()
       newpath = "/mnt/usb/TEMP_PICS/" + year + "/"
       # do not copy duplicate files.
       if md5 not in md5List:
          md5List[md5] = md5
          #check if directory exists if not make it
          if not os.path.exists(newpath):
            os.makedirs(newpath)
          #check if the file already exists
          if not os.path.isfile(newpath + newfile):
            print("copying file " + filename)  
            # copy this file since it doesnt' exist
            copyfile(filename, newpath + newfile)
          else:
            print("checking existing md5 on file " + newpath + newfile) 
            # file exists so check it's md5 checksum
            md5sumExisting = md5sum(newpath + newfile)
            if md5sumExisting != md5:
              print("copying file md5 does not match " + filename)
              copyfile(filename, newpath + newfile) 
            else:
              print("md5 match skipping " + newpath + newfile)     
       else:
          print ("md5 exists " + md5)
       



     
db.close()
