import numpy as np
from PIL import Image

from ... import imageproc
from ....global_var import Settings, GameplaySettings


def prepare_background(backgroundname):
	"""
	:param backgroundname: string
	:return: PIL.Image
	"""
	print(backgroundname)
	img = Image.open(backgroundname).convert("RGBA")

	width = Settings.width
	height = Settings.height
	ratiow = width / height
	ratioh = height / width

	w = min(img.size[0], int(img.size[1] * ratiow))
	h = min(img.size[1], int(img.size[0] * ratioh))
	x, y = (img.size[0] - w)//2, (img.size[1] - h)//2
	img = img.crop((x, y, x + w, y + h))

	scale = width/w
	img = imageproc.change_size(img, scale, scale)
	imgs = [Image.new("RGBA", (1, 1))]

	dim = max(0, min(100, (100 - GameplaySettings.settings["Background dim"]))) * 2.55
	color = np.array([dim, dim, dim])
	interval = int(1000/Settings.fps)
	c_interval = max(0, (GameplaySettings.settings["Background dim"] - 50) * 2.55/interval)
	color[:] = color[:] - c_interval
	for x in range(interval):
		color[:] = color[:] + c_interval
		a = imageproc.add_color(img, color)
		imgs.append(a)
	return imgs