# How to Build Your Own VM / OS — from Zero

> *"Can we reconstruct it and make it a How-To Build an own VM/OS?"* — E.C.Pabel

This guide walks you from **nothing** to a working virtual machine (VM) and then a minimal operating system (OS) shell. Everything here can be done on Linux, macOS, or Windows (WSL2). No prior OS-dev experience required.

---

## Part 0 — What are we building?

| Term | What it means here |
|---|---|
| **VM (virtual machine)** | A program that pretends to be a CPU — you feed it bytecode instructions and it executes them |
| **OS** | Software that sits between hardware and programs: manages memory, handles keyboard/screen, loads files |
| **Bootloader** | The tiny program that wakes the CPU up and loads the OS |
| **Kernel** | The core of the OS — the part that always runs and talks to hardware |

We'll build in three layers, each runnable on its own:

```
Layer 3 │  iam_universe kernel shell  (your own "OS personality")
Layer 2 │  minimal x86 bootloader + kernel  (bare-metal, runs in QEMU)
Layer 1 │  stack-based bytecode VM in C  (understand how VMs work)
```

---

## Part 1 — A Stack-Based Bytecode VM in C

The simplest possible VM. It has:
- A **stack** (a small array of numbers)
- A **program counter** (which instruction to run next)
- A handful of **opcodes**: PUSH, ADD, SUB, MUL, DIV, PRINT, HALT

### 1.1 Create the file

```c
// vm/vm.c
#include <stdio.h>
#include <stdlib.h>

#define STACK_MAX 256

typedef enum {
    OP_PUSH  = 0x01,
    OP_ADD   = 0x02,
    OP_SUB   = 0x03,
    OP_MUL   = 0x04,
    OP_DIV   = 0x05,
    OP_PRINT = 0x06,
    OP_HALT  = 0xFF,
} OpCode;

typedef struct {
    int stack[STACK_MAX];
    int sp;           /* stack pointer */
    unsigned char *code;
    int pc;           /* program counter */
} VM;

void vm_push(VM *vm, int val) {
    if (vm->sp >= STACK_MAX) { fprintf(stderr, "stack overflow\n"); exit(1); }
    vm->stack[vm->sp++] = val;
}

int vm_pop(VM *vm) {
    if (vm->sp <= 0) { fprintf(stderr, "stack underflow\n"); exit(1); }
    return vm->stack[--vm->sp];
}

void vm_run(VM *vm) {
    for (;;) {
        unsigned char op = vm->code[vm->pc++];
        switch (op) {
            case OP_PUSH: {
                int val = (vm->code[vm->pc] << 8) | vm->code[vm->pc+1];
                vm->pc += 2;
                vm_push(vm, val);
                break;
            }
            case OP_ADD:   vm_push(vm, vm_pop(vm) + vm_pop(vm)); break;
            case OP_SUB: { int b = vm_pop(vm); vm_push(vm, vm_pop(vm) - b); break; }
            case OP_MUL:   vm_push(vm, vm_pop(vm) * vm_pop(vm)); break;
            case OP_DIV: { int b = vm_pop(vm); vm_push(vm, vm_pop(vm) / b); break; }
            case OP_PRINT: printf("%d\n", vm_pop(vm)); break;
            case OP_HALT:  return;
            default:
                fprintf(stderr, "unknown opcode 0x%02X\n", op);
                exit(1);
        }
    }
}

int main(void) {
    /* Program: (3 + 4) * 2 = 14 */
    unsigned char program[] = {
        OP_PUSH, 0x00, 0x03,   /* push 3    */
        OP_PUSH, 0x00, 0x04,   /* push 4    */
        OP_ADD,                /* 3 + 4 = 7 */
        OP_PUSH, 0x00, 0x02,   /* push 2    */
        OP_MUL,                /* 7 * 2 = 14 */
        OP_PRINT,              /* print 14  */
        OP_HALT,
    };
    VM vm = { .sp = 0, .code = program, .pc = 0 };
    vm_run(&vm);
    return 0;
}
```

### 1.2 Build & run

```bash
mkdir -p vm
# paste the code above into vm/vm.c
gcc -O2 -o vm/vm vm/vm.c
./vm/vm
# → 14
```

### 1.3 What you just built

- A **fetch-decode-execute** loop — the same loop every real CPU runs
- A **stack machine** — Python's own bytecode VM (CPython) works this way
- The `.iam` language interpreter in `lang/iamrun.c` uses the same pattern

---

## Part 2 — A Minimal x86 Bootloader (runs in QEMU)

A bootloader is a 512-byte program that the BIOS loads at address `0x7C00`. This one prints `iam_universe` on screen and halts.

### 2.1 Install tools

```bash
# Ubuntu / Debian
sudo apt install nasm qemu-system-x86

# macOS (Homebrew)
brew install nasm qemu
```

### 2.2 Write the bootloader

```nasm
; boot/boot.asm
BITS 16
ORG  0x7C00

start:
    mov  ax, 0x0003       ; text mode 80x25
    int  0x10

    mov  si, msg
.print:
    lodsb
    test al, al
    jz   .done
    mov  ah, 0x0E
    int  0x10
    jmp  .print
.done:
    cli
    hlt

msg: db "iam_universe booted.", 13, 10, 0

TIMES 510 - ($ - $$) db 0
DW 0xAA55               ; boot signature
```

### 2.3 Assemble & run in QEMU

```bash
mkdir -p boot
# paste the code above into boot/boot.asm
nasm -f bin boot/boot.asm -o boot/boot.img
qemu-system-x86_64 -drive format=raw,file=boot/boot.img -nographic
# press Ctrl-A then X to quit QEMU
```

You will see:
```
iam_universe booted.
```

**That's your own code running before any OS.** No Linux. No Windows. Just your 512 bytes talking to hardware.

### 2.4 What happened

| Step | What the hardware does |
|---|---|
| Power on | BIOS runs from ROM, checks hardware |
| Boot device found | BIOS reads sector 1 of the disk into RAM at `0x7C00` |
| Signature check | Last two bytes must be `0xAA55` — BIOS checks this |
| Jump to `0x7C00` | CPU starts executing your code |
| BIOS `int 0x10` | Video interrupt — prints a character to screen |

---

## Part 3 — A Minimal Kernel in C + NASM

Now we add a **C kernel** that the bootloader loads and jumps to. This is the basic structure of every OS: a bootloader that enters 32-bit protected mode and then calls `kmain()`.

### 3.1 File layout

```
kernel/
├── boot/
│   └── boot.asm      ← 16-bit bootloader + switch to protected mode
├── kernel/
│   └── kmain.c       ← C entry point
├── linker.ld         ← memory layout
└── Makefile
```

### 3.2 The protected-mode bootloader (`kernel/boot/boot.asm`)

```nasm
BITS 16
ORG 0x7C00

; Switch to 32-bit protected mode
cli
lgdt [gdt_descriptor]
mov eax, cr0
or  eax, 1
mov cr0, eax
jmp 0x08:protected_mode   ; far jump — flushes pipeline

BITS 32
protected_mode:
    mov ax, 0x10
    mov ds, ax
    mov ss, ax
    mov esp, 0x90000
    extern kmain
    call kmain
    hlt

; ---- Minimal GDT (Global Descriptor Table) ----
gdt_start:
    dq 0x0000000000000000   ; null descriptor
    dq 0x00CF9A000000FFFF   ; code segment
    dq 0x00CF92000000FFFF   ; data segment
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

TIMES 510 - ($ - $$) db 0
DW 0xAA55
```

### 3.3 The C kernel (`kernel/kernel/kmain.c`)

```c
/* Write directly to VGA text buffer at 0xB8000 */
#define VGA_BASE ((volatile unsigned short *)0xB8000)
#define WHITE_ON_BLACK 0x0F00

static void kprint(const char *s) {
    static int col = 0;
    for (; *s; s++, col++)
        VGA_BASE[col] = WHITE_ON_BLACK | (unsigned char)*s;
}

void kmain(void) {
    kprint("iam_universe kernel running.");
    /* hang */
    for (;;) __asm__("hlt");
}
```

### 3.4 Linker script (`kernel/linker.ld`)

```
ENTRY(kmain)
SECTIONS {
    . = 0x1000;
    .text  : { *(.text)  }
    .data  : { *(.data)  }
    .bss   : { *(.bss)   }
}
```

### 3.5 Makefile (`kernel/Makefile`)

```makefile
CC    = gcc
CFLAGS = -m32 -ffreestanding -fno-pic -O2
NASM  = nasm

all: os.img

boot.o:
	$(NASM) -f elf32 boot/boot.asm -o boot.o

kmain.o:
	$(CC) $(CFLAGS) -c kernel/kmain.c -o kmain.o

kernel.bin: boot.o kmain.o
	ld -m elf_i386 -T linker.ld -o kernel.bin boot.o kmain.o

os.img: kernel.bin
	objcopy -O binary kernel.bin os.img
	# Pad to 1.44 MB floppy size
	dd if=/dev/zero bs=512 count=2880 of=floppy.img
	dd if=os.img of=floppy.img conv=notrunc

run:
	qemu-system-x86_64 -drive format=raw,file=floppy.img -nographic

clean:
	rm -f *.o *.bin *.img
```

### 3.6 Build & run

```bash
cd kernel
sudo apt install gcc-multilib   # for -m32 support
make
make run
# → iam_universe kernel running.
```

---

## Part 4 — What's Next (the real OS path)

You now have a working bare-metal kernel. Here's what every serious OS adds next:

| Feature | What to implement | Difficulty |
|---|---|---|
| **Interrupt handling (IDT)** | Catch keyboard, timer, faults | ⭐⭐ |
| **Physical memory manager** | Track which RAM pages are free | ⭐⭐ |
| **Virtual memory / paging** | Each process gets its own address space | ⭐⭐⭐ |
| **Keyboard driver** | Read PS/2 scan codes via I/O port `0x60` | ⭐⭐ |
| **Simple shell** | Read commands from keyboard, execute them | ⭐⭐ |
| **File system (FAT16)** | Read files from disk | ⭐⭐⭐ |
| **ELF loader** | Load and run user programs | ⭐⭐⭐ |
| **System calls** | Programs request OS services via `int 0x80` | ⭐⭐⭐ |

---

## Part 5 — Connect this to iam_universe

The `.iam` interpreter in `lang/iamrun.c` **is already a VM** — it has:
- A fetch-decode-execute loop (like Part 1)
- Named opcodes (`GRID`, `PATCH`, `RUN`, `SAVE`)
- State (the grid) that persists between instructions

To turn it into an "iam OS":
1. Add a `SHELL` opcode that reads the next `.iam` command from `stdin` in a loop
2. Add a `LOAD filename` opcode that reads another `.iam` file and runs it
3. Add `SAVE filename` to write grid state to disk
4. Run it in your Part 3 kernel as the user program

That's a tiny, custom operating environment — your research framework as a running system.

---

## Resources

| Resource | What you'll find |
|---|---|
| [wiki.osdev.org](https://wiki.osdev.org/Bare_Bones) | The standard OS-dev reference. Start with "Bare Bones". |
| [littleosbook.github.io](https://littleosbook.github.io) | "The little book about OS development" — free PDF |
| [nasm.us/doc](https://www.nasm.us/doc/) | NASM assembler documentation |
| [brendangregg.com/blog.html](https://www.brendangregg.com/blog.html) | Deep OS internals |
| [craftinginterpreters.com](https://craftinginterpreters.com) | Build a language + VM from scratch (free online) |

---

> *"You want to understand how PCs truly work. Building a VM and OS is the most direct answer."*
> Every line in this file is something you can type, compile, and run today.
