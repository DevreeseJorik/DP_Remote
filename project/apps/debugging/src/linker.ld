MEMORY {
    RAM : ORIGIN = 0x023B0000, LENGTH = 60k
}

SECTIONS {
    .text : {
        _start = 0x023B0000;
        KEEP(*(.text.main))
        KEEP(*(.text.main_thumb))
        *(.text.startup)
        *(.text*)
        . = ALIGN(4);
    } > RAM

    .rodata : {
        *(.rodata*)
        . = ALIGN(4);
    } > RAM

    .data : {
        KEEP(*(.data.command_data))
        *(.data*)
        *(.data.*)
        . = ALIGN(4);
    } > RAM

    .got : {
        *(.got*)
        . = ALIGN(4);
    } > RAM
}
