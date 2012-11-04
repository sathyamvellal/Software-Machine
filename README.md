Software Machine
================

#Changelog v1.4.1
+ Added support for subroutines
+ Added 'call' instruction
+ Added 'ret' instruction
+ Added option for user to choose location of stack

#Changelog v1.3.2
+ Added 'sp' button
+ Removed currentInstruction textbox
+ Redesigned UI

#Changelog v1.3.1
+ Added stack support
+ Has a stack pointer register (initialized; not modifiable)
+ Added 'push' instruction
+ Added 'pop' instruction

#Changelog v.1.3.0 (Initial Upload)
+ Designed UI
+ Has instructions : neg, and, xor, or, lsr, lsl, asr, tst, ror, rol, hlt, movb, mov, cmp, jmp, add, sub
+ Has registers (modifiable) : r0, r1, r2, r3, r4, r5, r6, r7
+ Has registers (not modifiable) : pc, flags (ZEGV)
+ Has memory view (memory cells are modifiable)
+ Has code-box
+ Shortcuts :
    + ctrl+o : open mc file
    + ctrl+r : refresh memory cells from code-box
    + ctrl+q : quit
