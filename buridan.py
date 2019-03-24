#!/usr/bin/env python

from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
import sys, time

import threading

N_PANELS = 2
ROWS = 64
COLS = 64

class BuridanSetup():
    
    WIDTH = COLS * N_PANELS
    HEIGHT = ROWS
    
    def __init__(self):
        '''
        '''
        
        opts = RGBMatrixOptions()
        opts.gpio_slowdown = 4
        opts.disable_hardware_pulsing = True
        opts.rows = ROWS
        opts.cols = COLS
        opts.chain_length = N_PANELS #number of panels connected
        opts.hardware_mapping = 'adafruit-hat' # or 'regular'
        self.matrix = RGBMatrix(options = opts)
        
        self.image = Image.new('RGB', (self.WIDTH, self.HEIGHT), "black") 
        self.draw = ImageDraw.Draw(self.image)
        self.n = 0
        
        self.options = {}
        self.options['calculate_refresh_rate'] = False
        self.options['virtual_LED'] = False

        #option 1) A solid background
        self.options['solid_background'] = False
        self.options['bg_color'] = (0, 5, 0)
        
        #option 2) A single bar moving around in the background
        self.options['moving_back_bar'] = False
        #option 3) A grated background with multiple vertical bars moving in the background
        self.options['grated_background'] = True

        #Some settings for options 2 and 3
        self.options['bar_width'] = 10
        self.options['grating_color'] = (5, 0, 0)
        self.options['bg_speed'] = 5
        
        #option 4) Two flashing bars at an angle from buridan
        self.options['flashing_bars'] = False
        self.options['flashing_bars_positions'] = (60, 315)
        
                
        #The only foreground option for the moment, two buridan facing bars
        self.options['draw_buridan'] = True
        self.options['fg_color'] = (200, 0, 0)
        self.options['buridan_position'] = 25
        
        
        #these are used to calculate refresh rate
        self.rt = 0
        self._lastpaint = 0
        
        #Create, daemonize, and start thread
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                          
        thread.start()   

    def Clear(self, color="black"):
        '''
        '''
        self.draw.rectangle(((0, 0), (self.WIDTH, self.HEIGHT)), fill=color)
        
    def DrawVBar(self, pos, width, color):
        '''
        Draws a single vertical bar of width "width" at position "pos"
        Both parameters are in degree
        '''
        #convert measures from degrees to pixels
        x = int ( pos / 360.0 * self.WIDTH )
        w = int ( width / 360.0 * self.WIDTH )
        
        self.draw.rectangle(((x , 0), (x+w , self.HEIGHT)), fill=color)
        
    def DrawBuridanPattern(self, pos, color):
        '''
        Draws the simplest Buridan pattern
        '''
        
        self.DrawVBar(pos, 10, color)
        self.DrawVBar(pos+180, 10, color)
        

    def DrawGratedBackground(self, width = 5, speedHz = 1, color = "blue"):
        '''
        '''

        t = time.time()
   
        try:
            d = t - self._lp
        except:
            self._lp = 0
            d = t
        
        if d > (1.0 / speedHz):

            self._lp = t

            try:
                self._mx += 1
            except:
                self._mx = 0

        if self._mx >= width : self._mx = 0

        for i in range(0,360,width*2):
            self.DrawVBar(i+self._mx, width, color)

    def DrawFlashingBars (self, positions = (60, 315), width = 5, speedHz = 1, color = "blue"):
        '''
        '''
        t = time.time()
   
        try:
            d = t - self._lp
        except:
            self._lp = 0
            d = t
        
        if d > (1.0 / speedHz):

            self._lp = t

            try:
                self._visible = not self._visible
            except:
                self._visible = True
                
        if self._visible:
            
            for p in positions:
                self.DrawVBar(p, width, color)
                
    


    def DrawMovingBackBar (self, width = 5, speedHz = 1, color = "blue"):
        '''
        '''

        t = time.time()
   
        try:
            d = t - self._lp
        except:
            self._lp = 0
            d = t
        
        if d > (1.0 / speedHz):

            self._lp = t

            try:
                self._mx += 1
            except:
                self._mx = 0

        if self._mx >= 360 : self._mx = 0

        self.DrawVBar(self._mx, width, color)

    def run(self):
        '''
        '''
        
        offset_canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            
            if self.options['solid_background']:
                self.Clear(self.options['bg_color'])
                
            elif self.options['grated_background']:
                self.Clear(self.options['bg_color'])
                self.DrawGratedBackground(width = self.options['bar_width'], speedHz = self.options['bg_speed'], color=self.options['grating_color'])
                
            elif self.options['moving_back_bar']:
                self.Clear(self.options['bg_color'])
                self.DrawMovingBackBar(width = self.options['bar_width'], speedHz = self.options['bg_speed'], color=self.options['grating_color'])
                
            elif self.options['flashing_bars']:
                self.Clear(self.options['bg_color'])
                self.DrawFlashingBars(positions = self.options['flashing_bars_positions'] , width = self.options['bar_width'], speedHz = self.options['bg_speed'], color=self.options['grating_color'])
                
            if self.options['draw_buridan']:
                self.DrawBuridanPattern(self.options['buridan_position'], self.options['fg_color'])
                
                
            #draw
            if self.options['virtual_LED']: 
                self.image.show()
            else:
                #self.matrix.SetImage(self.image)

                offset_canvas.SetImage(self.image)
                offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
                
            time.sleep(0.01)

            
            if self.options['calculate_refresh_rate']:
                n = time.time()
                self.rt = n - self._lastpaint
                self._lastpaint = n
                
                print ("refresh rate: %s Hz" % (1 / self.rt), flush=True)


# Main function
if __name__ == "__main__":

    buridan_chamber = BuridanSetup()
    buridan_chamber.run()

    
