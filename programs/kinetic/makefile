V_N = 100000
V_U0 = 0.23
V_DT = 1e-6
#V_MONOMIAL_COUNT = 2
#V_ALPHAS = {-1.0,3.0}
#V_POWERS = {1,2}
V_MONOMIAL_COUNT = 5
V_ALPHAS = {-1.0,3.0,2.0,-1.0,5.0}
V_POWERS = {1,2,3,4,6}

EPSVIEWER = atril

CC = gcc./kinetic

VECFLAGS = -ftree-vectorize -fopt-info-vec-optimized
CONSTFLAGS = -march=native
RANDFLAGS = -msse2 -finline-functions -fomit-frame-pointer -fno-strict-aliasing --param max-inline-insns-single=1800
OPTIFLAGS = -O3 $(CONSTFLAGS) $(RANDFLAGS) $(VECFLAGS)
MTFLAGS = -DSFMT_MEXP=19937 -DHAVE_SSE2
CFLAGS = -DN=$(V_N) -DU0=$(V_U0) -DDT=$(V_DT) -DMONOMIAL_COUNT=$(V_MONOMIAL_COUNT) -DALPHAS=$(V_ALPHAS) -DPOWERS=$(V_POWERS)
LDFLAGS = -lm

EXEC_KIN = kinetic
EXEC_ANA = analytic
SRC_KIN = $(EXEC_KIN).c
SRC_ANA = $(EXEC_ANA).c
SRC_MT = SFMT.c

all: $(EXEC_KIN) $(EXEC_ANA)
	mkdir -p out
	./$(EXEC_KIN)
	# ./$(EXEC_ANA)
	# ./graph.gnu
	# $(EPSVIEWER) ./out/graph.eps

$(EXEC_ANA): $(SRC_ANA)
	$(CC) $(SRC_ANA) $(CFLAGS) $(LDFLAGS) -o $(EXEC_ANA)

$(EXEC_KIN): $(SRC_KIN) $(SRC_MT)
	$(CC) $(SRC_KIN) $(SRC_MT) $(OPTIFLAGS) $(MTFLAGS) $(CFLAGS) $(LDFLAGS) -o $(EXEC_KIN)

orig: kinetic_orig.c $(SRC_MT)
	gcc kinetic_orig.c $(SRC_MT) $(OPTIFLAGS) $(MTFLAGS) $(CFLAGS) $(LDFLAGS) -o kinetic_orig
	./kinetic_orig kinetic_orig

clean:
	rm -f $(EXEC_KIN)
	rm -f ./kin_orig kin_orin.txt

clean_all:
	rm -rf out/*
	rm -f $(EXEC_KIN) $(EXEC_ANA)
