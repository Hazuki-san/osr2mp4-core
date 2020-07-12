import cv2
import numpy
from PIL import Image

from ....global_var import Settings
from ... import imageproc
from ...PrepareFrames.YImage import YImage


scoreboard = "menu-button-background"


def prepare_scoreboard(scale, settings):
	"""
	:param scale: float
	:return: [PIL.Image]
	"""
	img = YImage(scoreboard, settings, scale).img
	img = img.crop((int(img.size[0] * 2/3), 0, img.size[0], img.size[1]))
	if not Settings.usecv2:
		img = img.resize((int(140 * scale), int(64 * scale)))
	else:
		npimg = numpy.array(img)
		newimg = cv2.resize(npimg, (int(140 * scale), int(64 * scale)))
		img = Image.fromarray(newimg)
	imageproc.changealpha(img, 0.3)

	playerimg = imageproc.add_color(img, [80, 80, 80])
	img = imageproc.add_color(img, [60, 70, 120])
	return [img, playerimg]

