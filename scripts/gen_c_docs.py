#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate expanded beginner-friendly C docs (ru + en). Documentation style, not homework."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RU = ROOT / "docs" / "c" / "ru"
EN = ROOT / "docs" / "c" / "en"

# Each entry: (slug, title_ru, title_en, body_ru, body_en)


def wrap(level, title, body, lang, slug):
    track = "Программирование на C" if lang == "ru" else "C Programming"
    return f"""# [{level}/10] {title}

> **Track:** {track} · **Level:** {level} · **Slug:** `{slug}`  
> {"Мягкая документация для полного нуля: что это, зачем, когда, примеры кода." if lang == "ru" else "Gentle documentation for absolute beginners: what, why, when, code examples."}

{body.strip()}

---
{"*Дальше по треку C — следующий номер в этой папке.*" if lang == "ru" else "*Continue with the next numbered lesson in this folder.*"}
"""


LESSONS = []

# ========== 0 ==========
LESSONS.append((
"00-hello-world",
"Самая первая программа и что такое «скомпилировать»",
"Your first program and what compile means",
r'''
## Зачем этот уровень

Прежде чем учить переменные и указатели, нужно спокойно понять **что происходит**, когда человек «пишет программу на C». Здесь нет сложных идей — только картина целиком.

## Что такое программа

**Программа** — текст, в котором по правилам языка C описано, что должен сделать компьютер. Текст обычно лежит в файле с расширением `.c` (например `hello.c`).

Компьютер **не понимает** `.c` «как есть». Он понимает **машинный код** — низкоуровневые инструкции процессора. Нужен посредник:

| Роль | Простыми словами |
|------|------------------|
| **Исходный код** | То, что пишешь ты (текст `.c`) |
| **Компилятор** | Программа-переводчик текста в машинный код |
| **Исполняемый файл** | Готовый результат (например `hello`) |
| **Запуск** | Система загружает файл и выполняет его |

На Xodex компилятор C — **`gcc`**.

## Самый маленький пример

Файл `hello.c`:

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, Xodex\n");
    return 0;
}
```

### `#include <stdio.h>`

Просьба: «подключи описание стандартных функций ввода-вывода».

- `stdio` = standard input/output
- Функция `printf` описана именно там
- Угловые скобки `<...>` — искать в системных каталогах заголовков

### `int main(void)`

**`main`** — особая функция. С неё **начинается** выполнение обычной консольной программы.

- `int` — тип возвращаемого значения (программа отдаёт число системе)
- `(void)` — параметров нет

### Фигурные скобки `{ ... }`

Тело функции: «вот что делать».

### `printf("Hello, Xodex\n");`

Печать в терминал.

- `"..."` — **строка** (текст)
- `\n` — символ **новой строки** (не две отдельные буквы)
- `;` в C **заканчивает** оператор. Забыть `;` — частая первая ошибка

### `return 0;`

Код завершения для операционной системы. `0` обычно значит «успех».

## Как из текста сделать программу

```bash
cd /usr/local/xodex/examples/c/hello
gcc -Wall -Wextra -o hello hello.c
./hello
```

| Часть | Смысл |
|-------|--------|
| `gcc` | компилятор |
| `-Wall -Wextra` | больше полезных предупреждений |
| `-o hello` | имя результата (**o**utput) |
| `hello.c` | исходник |
| `./hello` | запуск файла **из текущей папки** |

Ожидаемый вывод:

```text
Hello, Xodex
```

## Что делает gcc (упрощённо)

1. **Препроцессор** — `#include`, `#define`, …
2. **Компиляция** — C → объектный код
3. **Линковка** — склейка со стандартной библиотекой (там живёт `printf`)

Мантра уровня 0: **исходник → gcc → программа → запуск**.

## Частые ошибки

| Сообщение / симптом | Частая причина |
|---------------------|----------------|
| `expected ';' ...` | забыли `;` |
| `No such file` при `./hello` | не скомпилировали или не та папка |
| Кракозябры | кодировка; на Xodex удобен UTF-8 |

## Редакторы на Xodex

`nano`, `vim`/`nvim`, `mcedit` (из `mc`). Важнее освоить цикл «написал → скомпилировал → запустил», чем выбрать идеальный редактор.

## Мини-словарь

| Термин | Смысл |
|--------|--------|
| Исходный код | текст программы |
| Компилятор | переводчик в машинный код |
| Бинарник | готовая к запуску программа |
| Терминал | текстовое окно команд |
| Библиотека | уже написанный чужой код |
| Заголовок `.h` | описание доступных функций |

## Куда смотреть

- `/usr/local/xodex/examples/c/hello/hello.c`
- `man 3 printf` — справка по `printf` (раздел 3 — библиотека)

## Дальше по смыслу

Уровень 1 — **переменные и типы**: зачем программе «коробки» для чисел.
''',
r'''
## Why this level exists

Before variables and pointers, get a calm picture of **what happens** when someone writes a C program.

## What a program is

A **program** is text describing what the computer should do. It usually lives in a `.c` file.

The CPU does not run `.c` text directly. A **compiler** translates source into an **executable**. On Xodex that compiler is **`gcc`**.

| Role | Plain words |
|------|-------------|
| Source code | Your `.c` text |
| Compiler | Translator to machine code |
| Executable | Runnable file |
| Run | OS loads and executes it |

## Smallest example

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, Xodex\n");
    return 0;
}
```

- `#include <stdio.h>` — declarations for standard I/O (`printf`)
- `main` — entry point of a normal console program
- `printf` — print text; `\n` is newline; `;` ends the statement
- `return 0` — success exit status for the OS

## Compile and run

```bash
cd /usr/local/xodex/examples/c/hello
gcc -Wall -Wextra -o hello hello.c
./hello
```

`-Wall -Wextra` enable useful warnings. `-o hello` names the output. `./hello` runs the file in the current directory.

## Inside gcc (simplified)

Preprocessor → compile → link with the standard library.

Mantra: **source → gcc → program → run**.

## Common mistakes

Missing `;`, wrong directory, forgot to compile, encoding issues.

## Editors

`nano`, `vim`/`nvim`, `mcedit`. The edit → compile → run loop matters most.

## See also

`/usr/local/xodex/examples/c/hello/hello.c`, `man 3 printf`

## Next topic

Level 1 — variables and types.
''',
))

# ========== 1 ==========
LESSONS.append((
"01-variables-types",
"Переменные и типы: коробки для данных",
"Variables and types: boxes for data",
r'''
## Идея

Программе нужно **запоминать** значения. В C для этого есть **переменные**.

Переменная — как **коробка** с:

1. **именем** (как обращаться),
2. **типом** (что можно хранить),
3. **значением** (что лежит сейчас).

```c
int score;        /* объявили коробку */
score = 10;       /* положили 10 */
score = 11;       /* теперь 11; старое забыто */
int lives = 3;    /* объявление сразу с значением */
```

Знак `=` — это **присваивание** («положить в коробку»), а не «равно» из школьного уравнения. Для сравнения позже будет `==`.

## Зачем типы

Память — байты. Тип говорит компилятору:

- сколько байт занять,
- как понимать биты,
- какие операции допустимы.

| Тип | Обычно хранит | Частый размер* |
|-----|----------------|----------------|
| `char` | символ / маленькое целое | 1 байт |
| `int` | целое | 4 байта |
| `long` | целое «пошире» | 4 или 8 |
| `float` | дробное приближённо | 4 |
| `double` | дробное точнее | 8 |

\*Зависит от платформы. Проверка:

```c
#include <stdio.h>

int main(void)
{
    printf("char=%zu int=%zu long=%zu double=%zu\n",
           sizeof(char), sizeof(int), sizeof(long), sizeof(double));
    return 0;
}
```

`sizeof` возвращает размер в байтах. `%zu` — удобный формат для этого значения.

## Целые: знаковые и беззнаковые

- `int` по умолчанию **signed** — бывают отрицательные
- `unsigned int` — только ≥ 0

```c
unsigned char c = 255;
c = c + 1;   /* для unsigned: снова 0 (обёртка по модулю) */
```

Переполнение **signed** `int` в стандарте C — *undefined behavior* (нельзя на него опираться). У `unsigned` переполнение определено.

## Дроби приблизительные

```c
double x = 0.1 + 0.2;
printf("%.20f\n", x);  /* часто не «идеальные» 0.3 */
```

Так устроена двоичная floating-point арифметика, это не «поломка» твоего ПК.

## Символы

```c
char letter = 'A';   /* одинарные кавычки — один символ */
```

`'A'` и `"A"` — разное:

- `'A'` — один `char`
- `"A"` — **строка** (про строки будет отдельный уровень)

## Имена

Можно буквы, цифры, `_`. Нельзя начинать с цифры. Регистр важен: `Score` ≠ `score`.

Понятные имена сильно помогают:

```c
int n;               /* через неделю непонятно */
int apple_count;     /* лучше */
```

## Печать разных типов

```c
#include <stdio.h>

int main(void)
{
    int a = 42;
    double p = 3.5;
    char ch = 'Z';

    printf("a=%d\n", a);
    printf("p=%.2f\n", p);
    printf("ch=%c\n", ch);
    return 0;
}
```

| Спецификатор | Тип (типично) |
|--------------|----------------|
| `%d` | `int` |
| `%u` | `unsigned int` |
| `%ld` | `long` |
| `%f` | `double` |
| `%c` | `char` как символ |
| `%s` | строка |
| `%zu` | `sizeof` / `size_t` |

Неверный спецификатор — частая причина «странных чисел» на экране.

## Полный пример

```c
#include <stdio.h>

int main(void)
{
    int apples = 3;
    int more = 2;
    int total = apples + more;

    printf("apples=%d more=%d total=%d\n", apples, more, total);
    return 0;
}
```

## Типичные ловушки

1. Читать переменную **до** первого присваивания (в коробке мусор).
2. Перепутать `=` и `==`.
3. Скормить `printf` не тот формат.
4. Ждать от `float`/`double` школьной «идеальной» точности.

## Связь с памятью (задел)

Локальная переменная занимает место (часто на **стеке**). Адрес этой коробки — тема **указателей** (уровень 4).

## Дальше

Уровень 2 — **условия и циклы**.
''',
r'''
## The idea

A **variable** is a named box with a **type** and a **value**.

```c
int score = 10;
score = 11; /* assignment */
```

`=` stores a value. Comparison later uses `==`.

## Why types

Types describe size and meaning of bytes: `char`, `int`, `long`, `float`, `double`. Use `sizeof` because sizes can vary by platform.

## Signed vs unsigned

Signed may be negative. Unsigned are ≥ 0. Prefer not relying on signed overflow.

## Floating point is approximate

`0.1 + 0.2` may not print as exact `0.3`.

## Characters vs strings

```c
char letter = 'A'; /* one character */
/* "A" is a string — later lesson */
```

## printf helpers

`%d` int, `%f` double, `%c` char, `%s` string, `%zu` size_t.

```c
#include <stdio.h>
int main(void) {
    int apples = 3, more = 2;
    printf("total=%d\n", apples + more);
    return 0;
}
```

## Common traps

Uninitialized variables, `=` vs `==`, wrong format specifiers, exact float expectations.

## Next

Level 2 — conditions and loops.
''',
))

# ========== 2 ==========
LESSONS.append((
"02-control-flow",
"Условия и циклы: выбор и повторение",
"Conditions and loops: choice and repetition",
r'''
## Зачем

Программы не только идут сверху вниз. Они:

- **выбирают** ветку («если … иначе …»),
- **повторяют** действия («пока …»).

## Условие if

```c
#include <stdio.h>

int main(void)
{
    int temperature = 30;

    if (temperature > 25) {
        printf("Warm\n");
    } else {
        printf("Not warm\n");
    }
    return 0;
}
```

В C **ложь** — это `0`, **истина** — любое ненулевое значение.  
Фигурные скобки лучше ставить всегда — меньше случайных ошибок.

## Операторы сравнения и логики

| Оператор | Смысл |
|----------|--------|
| `==` | равно |
| `!=` | не равно |
| `< > <= >=` | сравнения |
| `&&` | логическое И |
| `\|\|` | логическое ИЛИ |
| `!` | НЕ |

Важно:

```c
if (x = 5)  { /* почти наверняка ошибка: это ПРИСВАИВАНИЕ */ }
if (x == 5) { /* сравнение */ }
```

## else if

```c
if (score >= 90) {
    printf("A\n");
} else if (score >= 75) {
    printf("B\n");
} else {
    printf("C or below\n");
}
```

## switch

Удобен, когда значение — один из дискретных вариантов:

```c
switch (day) {
case 1:
    printf("Mon\n");
    break;
case 2:
    printf("Tue\n");
    break;
default:
    printf("Other\n");
    break;
}
```

Без `break` выполнение «проваливается» в следующий `case`.

## Цикл while

```c
int i = 0;
while (i < 5) {
    printf("%d\n", i);
    i = i + 1;  /* или i++ */
}
```

Если забыть менять условие, цикл может стать **бесконечным**.

## Цикл for

```c
for (int i = 0; i < 5; i++) {
    printf("%d\n", i);
}
```

Три части: **инициализация** (один раз) ; **условие** (перед каждой итерацией) ; **шаг** (после тела).

## Остаток от деления `%`

```c
int r = 10 % 3;  /* r == 1 */
```

`i % 3 == 0` значит «делится на 3 нацело».

## Пример: сумма 1..N

```c
#include <stdio.h>

int main(void)
{
    int n = 10;
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i; /* sum = sum + i */
    }
    printf("sum=%d\n", sum);
    return 0;
}
```

## Пример: FizzBuzz (как иллюстрация условий)

Идея: для чисел 1…100 печатать `Fizz` / `Buzz` / `FizzBuzz` / число:

```c
#include <stdio.h>

int main(void)
{
    for (int i = 1; i <= 100; i++) {
        if (i % 3 == 0 && i % 5 == 0) {
            printf("FizzBuzz\n");
        } else if (i % 3 == 0) {
            printf("Fizz\n");
        } else if (i % 5 == 0) {
            printf("Buzz\n");
        } else {
            printf("%d\n", i);
        }
    }
    return 0;
}
```

Это не «задание ради задания», а **живой пример** сочетания цикла и нескольких `if`.

## break и continue

- `break` — выйти из цикла
- `continue` — перейти к следующей итерации

## Стиль

Понятные условия, скобки всегда, не стесняйся промежуточных переменных с ясными именами.

## Дальше

Уровень 3 — **функции**.
''',
r'''
## Why

Programs choose branches and repeat work.

## if / else

```c
if (temperature > 25) {
    printf("Warm\n");
} else {
    printf("Not warm\n");
}
```

`0` is false; non-zero is true. Use `==` to compare, `=` to assign.

Logic: `&&` (and), `||` (or), `!` (not).

## while / for

```c
int i = 0;
while (i < 5) {
    printf("%d\n", i);
    i++;
}

for (int j = 0; j < 5; j++) {
    printf("%d\n", j);
}
```

## Remainder

`i % 3 == 0` means divisible by 3. Useful in patterns like FizzBuzz:

```c
for (int i = 1; i <= 100; i++) {
    if (i % 3 == 0 && i % 5 == 0) printf("FizzBuzz\n");
    else if (i % 3 == 0) printf("Fizz\n");
    else if (i % 5 == 0) printf("Buzz\n");
    else printf("%d\n", i);
}
```

## break / continue

Leave the loop, or skip to the next iteration.

## Next

Level 3 — functions.
''',
))

# ========== 3 ==========
LESSONS.append((
"03-functions",
"Функции: именованные куски смысла",
"Functions: named pieces of meaning",
r'''
## Зачем

**Функция** — именованный фрагмент кода, который можно вызывать снова и снова.

Зачем так делают:

- не копировать один и тот же текст,
- дать действию понятное **имя**,
- читать программу по частям.

Ты уже знаком с **`main`** — это тоже функция.

## Анатомия

```c
#include <stdio.h>

int add(int a, int b);   /* прототип: «такая функция есть» */

int main(void)
{
    int result = add(2, 3);
    printf("%d\n", result);
    return 0;
}

int add(int a, int b)    /* определение */
{
    return a + b;
}
```

| Часть | Пример | Смысл |
|-------|--------|--------|
| Тип возврата | `int` | что отдаём наружу |
| Имя | `add` | как вызывать |
| Параметры | `int a, int b` | что принимаем |
| `return` | `return a + b;` | результат |

Если возвращать нечего:

```c
void greet(void)
{
    printf("Hi\n");
}
```

## Передача по значению

В C в параметры попадает **копия**:

```c
void try_change(int x)
{
    x = 100; /* меняется копия */
}

int main(void)
{
    int n = 1;
    try_change(n);
    /* n всё ещё 1 */
    return 0;
}
```

Чтобы менять «чужую» переменную, понадобятся **указатели** (уровень 4).

## Локальные переменные

Объявленные внутри функции видны только там и живут, пока идёт вызов.

## Рекурсия и итерация

```c
int factorial(int n)
{
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int factorial_iter(int n)
{
    int r = 1;
    for (int i = 2; i <= n; i++) r *= i;
    return r;
}
```

Рекурсия — когда функция вызывает себя. Нужен **случай остановки**. Итерация часто проще для старта.

## Стек вызовов (интуиция)

Каждый вызов кладёт на «стопку» (stack) данные: куда вернуться, параметры, локальные. Слишком глубокая рекурсия может переполнить стек.

## Прототипы

Компилятор читает файл сверху вниз. Если вызов раньше определения — нужен прототип. В больших проектах прототипы живут в `.h` (уровень 9).

## Пример с несколькими функциями

```c
#include <stdio.h>

int max2(int a, int b)
{
    if (a > b) return a;
    return b;
}

void print_max(int a, int b)
{
    printf("max=%d\n", max2(a, b));
}

int main(void)
{
    print_max(10, 3);
    print_max(-1, -5);
    return 0;
}
```

## Привычки

Имена-действия (`compute_total`), одна ясная ответственность, умеренный размер функции.

## Дальше

Уровень 4 — **указатели**.
''',
r'''
## Why functions exist

A **function** is a reusable named block of code. `main` is one of them.

```c
int add(int a, int b) {
    return a + b;
}
```

Arguments are passed **by value** (copies). Locals live only during the call.

```c
void try_change(int x) { x = 100; }
/* caller variable stays unchanged */
```

Prototypes tell the compiler a function exists before it is defined. Recursion needs a base case; iteration is often clearer at first.

**Call stack** intuition: each call pushes a frame; return pops it.

## Next

Level 4 — pointers.
''',
))

# ========== 4 ==========
LESSONS.append((
"04-pointers",
"Указатели: адреса переменных",
"Pointers: addresses of variables",
r'''
## Самая важная идея C

Переменная лежит **где-то в памяти**. У этого места есть **адрес** (номер «ячейки»).

**Указатель** — переменная, которая хранит **адрес** другой переменной (или «никуда» — `NULL`).

```text
  имя: score          имя: p
  значение: 42        значение: адрес score
  адрес: 0x7ffc...    
```

## Операторы & и *

```c
#include <stdio.h>

int main(void)
{
    int score = 42;
    int *p = &score;   /* p хранит адрес score */

    printf("score=%d\n", score);
    printf("p points to %d\n", *p);  /* разыменование: «сходи по адресу» */

    *p = 100;          /* записали в score через указатель */
    printf("score now=%d\n", score);
    return 0;
}
```

| Запись | Читать как |
|--------|------------|
| `int *p` | «p — указатель на int» |
| `&score` | «адрес переменной score» |
| `*p` | «значение там, куда указывает p» |

Звёздочка в объявлении и звёздочка при использовании — связанный, но разный контекст. Новичкам помогает проговаривать вслух.

## Зачем это нужно

1. Функция может **изменить** переменную вызывающего (через адрес).
2. Удобно работать с **массивами** и строками (они тесно связаны с указателями).
3. Динамическая память (`malloc`) возвращает указатель (уровень 6).
4. Структуры и «объекты» в C-стиле часто передают по указателю.

## Пример: обмен двух чисел

```c
#include <stdio.h>

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int main(void)
{
    int x = 3, y = 7;
    swap(&x, &y);
    printf("x=%d y=%d\n", x, y);  /* 7 3 */
    return 0;
}
```

Без указателей `swap(int a, int b)` менял бы только копии — снаружи `x` и `y` остались бы прежними.

## NULL

```c
int *p = NULL;  /* «ни на что не указывает» */
```

Разыменовывать `NULL` нельзя — это ошибка (часто падение программы). Перед использованием указателя извне иногда проверяют `if (p != NULL)`.

## Указатель и тип

`int *` и `char *` — разные типы. Адрес «смотрит» на объект определённого типа; от типа зависит, как работает **арифметика указателей** (уровень 5, массивы).

## Частые ошибки

1. Забыли `&` при передаче в `swap`.
2. Разыменовали неинициализированный указатель (мусорный адрес).
3. Вернули из функции адрес **локальной** переменной (после `return` её уже нет — висячий указатель).
4. Перепутали `*` и `&`.

## Печать адреса (для любопытства)

```c
printf("%p\n", (void *)p);
```

`%p` — формат для указателя. На разных запусках адреса могут отличаться (это нормально).

## Мягкая аналогия

Квартира = переменная, **адрес дома** = pointer, «открой дверь по адресу» = `*p`.  
Можно передать другу **адрес**, чтобы он сам положил вещи в квартиру — это `swap` и подобные функции.

## Дальше

Уровень 5 — **массивы и строки** (и почему массив «похож» на указатель).
''',
r'''
## Core idea

Every variable lives somewhere in memory and has an **address**.  
A **pointer** stores an address.

```c
int score = 42;
int *p = &score;  /* address of score */
*p = 100;         /* write through the pointer → score becomes 100 */
```

| Syntax | Meaning |
|--------|---------|
| `int *p` | p points to int |
| `&score` | address of score |
| `*p` | value at that address |

## Why pointers exist

- Let functions modify caller variables
- Work with arrays/strings
- Dynamic allocation returns pointers
- Pass large structs efficiently

## swap example

```c
void swap(int *a, int *b) {
    int t = *a; *a = *b; *b = t;
}
/* call: swap(&x, &y); */
```

Without pointers, only copies would change.

## NULL

`NULL` means “points nowhere”. Do not dereference it.

## Common mistakes

Missing `&`, uninitialized pointers, returning address of a local, mixing up `*` and `&`.

## Next

Level 5 — arrays and strings.
''',
))

# ========== 5 ==========
LESSONS.append((
"05-arrays-strings",
"Массивы и строки C",
"Arrays and C strings",
r'''
## Массив

**Массив** — несколько элементов **одного типа** подряд в памяти.

```c
int a[5];           /* 5 элементов int, пока без явных значений */
int b[5] = {1, 2, 3, 4, 5};
int c[]  = {10, 20, 30};  /* размер 3 посчитается сам */
```

Индексация **с нуля**:

```c
b[0] == 1;
b[4] == 5;
/* b[5] — уже за границей: нельзя */
```

Выход за границу массива в C **не проверяется** автоматически. Это источник серьёзных ошибок (переполнение буфера).

## Связь с указателями

Имя массива в большинстве выражений **превращается** (decay) в указатель на первый элемент:

```c
int b[5] = {1, 2, 3, 4, 5};
int *p = b;      /* то же, что &b[0] */
printf("%d\n", p[2]);  /* 3 */
printf("%d\n", *(p + 2)); /* тоже 3 */
```

Арифметика указателей: `p + 1` сдвигает на **следующий int**, а не на «+1 байт».

## Передача массива в функцию

```c
#include <stdio.h>

/* размер сам «не приедет»: передай length отдельно */
int sum(const int *arr, int length)
{
    int s = 0;
    for (int i = 0; i < length; i++) {
        s += arr[i];
    }
    return s;
}

int main(void)
{
    int xs[] = {1, 2, 3, 4};
    printf("%d\n", sum(xs, 4));
    return 0;
}
```

`const` здесь — обещание «не менять элементы через этот указатель».

## Строки в C

Строка — это массив `char`, где конец отмечен символом **`'\0'`** (нулевой байт), не путать с `'0'`.

```c
char hi[] = "Hi";
/* в памяти: 'H', 'i', '\0'  → длина текста 2, занято байт 3 */
```

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[32] = "Xodex";
    printf("len=%zu\n", strlen(name));
    printf("%s\n", name);
    return 0;
}
```

`strlen` считает символы **до** `'\0'`, не включая его.

## Осторожно с копированием

```c
char dest[8];
/* strcpy(dest, "too long string");  — опасно, если не влезает */
```

Предпочтительнее ограничивать размер (идея `snprintf` / аккуратный копирующий код). Старый `gets` — **никогда**.

## Пример: разворот строки на месте

```c
#include <stdio.h>
#include <string.h>

void reverse(char *s)
{
    size_t n = strlen(s);
    for (size_t i = 0; i < n / 2; i++) {
        char t = s[i];
        s[i] = s[n - 1 - i];
        s[n - 1 - i] = t;
    }
}

int main(void)
{
    char buf[] = "abcd";
    reverse(buf);
    printf("%s\n", buf);  /* dcba */
    return 0;
}
```

## Частые ловушки

1. Забыть место под `'\0'`.
2. Путать длину строки и размер массива (`sizeof`).
3. `sizeof(arr)` **внутри функции** после передачи указателя **не** даёт размер массива вызывающего — только размер указателя.
4. Запись за концом буфера.

## Дальше

Уровень 6 — **динамическая память** (`malloc` / `free`).
''',
r'''
## Arrays

An array is consecutive elements of one type:

```c
int b[5] = {1, 2, 3, 4, 5};
/* indexes 0..4 ; b[5] is out of bounds */
```

C does **not** bounds-check for you.

## Arrays and pointers

The array name often decays to a pointer to the first element. `p + 1` advances by one element, not one byte.

When passing arrays to functions, pass the **length** separately.

## C strings

A string is a `char` array ending with `'\0'`.

```c
char name[32] = "Xodex";
printf("%s\n", name);
```

`strlen` counts until `'\0'`. Prefer size-aware copying over unbounded `strcpy`. Never use `gets`.

## Next

Level 6 — dynamic memory.
''',
))

# ========== 6 ==========
LESSONS.append((
"06-memory",
"Динамическая память: malloc и free",
"Dynamic memory: malloc and free",
r'''
## Зачем куча (heap)

Локальные массивы удобны, когда размер **известен** и невелик. Иногда размер известен только **во время работы** программы, или данных много.

Тогда используют **динамическую память**:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n = 10;
    int *a = malloc(n * sizeof *a);
    if (a == NULL) {
        printf("malloc failed\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        a[i] = i * i;
    }
    printf("a[3]=%d\n", a[3]);

    free(a);     /* отдать память обратно */
    a = NULL;    /* хорошая гигиена: не держать старый адрес */
    return 0;
}
```

## Семейство функций

| Функция | Смысл |
|---------|--------|
| `malloc(size)` | выделить `size` байт (содержимое не определено) |
| `calloc(n, size)` | выделить и **заполнить нулями** |
| `realloc(ptr, size)` | изменить размер блока |
| `free(ptr)` | освободить блок |

Всегда проверяй результат `malloc`/`calloc` на `NULL`.

## Правила владения

1. Каждый успешный `malloc` (в итоге) — **ровно один** `free`.
2. Нельзя делать `free` дважды одному адресу.
3. Нельзя использовать память после `free`.
4. Нельзя `free` то, что не из `malloc` (например адрес локальной переменной).

Кто выделил — тот обычно и освобождает, либо в документации ясно сказано иное.

## Утечки

Если забыть `free`, память «теряется» до конца процесса. В коротких учебных программах ОС всё подчистит при выходе, но привычка **освобождать** важна для настоящих программ.

На Xodex помогает **valgrind**:

```bash
gcc -g -o prog prog.c
valgrind --leak-check=full ./prog
```

## Пример: «динамический массив» чисел (идея)

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int size;     /* сколько элементов занято */
    int capacity; /* сколько выделено */
} IntArray;

void ia_init(IntArray *a)
{
    a->data = NULL;
    a->size = 0;
    a->capacity = 0;
}

int ia_push(IntArray *a, int value)
{
    if (a->size >= a->capacity) {
        int newcap = (a->capacity == 0) ? 4 : a->capacity * 2;
        int *p = realloc(a->data, newcap * sizeof *p);
        if (!p) return -1;
        a->data = p;
        a->capacity = newcap;
    }
    a->data[a->size++] = value;
    return 0;
}

void ia_free(IntArray *a)
{
    free(a->data);
    a->data = NULL;
    a->size = a->capacity = 0;
}
```

(Использование структур — уровень 7; здесь видно, *зачем* они рядом с памятью.)

## Частые ошибки

Утечки, double-free, use-after-free, неверный размер (`malloc(n)` вместо `malloc(n * sizeof *p)` для массива `int`).

## Дальше

Уровень 7 — **структуры** и раскладка данных в памяти.
''',
r'''
## Why the heap exists

When size is known only at runtime, use dynamic memory:

```c
int *a = malloc(n * sizeof *a);
if (!a) { /* handle failure */ }
/* use a[i] ... */
free(a);
a = NULL;
```

## Family

`malloc`, `calloc` (zeroed), `realloc`, `free`. Always check for `NULL`.

## Ownership rules

One `free` per successful allocation; no double-free; no use-after-free; only free malloc’d pointers.

Valgrind helps find leaks:

```bash
gcc -g -o prog prog.c
valgrind --leak-check=full ./prog
```

## Next

Level 7 — structs and memory layout.
''',
))

# ========== 7 ==========
LESSONS.append((
"07-structs",
"Структуры: несколько полей вместе",
"Structs: fields together",
r'''
## Зачем struct

Иногда данные логически связаны: точка `(x, y)`, студент (имя + балл), прямоугольник…

**Структура** склеивает поля под одним типом.

```c
#include <stdio.h>

struct Point {
    int x;
    int y;
};

int main(void)
{
    struct Point p;
    p.x = 3;
    p.y = 4;
    printf("(%d,%d)\n", p.x, p.y);
    return 0;
}
```

Точка `.` — доступ к полю.

## typedef — короткое имя

```c
typedef struct {
    int x;
    int y;
} Point;

Point p = {3, 4};
```

(В учебном коде оба стиля встречаются.)

## Указатель на структуру

```c
void move(Point *p, int dx, int dy)
{
    p->x += dx;   /* то же, что (*p).x */
    p->y += dy;
}
```

`->` читается: «по указателю возьми поле».

## Вложенность

```c
typedef struct {
    Point top_left;
    Point bottom_right;
} Rect;

int width(const Rect *r)
{
    return r->bottom_right.x - r->top_left.x;
}
```

## Padding и sizeof

Компилятор может вставлять **пустые байты** между полями для выравнивания. Поэтому `sizeof(struct ...)` не всегда равен сумме sizeof полей.

Порядок полей влияет на итоговый размер. Для отладки раскладки смотрят `offsetof` из `<stddef.h>`.

## Opaque pointer (идея API)

В заголовке можно показать только «есть тип `struct Foo`», а поля спрятать в `.c`. Тогда пользователи библиотеки работают через указатели и функции — меньше связанности и безопаснее изменения внутри.

## Пример

```c
#include <stdio.h>

typedef struct {
    int x, y;
} Point;

typedef struct {
    Point tl, br;
} Rect;

int area(const Rect *r)
{
    int w = r->br.x - r->tl.x;
    int h = r->br.y - r->tl.y;
    if (w < 0) w = -w;
    if (h < 0) h = -h;
    return w * h;
}

int main(void)
{
    Rect r = {{0, 0}, {10, 5}};
    printf("area=%d sizeof(Rect)=%zu\n", area(&r), sizeof r);
    return 0;
}
```

## Дальше

Уровень 8 — **файлы и ввод-вывод**.
''',
r'''
## Why structs

Group related fields under one type:

```c
typedef struct { int x, y; } Point;
Point p = {3, 4};
```

`.` accesses a field; `->` accesses through a pointer (`p->x` is `(*p).x`).

`sizeof` may include **padding** for alignment; field order can change size.

## Next

Level 8 — files and I/O.
''',
))

# ========== 8 ==========
LESSONS.append((
"08-files-io",
"Файлы и ввод-вывод",
"Files and I/O",
r'''
## Потоки FILE*

В C стандартный способ работы с файлами — тип **`FILE*`** из `<stdio.h>`.

Уже знакомые потоки:

| Поток | Смысл |
|-------|--------|
| `stdin` | ввод (клавиатура по умолчанию) |
| `stdout` | обычный вывод |
| `stderr` | вывод ошибок |

## Открыть / читать / писать / закрыть

```c
#include <stdio.h>

int main(void)
{
    FILE *f = fopen("note.txt", "w");
    if (f == NULL) {
        perror("fopen");
        return 1;
    }
    fprintf(f, "Hello file\n");
    fclose(f);
    return 0;
}
```

Режимы (основные):

| Режим | Смысл |
|-------|--------|
| `"r"` | чтение |
| `"w"` | запись (создать/очистить) |
| `"a"` | дописать в конец |
| `"rb"` `"wb"` | бинарные варианты |

## Чтение построчно

```c
char line[256];
FILE *f = fopen("note.txt", "r");
if (!f) {
    perror("fopen");
    return 1;
}
while (fgets(line, sizeof line, f) != NULL) {
    printf("%s", line);
}
fclose(f);
```

`fgets` безопаснее «бесконечного» чтения: размер буфера ограничен.

## Копирование байтами (идея)

```c
int c;
while ((c = fgetc(in)) != EOF) {
    fputc(c, out);
}
```

`EOF` — признак конца файла / ошибки (уточняют через `feof` / `ferror` при необходимости).

## perror и errno

При ошибках системных/библиотечных вызовов:

```c
perror("fopen");  /* печать понятного сообщения */
```

## Текст и бинарь

В текстовом режиме возможны преобразования переводов строк (зависит от платформы). Для точных байтов используют бинарные режимы.

## Дескрипторы (задел)

Под `FILE*` на Unix часто лежат **файловые дескрипторы** и системные вызовы `open`/`read`/`write`. Сначала удобно освоить stdio; низкий уровень — когда понадобится контроль.

## Дальше

Уровень 9 — **препроцессор и Make**: как собирать проект из нескольких файлов.
''',
r'''
## FILE* streams

```c
FILE *f = fopen("note.txt", "w");
if (!f) { perror("fopen"); return 1; }
fprintf(f, "Hello file\n");
fclose(f);
```

Modes: `"r"`, `"w"`, `"a"`, binary variants `"rb"` / `"wb"`.

Read lines with `fgets` (bounded buffer). Use `perror` on failure.

## Next

Level 9 — preprocessor and Make.
''',
))

# ========== 9 ==========
LESSONS.append((
"09-preprocessor-make",
"Препроцессор и сборка Make",
"Preprocessor and Make",
r'''
## Препроцессор

Строки, начинающиеся с `#`, обрабатываются **до** настоящей компиляции.

### #include

```c
#include <stdio.h>   /* системный заголовок */
#include "point.h"   /* свой заголовок рядом с проектом */
```

### #define

```c
#define MAX_SIZE 100
#define SQUARE(x) ((x) * (x))  /* скобки важны в макросах */
```

Макросы «текстово подставляются» и бывают коварны. Для констант в современном C часто предпочитают `enum` или `static const`.

### Include guards

Чтобы заголовок не вставился дважды:

```c
#ifndef POINT_H
#define POINT_H

typedef struct {
    int x, y;
} Point;

#endif
```

## Несколько файлов

`point.h` — объявления:

```c
#ifndef POINT_H
#define POINT_H
typedef struct { int x, y; } Point;
int point_manhattan(Point a, Point b);
#endif
```

`point.c` — реализация:

```c
#include "point.h"

int point_manhattan(Point a, Point b)
{
    int dx = a.x - b.x;
    int dy = a.y - b.y;
    if (dx < 0) dx = -dx;
    if (dy < 0) dy = -dy;
    return dx + dy;
}
```

`main.c`:

```c
#include <stdio.h>
#include "point.h"

int main(void)
{
    Point a = {0, 0}, b = {3, 4};
    printf("%d\n", point_manhattan(a, b));
    return 0;
}
```

Сборка вручную:

```bash
gcc -Wall -Wextra -c point.c
gcc -Wall -Wextra -c main.c
gcc -o app point.o main.o
```

## Makefile (идея)

```make
CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Werror -g

app: main.o point.o
	$(CC) $(CFLAGS) -o app main.o point.o

main.o: main.c point.h
	$(CC) $(CFLAGS) -c main.c

point.o: point.c point.h
	$(CC) $(CFLAGS) -c point.c

clean:
	rm -f app *.o
```

`make` пересоберёт только то, что изменилось (по датам файлов).

Флаги обучения:

- `-Wall -Wextra` — предупреждения
- `-Werror` — считать предупреждения ошибками (дисциплина)
- `-g` — отладочная информация для `gdb`

## Дальше

Уровень 10 — **системный C**: процессы, системные вызовы, связь с Linux.
''',
r'''
## Preprocessor

`#include` inserts headers. `#define` defines macros/constants. Use **include guards** in `.h` files.

## Multi-file programs

Headers declare; `.c` files define. Compile to `.o` then link.

## Make

A Makefile records dependencies so only changed parts rebuild. Useful flags: `-Wall -Wextra -Werror -g`.

## Next

Level 10 — systems C and the Linux boundary.
''',
))

# ========== 10 ==========
LESSONS.append((
"10-systems-c",
"Системный C: мост к Linux",
"Systems C: the bridge to Linux",
r'''
## Где C встречается с ОС

Большая часть «магии» Linux снаружи выглядит как функции. Часть из них — обёртки над **системными вызовами** (kernel API).

Грубо:

```text
твой код  →  libc (printf, malloc, ...)  →  kernel (read, write, fork, ...)
```

Справка:

- `man 2 ...` — системные вызовы
- `man 3 ...` — библиотечные функции

## Процессы (обзор)

**Процесс** — запущенная программа + её память + ресурсы.

Важные идеи (подробнее — трек **linux**):

| Вызов (идея) | Смысл |
|--------------|--------|
| `fork` | создать почти копию процесса |
| `exec` семейство | заменить программу в процессе |
| `wait` / `waitpid` | родитель дожидается завершения ребёнка |

## Мини-пример: идея простого launcher

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
    char line[256];

    printf("xodex-mini> ");
    if (!fgets(line, sizeof line, stdin)) {
        return 0;
    }
    line[strcspn(line, "\n")] = '\0';
    if (line[0] == '\0') {
        return 0;
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return 1;
    }
    if (pid == 0) {
        /* ребёнок */
        execlp(line, line, (char *)NULL);
        perror("exec");
        _exit(127);
    }
    /* родитель */
    int status = 0;
    waitpid(pid, &status, 0);
    return 0;
}
```

Это **иллюстрация**, не полноценный shell: без аргументов, пайпов, кавычек. Но по ней видно, как C склеивается с моделью процессов Unix.

## Сигналы (очень кратко)

Процессы могут получать **сигналы** (`SIGINT` при Ctrl+C и т.д.). Обработка сигналов — отдельная глубокая тема; на старте достаточно знать, что они существуют.

## Инструменты наблюдения

| Инструмент | Зачем |
|------------|--------|
| `gdb` | отладчик: точки останова, шаг, переменные |
| `strace` | какие syscall делает программа |
| `ltrace` | библиотечные вызовы (где доступно) |
| `valgrind` | память |

Пример:

```bash
gcc -g -o app app.c
strace ./app
gdb ./app
```

## Как продолжать расти

1. Читать `man` по мере встречи с новыми вызовами.
2. Писать маленькие программы, которые делают одну вещь.
3. Параллельно идти по треку **linux** (процессы, права, пайпы).
4. Сравнивать ментальную модель с **Rust** (ownership) — другой способ бороться с теми же классами ошибок.

## Что ты уже умеешь по треку C

| Уровень | Тема |
|--------:|------|
| 0 | компиляция и запуск |
| 1 | типы и переменные |
| 2 | условия и циклы |
| 3 | функции |
| 4 | указатели |
| 5 | массивы и строки |
| 6 | куча |
| 7 | структуры |
| 8 | файлы |
| 9 | многофайловая сборка |
| 10 | край ОС |

Дальше глубина растёт **практикой и чтением первоисточников**, а не «следующим секретным уровнем».
''',
r'''
## C meets the OS

Much of Linux functionality is reached through **libc** wrappers around **system calls**.

- `man 2` — syscalls  
- `man 3` — library functions  

## Processes (sketch)

`fork` clones a process; `exec*` replaces the program image; `waitpid` waits for a child. Together they build shells and launchers.

A tiny illustration (not a full shell): read a line, `fork`, child `execlp`, parent `waitpid`.

## Observation tools

`gdb` (debugger), `strace` (syscalls), `valgrind` (memory).

```bash
gcc -g -o app app.c
strace ./app
```

## Where to grow next

Read man pages as you go, write small programs, follow the **linux** track, compare with Rust’s ownership model.

You now have the full 0–10 C path: toolchain → language core → memory → structs/files/build → OS boundary.
''',
))


def main():
    RU.mkdir(parents=True, exist_ok=True)
    EN.mkdir(parents=True, exist_ok=True)

    rows_ru = []
    rows_en = []
    for i, (slug, tru, ten, bru, ben) in enumerate(LESSONS):
        level = int(slug.split("-")[0])
        (RU / f"{slug}.md").write_text(wrap(level, tru, bru, "ru", slug), encoding="utf-8")
        (EN / f"{slug}.md").write_text(wrap(level, ten, ben, "en", slug), encoding="utf-8")
        rows_ru.append(f"| {level} | [{tru}]({slug}.md) |")
        rows_en.append(f"| {level} | [{ten}]({slug}.md) |")
        print("wrote", slug)

    (RU / "README.md").write_text(
        "# Программирование на C — уровни 0–10\n\n"
        "Документация для **полного нуля**: что означает термин, зачем он нужен, "
        "когда встречается, и **примеры кода**. Без стиля «сделай задание №3».\n\n"
        "| Уровень | Тема |\n|--------:|------|\n"
        + "\n".join(rows_ru)
        + "\n\nПримеры в образе: `/usr/local/xodex/examples/c/`\n",
        encoding="utf-8",
    )
    (EN / "README.md").write_text(
        "# C Programming — levels 0–10\n\n"
        "Documentation for **absolute beginners**: what terms mean, why they exist, "
        "when they appear, and **code examples**. Not a homework checklist.\n\n"
        "| Level | Topic |\n|------:|-------|\n"
        + "\n".join(rows_en)
        + "\n\nLive examples: `/usr/local/xodex/examples/c/`\n",
        encoding="utf-8",
    )
    print("done", len(LESSONS), "lessons x2 langs")


if __name__ == "__main__":
    main()
