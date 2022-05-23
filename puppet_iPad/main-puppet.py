from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

import datetime
import numpy as np
import ui
import csv
import sound

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
# language of sent messages
lang = 'en'

####### LOG #######
# print sent messages with timestamp
def print_sent_messages(address, args):
    t = datetime.datetime.now()
    print(t, " | SENT    | ", f"{address}: {args}")
    v['console'].text = str(t) + "  | SENT    |  " + f"\t {address} -> {args}"

# print received messages with timestamp
def print_received_messages(address, *args):
    t = datetime.datetime.now()
    print(t, " | RECEIVE | ", f"{address}: {args}")
    v['console'].text = str(t) + "  | RECEIVE |  " + f"\t {address} -> {args}"

# print recorded messages with timestamp
def print_recorded_messages(address, *args):
    t = datetime.datetime.now()
    print(t, " | RECORD  | ", f"{address}: {args}")
    v['console'].text = str(t) + "  | RECEIVE |  " + f"\t {address} -> {args}"

####### SENDING MESSAGES #######
# ----- UI INPUT THAT TRIGGERS SENT MESSAGES ----- #

def pButtonVibe_input(sender):
    osc_address = "/p/buttonVibe"
    osc_value = True
    client.send_message(osc_address, osc_value)
    print_sent_messages(osc_address, osc_value)

def pButtonEarcon1_input(sender):
    osc_address = "/p/buttonEarcon1"
    osc_value = True
    client.send_message(osc_address, osc_value)
    print_sent_messages(osc_address, osc_value)
    
def pButtonText_input(sender):
    osc_address = "/p/buttonText"
    osc_value = v['instruction'].text
    client.send_message(osc_address, osc_value)
    print_sent_messages(osc_address, osc_value)
    
####### RECORDING MESSAGES #######
# ----- UI INPUT THAT TRIGGERS ANNOTATIONS----- #

# log annotations by appending to a list
def annotate(mode, value, list):
		t = datetime.datetime.now()
		if value == True:
				list.append([mode, 'start', len(list)//2, f"{t}"])
		elif value == False:
				list.append([mode, 'end', (len(list)-1)//2, f"{t}"])

def pSwitchWalk_annotate(sender):
		log_label = "/a/switchWalk" #this osc address is not actually sent
		log_value = sender.value
		print_recorded_messages(log_label, log_value)
		annotate('walk', log_value, annotateWalk)

def pSwitchExplore_annotate(sender):
		log_label = "/a/switchExplore" #this osc address is not actually sent
		log_value = sender.value
		print_recorded_messages(log_label, log_value)
		annotate('explore', log_value, annotateExplore)

####### RECEIVING MESSAGES #######
# ----- ACTIONS TRIGGERED BY RECEIVED MESSAGES VIA DISPATCHER ----- #
def uButtonUp_output(address, *args):
    print_received_messages(address, *args)
    sound.play_effect('/System/Library/Audio/UISounds/short_double_high.caf')
    v['switchUp'].value = True
    
def uButtonDown_output(address, *args):
    print_received_messages(address, *args)
    sound.play_effect('/System/Library/Audio/UISounds/short_double_low.caf')
    v['switchDown'].value = True

####### OTHER INTERNAL PROCESSES #######
# passing text to textfield
def pTextfield_display(sender):
		idx = sender.selected_row
		if lang == 'nl':
				v['instruction'].text = data_nl[idx]
		if lang == 'en':
				v['instruction'].text = data_en[idx]

####### MAIN #######
if __name__ == "__main__":
		# console.clear()
		
		# ----- START UI ----- #
		v = ui.load_view()
		v.present('fullscreen')
		
		# ----- DEFINING CLIENT ----- #
		# address (on destination device) you are sending messages to
		client = SimpleUDPClient(p_ip, p_port)
		print("Sending on {}, port {}".format(p_ip, p_port))
		
		# ----- DEFINING CLIENT ----- #
		# address (on destination device) you are sending messages to
		client = SimpleUDPClient(u_ip, u_port)
		print("Sending on {}, port {}".format(u_ip, u_port))
		v['labelClient'].text = ("{} {}".format(u_ip, u_port))

		# ----- DISPATCHER ----- #
		# when a message is received, the dispatcher sends it to a function that acts on the message
		dispatcher = Dispatcher()
		
		dispatcher.map("/u/buttonUp", uButtonUp_output)
		dispatcher.map("/u/buttonDown", uButtonDown_output)
		
		# ----- INITIAL PROCESS FOR ANNOTATION LOG ----- #
		# create list for logging
		annotateWalk = []
		annotateExplore = []
		
		# ----- READ & DISPLAY INSTRUCTIONS ----- #
		# grabbing instructions (en) from a text file
		f_en = open('instructions-en.txt', encoding='utf-8')
		data_en = [row.strip() for row in f_en] 
		f_nl = open('instructions-nl.txt', encoding='utf-8')
		data_nl = [row.strip() for row in f_nl] 
		
		# displaying instructions to table
		datasource = ui.ListDataSource(data_en)
		v['tableInstructions'].data_source = datasource
		v['tableInstructions'].reload_data()

		# ----- DEFINING SERVER ----- #
		# address (on this device) you are listening to
		server = ThreadingOSCUDPServer((p_ip, p_port), dispatcher)
		print("Receiving on {}, port {}".format(p_ip, p_port))
		v['labelServer'].text = ("{} {}".format(p_ip, p_port))
		
		try:
			server.serve_forever()
			
		except KeyboardInterrupt:
			# save annotation log list to csv file
			print('saving files...')
			with open('annotateWalk.csv', 'w') as csvfile:
				s = csv.writer(csvfile, delimiter=',')
				s.writerows(annotateWalk)
			with open('annotateExplore.csv', 'w') as csvfile:
				s = csv.writer(csvfile, delimiter=',')
				s.writerows(annotateExplore)
			print('finished...')
			
			pass
