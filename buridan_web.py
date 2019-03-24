#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import cgi

import threading

from buridan import BuridanSetup

HTTP_PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class webHandler(BaseHTTPRequestHandler):
    
    hasBuridan = False
    
    def linkBuridan(self):
        '''
        '''
        self.buridan_chamber = BuridanSetup()
        self.hasBuridan = True
        #buridan_chamber.run()

    
    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read(), "utf8"))
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


    def elaborateInput(self):
        '''
        '''
        
        #Getting URL parameters
        self.form = cgi.FieldStorage()

        #actions
        bg_choice = self.form.getvalue("background_choice", "")
        fg_choice = self.form.getvalue("foreground_choice", "")
 

    #Handler for the POST requests
    def do_POST(self):
        '''
        '''
        
    #if self.path=="/send":
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
        })

        fv = {}
        fv['bg_choice'] = form.getvalue("background_choice", "")
        
        fv['fill_bg_red'] = form.getvalue("fill_bg_red", "")
        fv['fill_bg_green'] = form.getvalue("fill_bg_green", "")
        fv['fill_bg_blue'] = form.getvalue("fill_bg_blue", "")

        fv['moving_vbars_size'] = form.getvalue("moving_vbars_size", "")
        fv['moving_vbars_speed'] = form.getvalue("moving_vbars_speed", "")
        fv['moving_vbars_bg_red'] = form.getvalue("moving_vbars_bg_red", "")
        fv['moving_vbars_bg_green'] = form.getvalue("moving_vbars_bg_green", "")
        fv['moving_vbars_bg_blue'] = form.getvalue("moving_vbars_bg_blue", "")
        fv['moving_vbars_fg_red'] = form.getvalue("moving_vbars_fg_red", "")
        fv['moving_vbars_fg_green'] = form.getvalue("moving_vbars_fg_green", "")
        fv['moving_vbars_fg_blue'] = form.getvalue("moving_vbars_fg_blue", "")

        fv['moving_vbar_size'] = form.getvalue("moving_vbar_size", "")
        fv['moving_vbar_speed'] = form.getvalue("moving_vbar_speed", "")
        fv['moving_vbar_bg_red'] = form.getvalue("moving_vbar_bg_red", "")
        fv['moving_vbar_bg_green'] = form.getvalue("moving_vbar_bg_green", "")
        fv['moving_vbar_bg_blue'] = form.getvalue("moving_vbar_bg_blue", "")
        fv['moving_vbar_fg_red'] = form.getvalue("moving_vbar_fg_red", "")
        fv['moving_vbar_fg_green'] = form.getvalue("moving_vbar_fg_green", "")
        fv['moving_vbar_fg_blue'] = form.getvalue("moving_vbar_fg_blue", "")

        fv['fg_choice'] = form.getvalue("foreground_choice", "")
        
        fv['buridan_bar_size'] = form.getvalue("buridan_bar_size", "")
        fv['buridan_fg_red'] = form.getvalue("buridan_fg_red", "")
        fv['buridan_fg_green'] = form.getvalue("buridan_fg_green", "")
        fv['buridan_fg_blue'] = form.getvalue("buridan_fg_blue", "")


        if not self.hasBuridan:
            self.linkBuridan()

        self.buridan_chamber.options['solid_background'] = ( fv['bg_choice'] == "fill_bg" )
        self.buridan_chamber.options['grated_background'] = ( fv['bg_choice'] == "moving_vbars" )
        self.buridan_chamber.options['moving_back_bar'] = ( fv['bg_choice'] == "moving_vbar" )
        
        if self.buridan_chamber.options['solid_background']:
            self.buridan_chamber.options['bg_color'] = (int(fv['fill_bg_red']), int(fv['fill_bg_green']), int(fv['fill_bg_blue']))

        if self.buridan_chamber.options['grated_background']:
            self.buridan_chamber.options['bg_color'] = (int(fv['moving_vbars_bg_red']), int(fv['moving_vbars_bg_green']), int(fv['moving_vbars_bg_blue']))
            self.buridan_chamber.options['grating_color'] = (int(fv['moving_vbars_fg_red']), int(fv['moving_vbars_fg_green']), int(fv['moving_vbars_fg_blue']))   

        if self.buridan_chamber.options['moving_back_bar']:
            self.buridan_chamber.options['bg_color'] = (int(fv['moving_vbar_bg_red']), int(fv['moving_vbar_bg_green']), int(fv['moving_vbar_bg_blue']))
            self.buridan_chamber.options['grating_color'] = (int(fv['moving_vbar_fg_red']), int(fv['moving_vbar_fg_green']), int(fv['moving_vbar_fg_blue']))   
            

        self.buridan_chamber.options['draw_buridan'] = ( fv['fg_choice'] == "buridan" )        
        self.buridan_chamber.options['fg_color'] = (int(fv['buridan_fg_red']), int(fv['buridan_fg_green']), int(fv['buridan_fg_blue']))

        self.buridan_chamber.options['calculate_refresh_rate'] = False


# Main function
if __name__ == "__main__":

    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', HTTP_PORT_NUMBER), webHandler)
        print ('Started httpserver on port ' , HTTP_PORT_NUMBER)
        
        #Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()
    
