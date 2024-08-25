# ===================================================================================================
NAME            = initial_connection

# The directory containing .s files
SRCDIR          = ./asm

# The build directory
BUILDDIR        = ./build

# The address where you want to extract the binary
VMA             = 0x0

# The name pattern for the built files
TARGET_VMA      = $(VMA)

# Compiler and flags
CC              = arm-none-eabi-gcc
CFLAGS          = -nostartfiles -nostdlib #-ffreestanding
LDFLAGS         = -Wl,--section-start=.text=$(VMA)

# Find all .s files in the SRCDIR
SOURCES         = $(wildcard $(SRCDIR)/*.s)

# Generate the list of object files
OBJECTS         = $(patsubst $(SRCDIR)/%.s, $(BUILDDIR)/%.o, $(SOURCES))

# Generate the list of binaries
BINS            = $(patsubst $(SRCDIR)/%.s, $(BUILDDIR)/%_$(TARGET_VMA).bin, $(SOURCES))

# ===================================================================================================

# Default target: build everything
all: clean $(BUILDDIR) $(BINS)

# Create the build directory if it doesn't exist
$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# Rule to generate the binary files
$(BUILDDIR)/%_$(TARGET_VMA).bin: $(SRCDIR)/%.s | $(BUILDDIR)
	$(CC) $< -o $(BUILDDIR)/$*_$(TARGET_VMA) $(CFLAGS) $(LDFLAGS)
	arm-none-eabi-objcopy -O binary $(BUILDDIR)/$*_$(TARGET_VMA) $@
	arm-none-eabi-objdump -d $(BUILDDIR)/$*_$(TARGET_VMA) > $(BUILDDIR)/$*_$(TARGET_VMA)_dump.txt
	rm $(BUILDDIR)/$*_$(TARGET_VMA)

# Clean the build directory
clean:
	rm -rf $(BUILDDIR)/*
