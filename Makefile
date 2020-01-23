CFLAGS += -std=c++17 -O3
LDFLAGS += -lpthread

all:
	$(CXX) sector.cpp $(CFLAGS) $(LDFLAGS) -o sector
