@ Inject overlay payload
@ Makes LoadOverlay execute from 0x023a9320 after copying overlays

@ r3, r4 and lr are already on the stack

.arch armv5te
.text
.code	16
.thumb_func
.global start
_start:
push {r0-r2, lr}

add r3, #0x11
ldmia r3!, {r0, r1, r2, r4}
str r2, [r0, #0x0]                  @ overwrite LoadOverlay return instruction
mov r2, #0x20                       @ size of data to copy
add r0, r3, #0x0                    @ source buffer address
blx r4                              @ execute memcp_uint8

pop {r0-r4, pc}

_data:
.word 0x020d75d8                    @ return instruction of LoadOverlay
.word 0x023a9320                    @ destination buffer address
.word 0xea0b4750                    @ branch instruction to 0x023a9320 relative to 0x020d75d8
.word 0x020ce3e0                    @ memcp_uint8
