import speech
import time

def finish_speaking():
	while speech.is_speaking():
		time.sleep(0.1)

a = 'dankjewel'

speech.say(a,'nl-NL')
finish_speaking()
