#! python3

"""this is 8comic module for comiccrawler.

"""

import re
from urllib.parse import urljoin

from node_vm2 import VM

from ..core import Episode, grabhtml

domain = ["www.8comic.com", "www.comicvip.com", "www.comicbus.com"]
name = "無限"

def get_title(html, url):
	return re.search("<font color=\"#FF6600\" style=\"font:12pt;"
			"font-weight:bold;\">(.+?)</font>",html).group(1)

def get_episodes(html, url):
	html = html.replace("\n", "")
	
	js = """
		var output;
		function getCookie() {}
		var window = {
			open: function(result){
				output = result;
			}
		};
		function get(url, catid) {
			cview(url, catid);
			return output;
		}
		var document = {
			location: {
				href: ""
			}
		};
	""" + grabhtml(urljoin(url, "/js/comicview.js"))
	
	s = []
	matches = re.finditer(
		"<a href='#' onclick=\"cview\('(.+?)',(\d+?)\);return "
			"false;\" id=\"\w+?\" class=\"\w+?\">(.+?)</a>",
		html, re.M
	)
	with VM(js) as vm:
		for match in matches:
			ep_url, catid, title = match.groups()
			
			ep_url = vm.call("get", ep_url, int(catid))

			# tag cleanup
			title = title.strip()
			title = re.sub("<script.+?</script>","",title)
			title = re.sub("<.+?>","",title)

			e = Episode(title, urljoin(url, ep_url))
			s.append(e)
	return s
	
def get_images_20140406(html, url, ch):
	"""before 2014/4/6"""
	itemid = re.search("itemid=(.+?);", html).group(1)
	allcodes = re.search("allcodes=\"(.+?)\"", html).group(1)

	cs = allcodes.split("|")
	code = ""

	for c in cs:
		if c.split(" ")[0] == ch:
			code = c
			break
	else:
		raise Exception("can't retrieve imgurl")

	num, sid, did, pages, code = code.split(" ")
	s = []
	for p in range(1, int(pages)+1):
		hash = (((p - 1) // 10) % 10) + (((p - 1) % 10) * 3)
		img = (
			"http://img{sid}.8comic.com/{did}/{itemid}/{num}/"
			"{page:03}_{code}.jpg"
		).format(sid=sid, did=did, itemid=itemid, num=num, page=p,
			code=code[hash:hash+3])
		s.append(img)
	return s

def get_images(html, url):
	m = re.search("ch=(\d+)", url)
	if m is None:
		ch = "1"
	else:
		ch = m.group(1)

	try:
		get_images_20140406(html, url, ch)
	except AttributeError:
		pass

	# after 2014/4/6
	def ss(str): # pylint: disable=invalid-name
		return re.sub("[a-z]+", "", str)

	cs = re.search("cs='(.+)'", html).group(1)
	ti = re.search("ti=(\d+);", html).group(1)

	i = 0
	while i < len(cs):
		if ch == ss(cs[i:i+4]):
			code = cs[i:i+50]
			break
		i += 50
	else:
		code = cs[-50:]

	pages = int(ss(code[7:10]))

	s = []
	for p in range(1, pages + 1):
		hash = (((p - 1) // 10) % 10) + (((p - 1) % 10) * 3)
		src = "http://img{}.8comic.com/{}/{}/{}/{:03}_{}.jpg".format(
				ss(code[4:6]), code[6:7], ti, ch, p, code[hash + 10:hash + 13])
		s.append(src)
	return s
