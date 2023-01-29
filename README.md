# Polytech ARM-based embedded processor

## 📋 Instructions we had to follow

By using [Logisim](proc/logisim/), we firstly had to make a [CPU](proc/) (a simplified one). To test it, we have [some very basic C snippets](c/) which can be compiled by the CPU into Assembly. Next, we had to make [a program](asm/) which can translate assembly language (ARMv7) into machine code.

You can learn more about Logisim, ARMv7 and the whole Cortex-M0 family of processors in the [docs](docs/) folder.

## ⚙️ Compile C to ARM Assembly

To check whether our CPU works or not, we need to compile these C programs and compare each other.

Install the `libc6-armel-cross`, `libc6-dev-armel-cross`, `binutils-arm-linux-gnueabi` and `libncurses5-dev` packages by using the following command:

```bash
sudo apt-get install libc6-armel-cross libc6-dev-armel-cross binutils-arm-linux-gnueabi libncurses5-dev
```

Then, install `gcc` and `g++` to support ARM:

```bash
sudo apt-get install gcc-arm-linux-gnueabi g++-arm-linux-gnueabi
```

Finally, you can compile like this:

```bash
arm-linux-gnueabi-gcc hello.c -S -mtune=cortex-m0 -march=armv7-m -mthumb -fomit-frame-pointer -o hello.s
```

## 📽️ Presentation

See the [presentation](presentation/) folder for more details.

## 🧾 Additional informations

### C Headers

| Program | Description |
|-|-|
| crypto | Cryptography |
| fixed | Fixed Point Decimal Numbers |
| math | Mathematical tools |
| parm | Main Header |
| stdio | Text Input/Output (keyboard, terminal) |
| string | Basic implementation of strings |
| string2 | Other basic implementation of strings |
| trigo | Trigonometric functions (Taylor series) |
| utils | Debugging Tools |
| video | Matrix screen |

### C programs

| Program | Description |
|-|-|
| calckeyb| Calculator with keyboard and terminal |
| calculator | Calculator with DIP-switches |
| simple_add | Adds two variables and displays it in RES |
| testfp | Demonstrate fixed-point number macros |
| tty | Display "Project PARM" in terminal |

### MMIO

See `parm.h` for the pins documentation.

## ✒️ Authors

* Marc PINET - [marcpinet](https://github.com/marcpinet)
* Loïc PANTANO - [loicpantano](https://github.com/loicpantano)
* Arthur RODRIGUEZ - [rodriguezarthur](https://github.com/rodriguezarthur)
