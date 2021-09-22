from machine import Pin
import wireless
import socket

#Disable debug output
import esp
esp.osdebug(None)

#It reclaims the memory occupied by objects that are not necessary for the program
import gc
gc.collect()

#Configuración inicial de WiFi
wireless.wifi('WiFi NETWORK', '*wifi-network*', 0)

#Output Pins
output_1 = Pin(5, Pin.OUT)
output_2 = Pin(16, Pin.OUT)

#Web Page
estate_1 = "OFF"
estate_2 = "OFF"
def web_page():  
    html = """
<!DOCTYPE html>
<html>
<head>
	<title>MicroPython Web Server</title>
    <link rel="shortcut icon" href="https://th.bing.com/th/id/OIP.A8WOluXYcZZ6j5M72poa4wHaEL?pid=ImgDet&rs=1">
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
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
		#t3{
			font-family: Helvetica; font-weight: bold;
			font-size: 30px; color: #063d6d;
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
		<h1 id='t1'>MicroPyton Web Server</h1>
		<p id='t2'>For more information visit <a id='t2' href="https://jhonatanlamina.com" target="_blank" title="Go to www.jhonatanlamina.com">www.jhonatanlamina.com</a></p>
	</div>
	<div class="home">
		<center>
		<div class="control">
			<img id="imag" src="https://th.bing.com/th/id/R.60f8839756f7da82618cf1cd38be8778?rik=vFw%2bIj7K0BILiA&pid=ImgRaw&r=0" alt="imagen">
			<hr class="myline">
			<h1 id='t3'>Estate:</h1><h1>""" + estate_1 + """</h1>
			<hr class="myline"><br /> &ensp;
			<button id='on' type="button" onmouseover="this.style.background='green'; this.style.color='white'" onmouseout="this.style.background='white'; this.style.color='green'" onclick="window.location.href='/?control-1=on'">ON</button> &ensp;
			<button id='off' type="button" onmouseover="this.style.background='red'; this.style.color='white'" onmouseout="this.style.background='white'; this.style.color='red'" onclick="window.location.href='/?control-1=off'">OFF</button> &ensp;
		</div>
		<div class="control">
			<img id="imag" src="https://th.bing.com/th/id/R.60f8839756f7da82618cf1cd38be8778?rik=vFw%2bIj7K0BILiA&pid=ImgRaw&r=0" alt="imagen">
			<hr class="myline">
			<h1 id='t3'>Estate:</h1><h1>""" + estate_2 + """</h1>
			<hr class="myline"><br /> &ensp;
			<button id='on' type="button" onmouseover="this.style.background='green'; this.style.color='white'" onmouseout="this.style.background='white'; this.style.color='green'" onclick="window.location.href='/?control-2=on'">ON</button> &ensp;
			<button id='off' type="button" onmouseover="this.style.background='red'; this.style.color='white'" onmouseout="this.style.background='white'; this.style.color='red'" onclick="window.location.href='/?control-2=off'">OFF</button> &ensp;
		</div>
		</center>
	</div>
</body>
</html>
"""
    return html
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('', 80))
tcp_socket.listen(5)
while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = tcp_socket.accept()
        conn.settimeout(3.0)
        print('New connection from: %s' %str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Request: %s' %request)
        if request.find('/?control-1=on') == 6:
            print('Output 1: ON')
            estate_1 = "ON"
            output_1.on()
        if request.find('/?control-1=off') == 6:
            print('Output 1: OFF')
            estate_1 = "OFF"
            output_1.off()
        if request.find('/?control-2=on') == 6:
            print('Output 2: ON')
            estate_2 = "ON"
            output_2.on()
        if request.find('/?control-2=off') == 6:
            print('Output 2: OFF')
            estate_2 = "OFF"
            output_2.off()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(web_page())
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')