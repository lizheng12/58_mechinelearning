#!/usr/bin/python
#-*- coding:utf-8 -*-
#定义Movie类及其父类Video类，对电影的基本信息进行分级描述
import webbrowser


class Video():
	"""抽象出影视作品的共同属性，作为影视基类"""

	#功能：初始化对象
	#输入：title - 标题
	#		poster_image - 海报图片
	def __init__(self, title, poster_image):
		self.title = title
		self.poster_image_url = poster_image


class Movie(Video):
	"""定义电影类，描述电影的属性"""

	#功能：初始化对象
	#输入：title - 标题
	#		poster_image - 海报图片
	def __init__(self, movie_title, movie_storyline, poster_image, trailer_youtube):
		Video.__init__(self, movie_title, poster_image)
		self.storyline = movie_storyline
		self.trailer_youtube_url = trailer_youtube