# ===================================================================================================

SRCDIR = $(CURDIR)/apps
OUTDIR = $(CURDIR)/out
OUTDIR_BIN = $(OUTDIR)/bin
OUTDIR_ELF = $(OUTDIR)/elf
SUBDIRS = $(shell find $(SRCDIR) -maxdepth 1 -type d | grep -vE "^$(SRCDIR)$$")
DEFAULT_MAKEFILE = $(SRCDIR)/default_makefile

# ===================================================================================================

all: clean $(OUTDIR) $(OUTDIR_BIN) $(OUTDIR_ELF) echo_build_dirs build_subdirs 

$(OUTDIR):
	mkdir -p $(OUTDIR)

$(OUTDIR_BIN):
	mkdir -p $(OUTDIR_BIN)

$(OUTDIR_ELF):
	mkdir -p $(OUTDIR_ELF)

echo_build_dirs:
	@echo $(SUBDIRS)

build_subdirs:
	for dir in $(SUBDIRS); do \
		if [ -f $$dir/Makefile ] || [ -f $$dir/makefile ]; then \
			$(MAKE) -C $$dir; \
		else \
			$(MAKE) -f $(DEFAULT_MAKEFILE) -C $$dir; \
		fi; \
		cp $$dir/build/*.bin $(OUTDIR_BIN)/; \
		cp $$dir/build/*.elf $(OUTDIR_ELF)/; \
	done

clean:
	rm -rf $(OUTDIR_BIN)
	rm -rf $(OUTDIR_ELF)

	for dir in $(SUBDIRS); do \
		if [ -f $$dir/Makefile ] || [ -f $$dir/makefile ]; then \
			$(MAKE) -C $$dir clean; \
		else \
			$(MAKE) -f $(DEFAULT_MAKEFILE) -C $$dir clean; \
		fi; \
	done
