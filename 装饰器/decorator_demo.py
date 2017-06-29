import urllib  # py2


# import urllib.request as urllib # py3

def cache(func):

    #
    saved = {}
    def wrapper(url):
        if url in saved:
            return saved[url]
        else:
            page = func(url)
            saved[url] = page
            return page

    return wrapper


@cache
def web_lookup(url):
    return urllib.urlopen(url).read()[:10]


if __name__ == '__main__':
    for _ in xrange(5):
        web_lookup("http://www.baidu.com")
