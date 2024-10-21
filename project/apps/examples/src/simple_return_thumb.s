@ Default code sent by server

.arch armv5te
.text
.code	32
.thumb
.global start
_start:

_return:
push {lr}
mov r0, #0
pop {pc}