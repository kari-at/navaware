from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

import datetime
import numpy as np
import ui
import csv
import sound
from PIL import Image

from accessiphone import *

####### IP ADDRESSES #######
# user IP (iPhone)
u_ip = "172.20.10.1"
#u_ip = "192.168.0.107"
u_port = 8000

# puppeteer IP (iPad)
p_ip = "172.20.10.7"
#p_ip = "192.168.0.102"
p_port = 2370

####### LANGUAGE #######
# language of sent messages
lang = 'nl'

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

# log annotations by appending to a list
def logInfo(mode, type, value, list):
		t = datetime.datetime.now()
		list.append([f"{t}", mode, type, value])

####### SENDING MESSAGES #######
# ----- UI INPUT THAT TRIGGERS SENT MESSAGES ----- #

# def pButtonVibe_input(sender):
#    osc_address = "/p/buttonVibe"
#    osc_value = True
#    client.send_message(osc_address, osc_value)
#    print_sent_messages(osc_address, osc_value)

# def pButtonEarcon1_input(sender):
#    osc_address = "/p/buttonEarcon1"
#    osc_value = True
#    client.send_message(osc_address, osc_value)
#    print_sent_messages(osc_address, osc_value)
#    v['labelDirection'].text_color = '#3d3dff'
#    v['viewDirection'].background_color = '#ffffff'

def pButtonEarcon_input(sender):
    osc_address = "/p/buttonEarcon"
    osc_value = True
    client.send_message(osc_address, osc_value)
    v['labelDirection'].text_color = '#3d3dff'
    v['viewDirection'].background_color = '#ffffff'
    print_sent_messages(osc_address, osc_value)
    
def pButtonText1_input(sender):
    osc_address = "/p/buttonText1"
    osc_value = v['textEnvDes'].text
    client.send_message(osc_address, osc_value)
    v['labelEnvDes'].text_color = '#34f134'
    v['viewEnvDes'].background_color = '#ffffff'
    print_sent_messages(osc_address, osc_value)
    mode = 'pull'
    type = 'environmental description'
    logInfo(mode, type, osc_value, logPushPullInfo)
    

def pButtonText2_input(sender):
    osc_address = "/p/buttonText2"
    osc_value = v['textStruct'].text
    client.send_message(osc_address, osc_value)
    print_sent_messages(osc_address, osc_value)
    mode = 'push'
    type = 'common street structure'
    logInfo(mode, type, osc_value, logPushPullInfo)

def pButtonTextBody_input(sender):
		osc_address = "/p/buttonTextB"
		if lang == 'nl':
				osc_value = 'Heroriënteer.'
		elif lang == 'en':
				osc_value = 'Reorient.'
		client.send_message(osc_address, osc_value)
		print_sent_messages(osc_address, osc_value)

def pButtonTextLeft_input(sender):
		osc_address = "/p/buttonTextL"
		if lang == 'nl':
				osc_value = 'Draai naar de linkerkant.'
		elif lang == 'en':
				osc_value = 'Turn towards your left.'
		client.send_message(osc_address, osc_value)
		print_sent_messages(osc_address, osc_value)
		mode = 'push'
		type = 'turning point'
		logInfo(mode, type, osc_value, logPushPullInfo)

def pButtonTextRight_input(sender):
		osc_address = "/p/buttonTextR"
		if lang == 'nl':
				osc_value = 'Draai naar de rechtkant.'
		elif lang == 'en':
				osc_value = 'Turn towards your right.'
		client.send_message(osc_address, osc_value)
		print_sent_messages(osc_address, osc_value)
		mode = 'push'
		type = 'turning point'
		logInfo(mode, type, osc_value, logPushPullInfo)

def pButtonTextStop_input(sender):
		osc_address = "/p/buttonTextS"
		if lang == 'nl':
				osc_value = 'Stop.'
		elif lang == 'en':
				osc_value = 'Stop.'
		client.send_message(osc_address, osc_value)
		print_sent_messages(osc_address, osc_value)

####### RECORDING MESSAGES #######
# ----- UI INPUT THAT TRIGGERS ANNOTATIONS----- #

# log annotations by appending to a list
def logAnnotate(mode, value, list):
		t = datetime.datetime.now()
		if value == True:
				list.append([f"{t}", mode, 'start', len(list)//2])
		elif value == False:
				list.append([f"{t}", mode, 'end', (len(list)-1)//2])

def pSwitchWalk_annotate(sender):
		log_label = "/a/switchWalk" #this osc address is not actually sent
		log_value = sender.value
		print_recorded_messages(log_label, log_value)
		logAnnotate('walk', log_value, annotateWalk)

def pSwitchExplore_annotate(sender):
		log_label = "/a/switchExplore" #this osc address is not actually sent
		log_value = sender.value
		print_recorded_messages(log_label, log_value)
		logAnnotate('explore', log_value, annotateExplore)

def pSwitchOther_annotate(sender):
		log_label = "/a/switchOther" #this osc address is not actually sent
		log_value = sender.value
		print_recorded_messages(log_label, log_value)
		logAnnotate('other', log_value, annotateOther)

####### RECEIVING MESSAGES #######
# ----- ACTIONS TRIGGERED BY RECEIVED MESSAGES VIA DISPATCHER ----- #
def uButtonUp_output(address, *args):
    print_received_messages(address, *args)
    sound.play_effect('/System/Library/Audio/UISounds/short_double_high.caf')
    osc_address = "/c/buttonUp"
    osc_value = args[0]
    client.send_message(osc_address, osc_value)
    v['labelDirection'].text_color = '#ffffff'
    v['viewDirection'].background_color = '#3d3dff'
    mode = 'pull'
    type = 'direction'
    value = 'none'
    logInfo(mode, type, value, logPushPullInfo)
    
def uButtonDown_output(address, *args):
    print_received_messages(address, *args)
    sound.play_effect('/System/Library/Audio/UISounds/short_double_low.caf')
    osc_address = "/c/buttonDown"
    osc_value = args[0]
    client.send_message(osc_address, osc_value)
    v['labelEnvDes'].text_color = '#ffffff'
    v['viewEnvDes'].background_color = '#34f134'

#confirm
def cText(address, *args):
		#print_received_messages(address, *args)
		text2speech(args[0], lang)

def cEarcon(address, *args):
    #print_received_messages(address, *args)
    earcon('iOS_healthNotification')
    
#def cEarcon2(address, *args):
#    #print_received_messages(address, *args)
#    earcon('download_pingBing')

####### OTHER INTERNAL PROCESSES #######
# passing text to textfield
def pTextEnvDes_display(sender):
		idx = sender.selected_row
		if lang == 'nl':
				v['textEnvDes'].text = envdes_nl[idx]
		elif lang == 'en':
				v['textEnvDes'].text = envdes_en[idx]

def pTextStruct_display(sender):
		idx = sender.selected_row
		if lang == 'nl':
				v['textStruct'].text = struct_nl[idx]
		elif lang == 'en':
				v['textStruct'].text = struct_en[idx]

def pTextDirect_display(sender):
		idx = sender.selected_row
		if lang == 'nl':
				v['textStruct'].text = direct_nl[idx]
		elif lang == 'en':
				v['textStruct'].text = direct_en[idx]

####### MAIN #######
if __name__ == "__main__":
		# console.clear()
		
		# ----- START UI ----- #
		v = ui.load_view()
		v.present('fullscreen')
		
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
		dispatcher.map("/c/text", cText)
		#dispatcher.map("/c/earcon1", cEarcon1)
		dispatcher.map("/c/earcon", cEarcon)
		
		# ----- INITIAL PROCESS FOR ANNOTATION LOG ----- #
		# create list for logging annotation
		annotateWalk = []
		annotateExplore = []
		annotateOther = []
		
		# create list for logging pushed and pulled info
		logPushPullInfo = []
		
		# ----- READ & DISPLAY INSTRUCTIONS ----- #
		# grabbing environment description (en) from a text file
		f_en = open('envdes_en.txt', encoding='utf-8')
		envdes_en = [row.strip() for row in f_en] 
		f_nl = open('envdes_nl.txt', encoding='utf-8')
		envdes_nl = [row.strip() for row in f_nl] 
		
		# grabbing street structure (en) from a text file
		f_en = open('struct_en.txt', encoding='utf-8')
		struct_en = [row.strip() for row in f_en] 
		f_nl = open('struct_nl.txt', encoding='utf-8')
		struct_nl = [row.strip() for row in f_nl] 
		
		# displaying instructions to table
		datasource1 = ui.ListDataSource(envdes_en)
		v['tableEnvDes'].data_source = datasource1
		v['tableEnvDes'].reload_data()
		
		# displaying instructions to table
		datasource2 = ui.ListDataSource(struct_en)
		v['tableStruct'].data_source = datasource2
		v['tableStruct'].reload_data()
		
		# display image
		map = ui.Image("map.jpg")
		v['imageMap'].image = map

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
			with open('annotateWalk.csv', 'w', encoding='utf-8') as csvfile:
				s = csv.writer(csvfile, delimiter=',')
				s.writerows(annotateWalk)
			with open('annotateExplore.csv', 'w', encoding='utf-8') as csvfile:
				s = csv.writer(csvfile, delimiter=',')
				s.writerows(annotateExplore)
			with open('annotateOther.csv', 'w', encoding='utf-8') as csvfile:
				s = csv.writer(csvfile, delimiter=',')
				s.writerows(annotateOther)
			with open('logPushPullInfo.csv', 'w', encoding='utf-8') as csvfile:
				s = csv.writer(csvfile, delimiter=',')
				s.writerows(logPushPullInfo, )
			print('finished...')
			
			pass
