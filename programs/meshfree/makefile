V_N = 10
V_U0 = 0.6
V_FUN = 'u^2-u'
V_GENFILE = recalcD
V_GENSCRIPT = gen_code.py
CC = gcc
CFLAGS = -DMASS=$(V_N) -DU0=$(V_U0) -O3
LDFLAGS = -lm
EXEC = meshfree
SRC = $(EXEC).c
SRC2 = $(V_GENFILE).c

$(EXEC)_noout: $(SRC) $(SRC2)
	$(CC) $(SRC) $(SRC2) $(CFLAGS) -DNOOUT $(LDFLAGS) -o $(EXEC)

$(EXEC): $(SRC) $(SRC2)
	$(CC) $(SRC) $(SRC2) $(CFLAGS) $(LDFLAGS) -o $(EXEC)

$(SRC2): $(V_GENSCRIPT)
	./$(V_GENSCRIPT) $(V_N) $(V_U0) $(V_FUN) $(V_GENFILE)

all: $(EXEC)
	mkdir -p out
	./$(EXEC)
	./graph.gnu
	okular ./out/graph.eps

clean:
	rm -f $(EXEC)

clean_all:
	rm -rf out/*
	rm -f $(EXEC) $(V_GENFILE).*
