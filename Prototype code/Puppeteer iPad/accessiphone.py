import ctypes
import time
import sound
import speech


c = ctypes.CDLL(None)

# access to vibration motor (duration cannot be controlled)
def vibrate():
	p = c.AudioServicesPlaySystemSound
	p.restype, p.argtypes = None, [ctypes.c_int32]
	vibrate_id = 0x00000fff
	p(vibrate_id)

# earcons
# type:
	# built-in iOS options
	# | iOS_shortDoubleLow
	# manually downloaded options
	# | download_pingBing

def earcon(type):
	if type == 'iOS_shortDoubleLow':
		sound.play_effect('/System/Library/Audio/UISounds/short_double_low.caf')
	elif type == 'iOS_healthNotification':
		sound.play_effect('/System/Library/Audio/UISounds/health_notification.caf')
	elif type == 'iOS_beep':
		sound.play_effect('/System/Library/Audio/UISounds/ct-path-ack.caf')
	elif type == 'download_pingBing':
		sound.play_effect('ping_bing.wav')
	else:
		print ('sound file does not exist.')

# text to speech
def finish_speech():
	while speech.is_speaking():
		time.sleep(0.1)

def text2speech(text, lang):
	input = text
	if lang == 'nl':
		speech.say(input,'nl-NL')
	if lang == 'en':
		speech.say(input,'en-EN')
	finish_speech()

