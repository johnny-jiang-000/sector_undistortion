CFLAGS += -std=c++17 -O3
LDFLAGS += -lpthread

all:
	g++ sector.cpp $(CFLAGS) $(LDFLAGS) -o sector
