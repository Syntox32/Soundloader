from setuptools import setup

version = "0.1.0"

lines = []
with open("requirements.txt") as f:
	lines = f.read().splitlines()
	
# Remove comments and empty lines
reqs = [s for s in lines if not s.startswith("#") and s != ""]

setup(
	name="Soundloader",
	packages=[],
	version=version,
	description="Take Soundcloud with you offline.",
	
	install_requires=reqs,
	scripts=["soundloader.py"]
)