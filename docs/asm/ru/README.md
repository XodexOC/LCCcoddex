# Assembly — уровни 00-10

Обзор трека Assembly для x86-64 Linux с NASM.

| Уровень | Тема | Описание |
|:-------:|------|----------|
| 00 | Как работает компьютер | Биты, байты, hex, регистры CPU, RAM, инструкции, ассемблер и линкер |
| 01 | Первая программа: syscall | `exit(0)`, `hello.asm`, секции .data/.text, syscall write |
| 02 | Регистры и mov | RAX/EAX/AX/AL/AH, mov imm/reg/память, адрес vs значение |
| 03 | Арифметика | `add`/`sub`/`inc`/`dec`, `mul`/`imul`, `div`/`idiv`, флаги ZF/CF/SF/OF |
| 04 | Память и .data | `db`/`dw`/`dd`/`dq`/`resb`, метки, массивы, `equ`/`$` |
| 05 | Режимы адресации | прямая, косвенная, base+disp, индексная, полная, LEA |
| 06 | Сравнение и переходы | `cmp`, `test`, условные jump'ы, if/else/while/for |
| 07 | Стек и подпрограммы | `push`/`pop`, `call`/`ret`, стековый фрейм, локальные переменные, рекурсия |
| 08 | Соглашение о вызовах | System V AMD64 ABI: аргументы, caller/callee-saved, выравнивание стека |
| 09 | Строки и REP | `lodsb`/`stosb`/`movsb`/`scasb`/`cmpsb`, `rep`/`repe`/`repne`, strlen/strcpy |
| 10 | Capstone: C + Assembly | `extern`/`global`, вызов C из asm, вызов asm из C, `printf`, inline asm |