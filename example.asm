; always update coin count
001deae0:
	nop

; always update timer 1
004cc360:
	bl #0x85e000

; always update timer 2
0085e000:
	mov x19, x0
	ldr x8, [x0, #0x2d0]
	ldr x22, [x8, #0x20]
	ldr w9, [x22, #0x6e8]
	str w9, [x22, #0x5d8]
	mov x0, x19
	ret

; store moon splits in purple coins
0051eb88:
	ldr w8, [x0, #0x9f0]
	ldr x9, [x0, #0xa00]
	cmp w8, #0
	ldr x10, [x0, #0x5e8]
	csel w8, w8, wzr, gt
	sbfiz x8, x8, #2, #0x20
	ldr w11, [x0, #0x6e8]
	str w11, [x9, x8]
	str wzr, [x10, x8]
	str xzr, [x0, #0x6e8]
	ret

; disable collecting coins
00520fcc:
	ret

; reset timer on laoding zones
00522cc4:
	str xzr, [x0, #0x6e8]
	ret

; disable coin counter animations
001debc0:
	nop

001dec28:
	nop

001df044:
	nop

001df0bc:
	nop

; always enable warps
001f2a2c:
	mov w0, #1

