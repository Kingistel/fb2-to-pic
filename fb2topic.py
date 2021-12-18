import sys, os, shutil, io
import base64
from PIL import Image
from lxml import etree

fal = sys.argv[1]
stage1=False
word = '" content-type="'
altword='<binary content-type="'
wordend = '</binary>'
os.chdir(fal)
try: shutil.rmtree('pic')
except: pass
os.mkdir('pic')

def openfile(file):
    try:
        with open(file, encoding='utf8') as fb2:
            fb2topicone(file, fb2)
    except: 
        with open(file, encoding='windows-1251') as fb2:
            fb2topicone(file, fb2)

def fb2topicone(file, fb2):
    try:
        xml_fb2 = etree.XML(fb2.read().encode())
        binaries = xml_fb2.xpath("//*[local-name()='binary']")
        for i, binary in enumerate(binaries, 1):
            content_type = binary.attrib['content-type']
            short_content_type = content_type.split('/')[-1]
            im_id = binary.attrib['id']
            im_data = base64.b64decode(binary.text.encode())
            with open(f"./pic/{file}.png", "wb") as fh:
                fh.write(im_data)
                
            print(file+": OK")
            break
    except:
        temp=None
        fh=None
        try:
            for i in fb2:
                if (altword in i):
                    temp = i[30:]
                    aa=list(temp)
                    while True:
                        if aa[0]!='>': aa.pop(0)
                        elif aa[0]=='>': aa.pop(0); break
                    temp=''.join(aa)
                    temp = temp[:-23]
            temp=temp.encode("windows-1251")
            with open(f"./pic/{file}.png", "wb") as fh:
                fh.write(base64.decodebytes(temp))
            print(file + ": OK")
        except: print(file+" ERROR")
        
for file in os.listdir(fal):
    if file.endswith(".fb2"):
        openfile(file)
        