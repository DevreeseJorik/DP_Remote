# ===================================================================================================
NAME            = debugging

SOURCE_DIR		= $(CURDIR)/src
COMMON_DIR		= $(CURDIR)/common
SOURCE 			= $(SOURCE_DIR)/debugging.c
COMMON_SRC      = $(wildcard $(COMMON_DIR)/*.c)


SYMBOLFILE		= $(SOURCE_DIR)/symbols.sym
LINKERFILE		= $(SOURCE_DIR)/linker.ld

BUILDDIR		= ./build

CC				= arm-none-eabi-gcc
AS				= arm-none-eabi-as
CFLAGS			= -mcpu=arm946e-s -mthumb -Os -nostartfiles -nodefaultlibs -fno-builtin -ffunction-sections --data-sections -Wl,--gc-sections
LDFLAGS			= --specs=nosys.specs -T $(LINKERFILE)
INC				= -I$(COMMON_DIR)

LDFLAGS			+= -Wl,--just-symbols=$(SYMBOLFILE)
LIB				=

COMMON_OBJS      = $(COMMON_SRC:$(COMMON_DIR)/%.c=$(BUILDDIR)/%.o)

MAIN_OBJ         = $(BUILDDIR)/debugging.o

all: clean $(BUILDDIR) $(BUILDDIR)/$(NAME)

$(BUILDDIR)/%.o: $(COMMON_DIR)/%.c
	$(CC) $(CFLAGS) $(INC) -c $< -o $@

$(MAIN_OBJ): $(SOURCE)
	$(CC) $(CFLAGS) $(INC) -c $(SOURCE) -o $(MAIN_OBJ)

$(BUILDDIR)/$(NAME): $(COMMON_OBJS) $(MAIN_OBJ)
	$(CC) $(CFLAGS) $(INC) $(LDFLAGS) $(COMMON_OBJS) $(MAIN_OBJ) -o $(BUILDDIR)/$(NAME) $(LIB)
	arm-none-eabi-objcopy -O binary $(BUILDDIR)/$(NAME) $(BUILDDIR)/$(NAME).bin
	arm-none-eabi-objdump -d $(BUILDDIR)/$(NAME) > $(BUILDDIR)/$(NAME).elf
	arm-none-eabi-objdump -s -j .data $(BUILDDIR)/$(NAME) >> $(BUILDDIR)/$(NAME).elf

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)/*