#!/usr/bin/python

from exget import Exget

class Wahrscheinlichkeitstheorie(Exget):

	toc_url = "http://wwwmath.uni-muenster.de/statistik/lehre/SS11/WT/"
	base_url = toc_url
	save_path = "~/uni/wahrscheinlichkeitstheorie/"
	file_pattern = "Aufgaben\/Blatt\d{1,2}\.pdf"
