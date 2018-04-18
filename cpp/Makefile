SHELL := /bin/bash

.PHONY: all clean

OPENCV_FLAGS := $(shell pkg-config --cflags --libs opencv)
GLOBAL_FLAGS = -std=c++0x

FILES = main.cpp\
camera_manager.cpp\
human_detector.cpp

all: main


main:
	g++ $(OPENCV_FLAGS) $(FILES) -o main $(GLOBAL_FLAGS)

clean:
	rm -f *.o main