
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'RPI_Zero_1/pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging    
import time
import traceback
from lib.waveshare_OLED import OLED_1in3
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

class Display:
    def __init__(self):
        self.startup()
        self.image = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
        self.font = ImageFont.load_default()
    def startup(self):
        #Start the oled display
        self.disp = OLED_1in3.OLED_1in3()
        logging.info("\r STARTING UP")
        # Initialize library.
        self.disp.Init()
        logging.info("clear display")
        self.disp.clear()
        return self.disp
       
    def draw_rectangle(self, rect=[0,0,20,20], fill = 0, draw = None):
        if not draw:
            draw = ImageDraw.Draw(self.image)
        draw.rectangle(rect, fill)
        return draw
        
    def draw_line(self, line, fill = 0, draw = None):
        if not draw:
            draw = ImageDraw.Draw(self.image)
            
        draw.line(line, fill)
        return draw
    
    def draw_circle(self, location,radius, fill = 0, draw = None):
        if not draw:
            draw = ImageDraw.Draw(self.image)
        draw.ellipse([location[0]-radius,location[1]-radius,location[0]+radius,location[1]+radius],fill)
    
    def show_text(self, location, text, draw = None):
        if not draw:
            draw = ImageDraw.Draw(self.image)
        draw.text(location, text, font = ImageFont.load_default(), fill = 0)
        
    def get_blank_image(self):
        return Image.new('1', (self.disp.width, self.disp.height), "WHITE")
        
    def refresh_image(self):
        self.disp.ShowImage(self.disp.getbuffer(self.image.rotate(180)))
        
    def clear_screen(self):
        self.disp.clear()
        
    
    
   
'''
disp = Display()
disp.draw_rectangle([0,20,20,40])
disp.refresh_image()
time.sleep(3)
'''

''' 

image1 = Image.new('1', (disp.width, disp.height), "WHITE")
draw = ImageDraw.Draw(image1)
font1 = ImageFont.load_default()
font2 = ImageFont.load_default()
logging.info ("***draw line")
draw.line([(0,0),(127,0)], fill = 0)
draw.line([(0,0),(0,63)], fill = 0)
draw.line([(0,63),(127,63)], fill = 0)
draw.line([(127,0),(127,63)], fill = 0)
logging.info ("***draw text")
draw.text((20,0), '[][][][][]]', font = font1, fill = 0)
draw.text((20,24), u'Chinese stuff ', font = font2, fill = 0)

image1 = image1.rotate(180) 
disp.ShowImage(disp.getbuffer(image1))
time.sleep(3)
draw2 = ImageDraw.Draw(image1)
draw2.line([(0,25),(127,25)], fill = 0)
image1.putpixel((5,23),0)
image1.putpixel((6,24),0)
disp.ShowImage(disp.getbuffer(image1))
time.sleep(3)

logging.info ("***draw image")
Himage2 = Image.new('1', (disp.width, disp.height), 255)  # 255: clear the frame
bmp = Image.open(os.path.join(picdir, '1in3.bmp'))
Himage2.paste(bmp, (0,0))
Himage2=Himage2.rotate(180) 


disp.ShowImage(disp.getbuffer(Himage2)) 

time.sleep(6)    
'''


#disp.clear_screen()
