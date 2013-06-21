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
	else:
		# Convert BeautifulSoup thing into real unicode object
		unescaped = unicode(unescaped)
	return unescaped.encode("utf-8")


def get_url(s):
	url = s.replace("<wbr></wbr>", "").split(">", 1)[1]
	assert not '<' in url, url
	assert not '>' in url, url
	if '&' in url:
		url = unescape_xhtml(url)
	if url.startswith("feed://"):
		# Feed Directory has some feed:// results, but Reader treats feed://
		# and http:// as the same feed.
		url = url.replace("feed://", "http://", 1)
	return url


def yield_urls(fh):
	TAKE, SKIP = range(2)
	state = TAKE
	for line in fh:
		if '<div class="feed-result-stats"><span class="number">' in line:
			if '<span class="number">Unknown</span>' in line:
				state = SKIP
			else:
				state = TAKE
		elif state == TAKE and line.startswith('<div class="feed-info">'):
			yield get_url(line.rstrip())


def main():
	for url in yield_urls(sys.stdin):
		print url


if __name__ == '__main__':
	main()
