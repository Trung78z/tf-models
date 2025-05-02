CXX ?= g++

# Compiler flags
CXXFLAGS = -std=c++17 -g -O0 `pkg-config --cflags opencv4`

# Linker flags - MUST include all required OpenCV libraries
LDFLAGS = `pkg-config --libs opencv4`

# Final executable
TARGET = main

all: $(TARGET)

$(TARGET): main.o
	$(CXX) $< -o $@ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f *.o $(TARGET)