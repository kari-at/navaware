from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from threading import Thread

from accessiphone import *

import datetime
from objc_util import NSBundle, ObjCClass, on_main_thread

####### IP ADDRESSES #######
# user IP (iPhone)
#u_ip = "172.20.10.1"
u_ip = "192.168.0.107"
u_port = 8000

# puppeteer IP (iPad)
#p_ip = "172.20.10.7"
p_ip = "192.168.0.102"
p_port = 2370

####### LANGUAGE #######
# language that is spoken
lang = 'en'

####### LOG #######
# print sent messages with timestamp
def print_sent_messages(address, args):
    t = datetime.datetime.now()
    print(t, " | SENT    | ", f"{address}: {args}")

# print received messages with timestamp
def print_received_messages(address, *args):
    t = datetime.datetime.now()
    print(t, " | RECEIVE | ", f"{address}: {args}")

####### SENDING MESSAGES #######
# ----- UI INPUT THAT TRIGGERS SENT MESSAGES----- #

def event_loop():
	print ('starting loop')
	
	def get_system_volume():
		return volume_view.subviews()[0].value()

	def set_system_volume(value):
		volume_view.subviews()[0].value = value

	def uButtonUp_input():
		osc_address = "/u/buttonUp"
		osc_value = True
		client.send_message(osc_address, osc_value)
		print_sent_messages(osc_address, osc_value)

	def uButtonDown_input():
		osc_address = "/u/buttonDown"
		osc_value = True
		client.send_message(osc_address, osc_value)
		print_sent_messages(osc_address, osc_value)

	NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
	MPVolumeView = ObjCClass('MPVolumeView')
	volume_view = MPVolumeView.new().autorelease()
	
	set_system_volume(0.5)
	default = get_system_volume()
	try:
		while True:
			if get_system_volume() > default:
				uButtonUp_input()
				set_system_volume(default)
			elif get_system_volume() < default:
				uButtonDown_input()
				set_system_volume(default)
	except KeyboardInterrupt:
		pass

####### RECEIVING MESSAGES #######
# ----- ACTIONS TRIGGERED BY RECEIVED MESSAGES VIA DISPATCHER ----- #
def pButtonVibe_output(address, *args):
    print_received_messages(address, *args)
    vibrate()
    
def pButtonEarcon1_output(address, *args):
    print_received_messages(address, *args)
    earcon('iOS_shortDoubleLow')

def pButtonText_output(address, *args):
		print_received_messages(address, *args)
		text2speech(args[0], lang)

if __name__ == "__main__":
		# console.clear()
		
		# ----- DISPATCHER ----- #
		# when a message is received, the dispatcher sends it to a function that acts on the message
		dispatcher = Dispatcher()
		
		dispatcher.map("/p/buttonVibe", pButtonVibe_output)
		dispatcher.map("/p/buttonText", pButtonText_output)
		dispatcher.map("/p/buttonEarcon1", pButtonEarcon1_output)
		
		# ----- EVENT THREAD ----- #
		event_thread = Thread(target=event_loop, args=())
		event_thread.start()
		
		# ----- DEFINING SERVER ----- #
		# address (on this device) you are listening to
		server = ThreadingOSCUDPServer((u_ip, u_port), dispatcher)
		print("Receiving on {}, port {}".format(u_ip, u_port))
		
		try:
			server.serve_forever()
		except KeyboardInterrupt:
			pass
