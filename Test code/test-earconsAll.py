import os
import sound
import time


for dirpath, dirnames, filenames in os.walk('/System/Library/Audio/UISounds'):
	for f in filenames:
		if f.endswith('.caf'):
			full_path = os.path.join(dirpath, f)
			sound.play_effect(full_path)
			time.sleep(0.5)
