import sys, gdown

url = sys.argv[1]
gdown.download(url=url, quiet=False, fuzzy=True)
