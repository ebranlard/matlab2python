MAIN=matlab2python.py
# --- Detecting OS: Windows, Darwin
ifeq '$(findstring ;,$(PATH))' ';'
    detected_OS := Windows
else
    detected_OS := $(shell uname 2>/dev/null || echo Unknown)
    detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
    detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
    detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
endif

all:
	python $(MAIN) tests/files/test_class1.m 

install:
	python setup.py install

dep:
	python -m pip install -r requirements.txt

help:
	@echo "Available rules:"
	@echo "   all        run the standalone program"
	@echo "   install    install the python package in the system" 
	@echo "   pull       download the latest version " 
	@echo "   test       run the unit tests " 

test:
	python -m unittest discover -v

prof:
	python -m cProfile -o _tests/prof_all.prof  _tests/prof_all.py
	python -m pyprof2calltree -i _tests/prof_all.prof -o _tests/callgrind.prof_all.prof
	snakeviz _tests/prof_all.prof

clean:
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf *.spec
	rm -rf build*
	rm -rf dist

pyexe:
	pyinstaller --onedir $(MAIN)

