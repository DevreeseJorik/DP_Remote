@ Default code sent by server

.arch armv5te
.text
.code	32
.arm
.global start
_start:

_return:
mov r0, #0x1
pop {r4, pc}