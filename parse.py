#!/usr/bin/python

import sys
from BeautifulSoup import BeautifulSoup


def unescape_xhtml(s):
	htmlInput = '<html>' + s
	# Livejournal stream has &apos; so we must use XHTML_ENTITIES
	unescaped = BeautifulSoup(
		htmlInput, convertEntities=BeautifulSoup.XHTML_ENTITIES
	).contents[0].string
	if not unescaped:
		unescaped = u""
	return unescaped.decode("utf-8")


def get_url(s):
	url = s.replace("<wbr></wbr>", "").split(">", 1)[1]
	if '&' in url:
		return unescape_xhtml(url)
	return url


def main():
	TAKE, SKIP = range(2)
	state = TAKE
	for line in sys.stdin:
		if '<div class="feed-result-stats"><span class="number">' in line:
			if '<span class="number">Unknown</span>' in line:
				state = SKIP
			else:
				state = TAKE
		elif state == TAKE and line.startswith('<div class="feed-info">'):
			print get_url(line.rstrip())


if __name__ == '__main__':
	main()
