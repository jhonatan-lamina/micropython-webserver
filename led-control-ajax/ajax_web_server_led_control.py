'''
 * LED control through a Web server using Ajax
 *
 * Name = Ajax Web Server - Led Control
 * Version = 1.0.0
 * Update Date = 10/10/2021
 * Author = Jhonatan Lamiña
 * e-mail = contacto@jhonatanlamina.com
 * Web = www.jhonatanlamina.com
 *
 * Copyright (c) Jhonatan Lamiña - All rights reserved
'''

from machine import Pin, reset
import network
import socket
import time

#Disable debug output
import esp
esp.osdebug(None)

#It reclaims the memory occupied by objects that are not necessary for the program
import gc
gc.collect()

#WiFi Connection
#Replace the SSID and KEY data with those of your Wi-Fi network
ssid = 'WiFi NETWORK'
key = '*wifi-network*'
indicator = Pin(0, Pin.OUT)
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.active(True)
    wlan.connect(ssid, key)
    print('Connecting to: %s' % ssid)
    timeout = time.ticks_ms()
    while not wlan.isconnected():
        indicator.on()
        time.sleep(0.15)
        indicator.off()
        time.sleep(0.15)
        if (time.ticks_diff (time.ticks_ms(), timeout) > 10000):
            break
    if wlan.isconnected():
        indicator.on()
        print('Successful connection to: %s' % ssid)
        print('IP: %s\nSUBNET: %s\nGATEWAY: %s\nDNS: %s' % wlan.ifconfig()[0:4])
    else:
        indicator.off()
        wlan.active(False)
        print('Failed to connect to: %s' % ssid)
else:
    indicator.on()
    print('Connected\nIP: %s\nSUBNET: %s\nGATEWAY: %s\nDNS: %s' % wlan.ifconfig()[0:4])
    
#Output Pin
output1 = Pin(16, Pin.OUT)
output2 = Pin(5, Pin.OUT)

#Web Page
def web_page():
    html = """
<!DOCTYPE html>
<html>
<head>
	<title>MicroPython Web Server</title>
    <link rel="shortcut icon" href="https://th.bing.com/th/id/OIP.A8WOluXYcZZ6j5M72poa4wHaEL?pid=ImgDet&rs=1">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
    	const xhttp = new XMLHttpRequest();
		function on1() {
			console.log("ON1");
			xhttp.open("GET", "/?control1=on");
			xhttp.send();
		}
		function off1() {
			console.log("OFF1");
			xhttp.open("GET", "/?control1=off");
			xhttp.send();
		}
		function on2() {
			console.log("ON2");
			xhttp.open("GET", "/?control2=on");
			xhttp.send();
		}
		function off2() {
			console.log("OFF2");
			xhttp.open("GET", "/?control2=off");
			xhttp.send();
		}
    </script>   
    <style>
	    *{
		padding: 0px; margin: 0px;
		}
		.home{
			padding: 0px 0px 10px 0px; background-color: #ffffff;
		}
		.nav{
			box-sizing: border-box; display: inline-block;
			padding: 10px 0px 10px 0px; background-color:#063d6d;
			width: 100%; height: auto;
		}
		.control{
			box-sizing: border-box; display: inline-block;
			padding: 0px 0px 15px 0px; background-color: #cccccc;
			border: 4px solid #063d6d; border-radius: 20px;
			width: auto; height: auto; margin: 30px;
		}
		.myline {
		  border: 2px solid #063d6d;
		}
		#t1{
			font-family: Helvetica; font-weight: bold;
			text-align: center; font-size: 50px; color: white;
		}
		#t2{
			font-family: Helvetica; font-weight: bold;
			text-align: center; font-size: 20px; color: white;
		}
		#imag{
			width: 200px; height: 200px; padding: 25px;
		}
		#on{
			border: 4px solid green; border-radius: 20px;
			background-color:white; color: green;
			font-weight: bold; font-size: 20px;
			width: 150px; height: 50px; cursor:pointer; 
		}
		#off{
			border: 4px solid red; border-radius: 20px;
			background-color:white; color: red;
			font-weight: bold; font-size: 20px;
			width: 150px; height: 50px; cursor:pointer; 
		}
  	</style>
</head>
<body>
	<div class='nav'>
		<h1 id='t1'>MicroPython Web Server</h1>
		<p id='t2'>For more information visit <a id='t2' href="https://jhonatanlamina.com" target="_blank" title="Go to www.jhonatanlamina.com">www.jhonatanlamina.com</a></p>
	</div>
	<div class="home">
		<center>
		<div class="control">
			<img id="imag" src="https://gifimage.net/wp-content/uploads/2017/11/foco-idea-gif-12.gif" alt="imagen">
			<hr class="myline"><br /> &ensp;
			<button id='on' type="button" onclick="on1();">ON</button> &ensp;
			<button id='off' type="button" onclick="off1();">OFF</button> &ensp;
		</div>
		<div class="control">
			<img id="imag" src="https://gifimage.net/wp-content/uploads/2017/11/foco-idea-gif-12.gif" alt="imagen">
			<hr class="myline"><br /> &ensp;
			<button id='on' type="button" onclick="on2();">ON</button> &ensp;
			<button id='off' type="button" onclick="off2();">OFF</button> &ensp;
		</div>
		</center>
	</div>
</body>
</html>
"""
    return html
try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 80))
    tcp_socket.listen(5)
    time.sleep(1)
    print('Successful socket configuration')
except OSError as e:
    print('Failed to socket configuration. Rebooting...')
    time.sleep(3)
    reset()

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = tcp_socket.accept()
        conn.settimeout(3.0)
        print('New connection from: %s' % str(addr[0]))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        #print('Request:  %s' % request)
        if request.find('/?control1=on') == 6:
            print('OUTPUT1: ON')
            output1.value(1)
        if request.find('/?control1=off') == 6:
            print('OUTPUT1: OFF')
            output1.value(0)
        if request.find('/?control2=on') == 6:
            print('OUTPUT2: ON')
            output2.value(1)
        if request.find('/?control2=off') == 6:
            print('OUTPUT2: OFF')
            output2.value(0)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(web_page())
        conn.close()
    except OSError as e:
        conn.close()
        #print('Connection Closed')
    time.sleep(0.1)