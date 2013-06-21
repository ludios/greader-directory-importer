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
	# Convert BeautifulSoup thing into real str
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


def yield_urls(fh, take_everything):
	UNKNOWN, TAKE, SKIP = range(3)
	state = UNKNOWN
	if take_everything:
		# In case we have grep filtering out everything but feed URL lines
		state = TAKE
	for line in fh:
		if '<div class="feed-result-stats"><span class="number">' in line:
			if not take_everything and '<span class="number">Unknown</span>' in line:
				state = SKIP
			else:
				state = TAKE
		elif line.startswith('<div class="feed-info">'):
			if state == TAKE:
				yield get_url(line.rstrip())
			elif state == UNKNOWN:
				raise RuntimeError("Got feed-info %r before feed-result-stats?" % (line,))
			# else pass if SKIP


def main():
	# Take everything because Google actually does have data for some "Unknown" feeds
	for url in yield_urls(sys.stdin, take_everything=True):
		print url


if __name__ == '__main__':
	main()
