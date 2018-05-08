
BINS = exo3

AS = gcc
ASFLAGS = -m64 -g -c
CC = gcc
CFLAGS = -Wall -Wextra -m64 -g -std=c99
LD = gcc
LDFLAGS = -m64

OSTYPE = $(shell uname)

.PHONY: all
all: $(BINS)

exo3: fct_exo3.o exo3.o

%.o: %.s
ifeq ($(OSTYPE),Darwin)
	$(AS) $(ASFLAGS) -o /tmp/_tmp_objconv_$@ $<
	objconv -fmacho -nu+ -v0 /tmp/_tmp_objconv_$@ $@
else
	$(AS) $(ASFLAGS) -o $@ $<
endif

OBJS = \
	   $(foreach f, $(BINS), $(addsuffix .o, $f)) \
	   $(foreach f, $(BINS), $(addprefix fct_, $(addsuffix .o, $f)))

.PHONY: clean
clean:
	$(RM) $(BINS) $(OBJS)

