#!/usr/bin/python
#-*- coding:utf-8 -*-
#文件描述：存储我喜欢的电影的基本信息，编入列表，并集中展示在网页上

import media
import fresh_tomatoes

Flipped = media.Movie("Flipped",
						"Palpitate with excitement", 
						"https://upload.wikimedia.org/wikipedia/en/3/3a/Flipped_poster.jpg", 
						"https://www.youtube.com/watch?v=RDlXdujRSD8")

Whisper_of_the_Heart_Trailer = media.Movie("Whisper of the Heart Trailer",
						"Whisper of the Heart Trailer",
						"https://upload.wikimedia.org/wikipedia/zh/8/8f/Whisper_of_the_Heart_Poster.jpg",	#noqa
						"https://www.youtube.com/watch?v=M2s3nDI9KMM")

Heidi = media.Movie("Heidi",
						"Heidi and her Grandpa",
						"https://upload.wikimedia.org/wikipedia/commons/1/1a/Spyri_Heidi_Cover_1887.jpg",	#noqa
						"https://www.youtube.com/watch?v=imsd1N9cnYw")

movies = [Flipped, Whisper_of_the_Heart_Trailer, Heidi]
fresh_tomatoes.open_movies_page(movies)