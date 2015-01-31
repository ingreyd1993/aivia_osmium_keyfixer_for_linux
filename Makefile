CC=gcc

CFLAGS=-std=c99

EXEC1=aivia_osmium_tty_getter

EXEC2=aivia_chvt_keyboard_restorer

all:
	$(CC) $(EXEC1).c $(CFLAGS) -o $(EXEC1).out
	$(CC) $(EXEC2).c $(CFLAGS) -o $(EXEC2).out
	@echo "Must chmod as root in order to claim ownership of compiled executables."
	@echo "***NOTE: if sudo is disabled on your system, you will have to change permissions manually.:"
	sudo chown root *.out
	sudo chmod +rxs *.out

