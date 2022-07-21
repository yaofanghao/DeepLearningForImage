CC  = gcc
CXX = g++

# run 
#   export PKG_CONFIG_PATH=/opt/OpenCV-2.4/lib/pkgconfig
OPENCV_CFLAGS = $(shell pkg-config --cflags opencv)
OPENCV_LIBS   = $(shell pkg-config --libs opencv)

BOOST_CFLAGS =
BOOST_LIBS   = -lboost_serialization -lboost_system -lboost_thread -lboost_program_options

CFLAGS = $(OPENCV_CFLAGS) $(BOOST_CFLAGS) \
	    -I./eigen3 \
        -msse4 -msse3 -msse2 -msse -std=c++0x
LDFLAGS = $(OPENCV_LIBS) $(BOOST_LIBS)

src-cxx-all := $(wildcard *.cpp)
src-c-all   := $(wildcard *.c)
bin-all     := $(patsubst %.cpp,%.e,$(src-cxx-all)) $(patsubst %.c,%.e,$(src-c-all))


all : utils.o tools.e



%.e:%.cpp
	$(CXX) -o $@ $? utils.o $(CFLAGS) $(LDFLAGS)
	
%.o:%.cpp
	$(CXX) -c $< -o $@ $(CFLAGS)

%.o:%.c
	$(CXX) -c $< -o $@ $(CFLAGS)

clean :
	rm -f *.e *.o

