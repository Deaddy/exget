#!/usr/bin/python

import imp, urllib2, sgmllib, os, re
from sys import argv, stdout, path

from BeautifulSoup import BeautifulSoup

# Where are the site definitions stored?
site_directory = path[0]+"/sites/"

class Exget():
	"""The base class every plugin inherits from. If you want one global
	save_path, you can provide it here and keep it out of your class
	definitions.
	
	toc_url is the url where you can find the "table of contents", i.e. where
	you can find the links.
	
	base_url is the base_url for the downloadable files
	
	file_pattern is a regex for defining which files to download
	
	save_path is the target directory"""
	toc_url = ""
	base_url = ""
	file_pattern = ""
	save_path = ""

	def __init__(self):
		html = urllib2.urlopen(self.toc_url).read()
		self.soup = BeautifulSoup(html)
		self.links = map(lambda x: x['href'], self.soup.findAll('a',
			href=re.compile(self.file_pattern)))
		files = os.listdir(os.path.expanduser(self.save_path))
		self.links = map(lambda x: x, (filter(lambda x: x.split('/')[-1] not in
			files, self.links)))

		print("Downloading files for %s"%(self.__class__.__name__))
		for link in self.links:
			self.__download(link)

	def __download(self, link):
		remote = urllib2.urlopen(self.base_url + link)
		with open(os.path.expanduser(self.save_path) + link.split('/')[-1], 'w') as f:
			stdout.write("Downloading %s... "%(link))
			f.write(remote.read())
			remote.close()
			stdout.write("done!\n")

def loadSites():
	"This function loads the sites"
	siteFiles = filter(lambda x: x[-3:] == ".py", os.listdir(site_directory))
	siteFiles.sort()
	for fn in siteFiles:
		f = fn[:-3]
		clsname = f[0].upper() + f[1:]
		info = imp.find_module(f, [site_directory])
		module = imp.load_module(f, info[0], info[1], info[2])
		info[0].close()
		cls = getattr(module, clsname)
		cls()

if __name__ == "__main__":
	loadSites()
	pass
