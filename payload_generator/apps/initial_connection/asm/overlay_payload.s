@ Custom payload to be ran after LoadOverlay

.arch armv5te
.text
.code	32
.arm
.global start
_start:
add r3, pc, #0x1
bx r3

.code	16
.thumb_func
push {r0-r7, lr}
ldr r3, [pc, #0x8]
ldr r2, [pc, #0x8]
strh r2, [r3, #0x0]
pop {r0-r7, pc}
.hword 0x0

_data:
.word 0x022331f8                   @ get Pokémon data from server function
bx r0                              @ ensure that the remote code does a pop {r4,pc} to return
.hword 0x0



