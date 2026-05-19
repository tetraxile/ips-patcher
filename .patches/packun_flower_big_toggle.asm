@nsobid 891687F016A18F1773D4A88EBF8A973C8E33ECC1

00103850:
	; Check for arg PackunFlowerBig and store it to location of big flag
	mov		x2, x1
	add		x0, x19, #0x175
	mov		x1, x20
	bl		#0x88b1c0

	; Skip now unused code
	b		#0x103874