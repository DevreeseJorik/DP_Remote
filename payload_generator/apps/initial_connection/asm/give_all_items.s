@ Give all items through RCE

.arch armv5te
.text
.code	32
.arm
.global start
_start:
add r0, pc, #0x1
bx r0

.code	16
.thumb_func
push {r1-r7}
add r0, #0x2F           @ load _data address
ldr r5, [r0, #0x0]      @ load base address
ldr r5, [r5, #0x0]      @ load base value
add r0, #0x4

_struct_loop:
ldrh r1, [r0, #0x0]     @ item pocket offset
cmp r1, #0x0
beq _return

add r1, r5              @ item pocket address
ldrh r2, [r0, #0x2]     @ item count
ldrh r3, [r0, #0x4]     @ start id
ldrh r4, [r0, #0x6]     @ end id
add r0, #0x8

_item_loop:
strh r3, [r1, #0x0]     @ store item id
strh r2, [r1, #0x2]     @ store item count

cmp r3, r4              @ if current item == end item 
beq  _struct_loop

add r3, #0x1            @ increase item id
add r1, #0x4            @ increase item address
b _item_loop

_return:
pop {r1-r7}
mov r0, #0x1
pop {r4, pc}

_padding:
nop

_data:
.word 0x02106FC0        @ base address 

_items_1:
.short 0x838            @ Items (section 1)
.short 999
.short 0x47
.short 0x69

_items_2:
.short 0x8E0            @ Items (section 2)
.short 999
.short 0x87
.short 0x88

_items_3:
.short 0x8E8            @ Items (section 3)
.short 999
.short 0xD6
.short 0x147

_key_items:
.short 0xACC            @ Key items
.short 1
.short 0x1AC
.short 0x1D0

_tm_items:
.short 0xB94            @ TMs
.short 999
.short 0x148
.short 0x1A3

_hm_items:
.short 0xC3C            @ HMs
.short 1
.short 0x1A4
.short 0x1AB

_mail_items:
.short 0xD24            @ Mail
.short 999
.short 0x89
.short 0x94

_medicine_items:
.short 0xD54            @ Medicine
.short 999
.short 0x11             
.short 0x36

_berry_items:
.short 0xDF4            @ Berries
.short 999
.short 0x95
.short 0xD4

_pokeball_items:
.short 0xEF4            @ Poké Balls
.short 999
.short 0x1              
.short 0x10             

_battle_items:
.short 0xF30            @ Battle Items
.short 999
.short 0x37
.short 0x45

_null_terminator:
.word 0                @ Null terminator