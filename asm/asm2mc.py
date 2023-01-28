# -------------------- IMPORTS --------------------


from glob import glob


# -------------------- CONSTANTS --------------------


DEFAULT_REGISTER_SIZE = 3
DEFAULT_HEXADECIMAL_SIZE = 4
TESTS_PATH = "tests/"


# -------------------- FUNCTIONS --------------------


class Parser:

    def __init__(self):
        pass

    @staticmethod
    def __convert(number: str, base_src: int, base_dest: int) -> str:
        """Converts a number from one base to another (limit=16).

        Args:
            number (str): The number to convert.
            base_src (int): The base of the number to convert.
            base_dest (int): The base to convert the number to.

        Returns:
            str: The converted number.
        """
        base_map = "0123456789abcdefghijklmnopqrstuvwxyz"
        base_10_number = int(number, base_src)
        if base_10_number == 0:
            return "0"
        result = ""
        while base_10_number > 0:
            result = base_map[base_10_number % base_dest] + result
            base_10_number //= base_dest
        return result

    @staticmethod
    def __get_register(register: str) -> str:
        """Get the binary representation of a register.

        Args:
            register (str): The register to get the binary representation of.

        Returns:
            str: The binary representation of the register.
        """
        return bin(int(register[1:]))[2:].zfill(DEFAULT_REGISTER_SIZE)

    @staticmethod
    def __get_immediate(immediate: str, size: int, division_by_4: bool = False) -> str:
        """Get the binary representation of an immediate.

        Args:
            immediate (str): The immediate to get the binary representation of.

        Returns:
            str: The binary representation of the immediate.
        """
        if immediate[1:] == 'sp':
            return '0' * size
        return bin(int(immediate[1:]))[2:].zfill(size) if not division_by_4 else bin(int(immediate[1:]) // 4)[2:].zfill(size)

    @staticmethod
    def parse_asm_into_machine_code(asm: str) -> str:
        """Parse an ASM code (with the ARMv7 instruction set) and returns the corresponding machine code.

        Args:
            asm (str): The ASM code to parse.

        Returns:
            str: The machine code.
        """
        parsed_asm_code = [[l.strip().strip(',') for l in l.replace(
            ',', ", ").split()] for l in asm.splitlines() if len(l.split()) > 0]
        machine_code = ""

        def __get_label_offset(instruction_number: int, label: str, size: int) -> str:
            """Get the the binary representation of a label offset.

            Args:
                label (str): The label to get the offset as binary representation of.

            Returns:
                str: The binary representation of the label offset.
            """
            i = 0
            for instruction in parsed_asm_code:
                if instruction[0] == label + ":":
                    return bin(2**size + i - instruction_number - 3)[-size:]

                elif instruction[0].endswith(':'):
                    continue

                i += 1
            raise Exception(f"Error: Label {label} not defined.")

        def __lsls(args: list, instruction_number: int = None) -> str:
            """Parse the lsls instruction. (Logical Shift Left) LSLS Rd, Rm, #<imm5> or LSLS Rdn, Rm"""
            if args[-1].startswith("#"):
                return "00000" + Parser.__get_immediate(args[-1], 5) + Parser.__get_register(args[1]) + Parser.__get_register(args[0])
            return "0100000010" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __lsrs(args: list, instruction_number: int = None) -> str:
            """Parse the lsrs instruction. (Logical Shift Right) LSRS Rd, Rm, #<imm5> or LSRS Rdn, Rm"""
            if args[-1].startswith("#"):
                return "00001" + Parser.__get_immediate(args[-1], 5) + Parser.__get_register(args[1]) + Parser.__get_register(args[0])
            return "0100000011" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __asrs(args: list, instruction_number: int = None) -> str:
            """Parse the asrs instruction. (Arithmetic Shift Right) ASRS Rd, Rm, #<imm5> or ASRS Rdn, Rm"""
            if args[-1].startswith("#"):
                return "00010" + Parser.__get_immediate(args[-1], 5) + Parser.__get_register(args[1]) + Parser.__get_register(args[0])
            return "0100000100" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __adds(args: list, instruction_number: int = None) -> str:
            """Parse the adds instruction. (Add register or 3-bit immediate) ADDS Rd, Rn, Rm or ADDS Rd, Rn, #<imm3>"""
            if args[-1].startswith("#"):
                return "0001110" + Parser.__get_immediate(args[-1], 3) + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

            return "0001100" + Parser.__get_register(args[2]) + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __subs(args: list, instruction_number: int = None) -> str:
            """Parse the subs instruction. (Subtract register or 3-bit immediate) SUBS Rd, Rn, Rm or SUBS Rd, Rn, #<imm3>"""
            if args[-1].startswith("#"):
                return "0001111" + Parser.__get_register(args[2]) + Parser.__get_register(args[1]) + Parser.__get_register(args[0])
            else:
                return "0001101" + Parser.__get_register(args[2]) + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __movs(args: list, instruction_number: int = None) -> str:
            """Parse the movs instruction. (Move 3-bit immediate) MOVS Rd, #<imm8>"""
            return "00100" + Parser.__get_register(args[0]) + Parser.__get_immediate(args[1], 8)

        def __ands(args: list, instruction_number: int = None) -> str:
            """Parse the ands instruction. (Bitwise AND) ANDS Rdn, Rm"""
            return "0100000000" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __eors(args: list, instruction_number: int = None) -> str:
            """Parse the eors instruction. (Bitwise Exclusive OR) EORS Rdn, Rm"""
            return "0100000001" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __adcs(args: list, instruction_number: int = None) -> str:
            """Parse the adcs instruction. (Add with carry) ADCS Rdn, Rm"""
            return "0100000101" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __sbcs(args: list, instruction_number: int = None) -> str:
            """Parse the sbcs instruction. (Subtract with carry) SBCS Rdn, Rm"""
            return "0100000110" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __rors(args: list, instruction_number: int = None) -> str:
            """Parse the rors instruction. (Rotate Right) RORS Rdn, Rm"""
            return "0100000111" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __tst(args: list, instruction_number: int = None) -> str:
            """Parse the tst instruction. (Test Bits) TST Rn, Rm"""
            return "0100001000" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __rsbs(args: list, instruction_number: int = None) -> str:
            """Parse the rsbs instruction. (Reverse Subtract) RSBS Rd, Rn"""
            return "0100001001" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __cmp(args: list, instruction_number: int = None) -> str:
            """Parse the cmp instruction. (Compare) CMP Rdn, Rm"""
            return "0100001010" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __cmn(args: list, instruction_number: int = None) -> str:
            """Parse the cmn instruction. (Compare Negative) CMN Rdn, Rm"""
            return "0100001011" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __orrs(args: list, instruction_number: int = None) -> str:
            """Parse the orrs instruction. (Bitwise OR) ORRS Rdn, Rm"""
            return "0100001100" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __muls(args: list, instruction_number: int = None) -> str:
            """Parse the muls instruction. (Multiply) MULS Rdm, Rn Rdm"""
            return "0100001101" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __bics(args: list, instruction_number: int = None) -> str:
            """Parse the bics instruction. (Bit Clear) BICS Rdn, Rm"""
            return "0100001110" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __mvns(args: list, instruction_number: int = None) -> str:
            """Parse the mvns instruction. (Move NOT) MVNS Rd, Rm"""
            return "0100001111" + Parser.__get_register(args[1]) + Parser.__get_register(args[0])

        def __str(args: list, instruction_number: int = None) -> str:
            """Parse the str instruction. (Store word) STR Rt, [SP, #<imm8>]"""
            return "10010" + Parser.__get_register(args[0]) + Parser.__get_immediate(args[-1][:-1], 8, division_by_4=True)  # Remove the closing bracket

        def __ldr(args: list, instruction_number: int = None) -> str:
            """Parse the ldr instruction. (Load word) LDR Rt, [SP, #<imm8>]"""
            return "10011" + Parser.__get_register(args[0]) + Parser.__get_immediate(args[-1][:-1], 8, division_by_4=True)  # Remove the closing bracket

        def __add(args: list, instruction_number: int = None) -> str:
            """Parse the add instruction. (Add immediate to SP) ADD [SP,] SP, #<imm7>"""
            return "101100000" + Parser.__get_immediate(args[-1], 7, division_by_4=True)

        def __sub(args: list, instruction_number: int = None) -> str:
            """Parse the sub instruction. (Subtract immediate from SP) SUB [SP,] SP, #<imm7>"""
            return "101100001" + Parser.__get_immediate(args[-1], 7, division_by_4=True)

        def __beq(args: list, instruction_number: int = None) -> str:
            """Parse the beq instruction. (Branch if equal) BEQ <label> (with label written on 8 bits as imm8)"""
            return "11010000" + __get_label_offset(instruction_number, args[0], 8)

        def __bne(args: list, instruction_number: int = None) -> str:
            """Parse the bne instruction. (Branch if not equal) BNE <label> (with label written on 8 bits as imm8)"""
            return "11010001" + __get_label_offset(instruction_number, args[0], 8)

        def __bcs(args: list, instruction_number: int = None) -> str:
            """Parse the bcs instruction. (Branch if carry set) BCS <label> (with label written on 8 bits as imm8)"""
            return "11010010" + __get_label_offset(instruction_number, args[0], 8)

        def __bcc(args: list, instruction_number: int = None) -> str:
            """Parse the bcc instruction. (Branch if carry clear) BCC <label> (with label written on 8 bits as imm8)"""
            return "11010011" + __get_label_offset(instruction_number, args[0], 8)

        def __bmi(args: list, instruction_number: int = None) -> str:
            """Parse the bmi instruction. (Branch if minus) BMI <label> (with label written on 8 bits as imm8)"""
            return "11010100" + __get_label_offset(instruction_number, args[0], 8)

        def __bpl(args: list, instruction_number: int = None) -> str:
            """Parse the bpl instruction. (Branch if plus) BPL <label> (with label written on 8 bits as imm8)"""
            return "11010101" + __get_label_offset(instruction_number, args[0], 8)

        def __bvs(args: list, instruction_number: int = None) -> str:
            """Parse the bvs instruction. (Branch if overflow set) BVS <label> (with label written on 8 bits as imm8)"""
            return "11010110" + __get_label_offset(instruction_number, args[0], 8)

        def __bvc(args: list, instruction_number: int = None) -> str:
            """Parse the bvc instruction. (Branch if overflow clear) BVC <label> (with label written on 8 bits as imm8)"""
            return "11010111" + __get_label_offset(instruction_number, args[0], 8)

        def __bhi(args: list, instruction_number: int = None) -> str:
            """Parse the bhi instruction. (Branch if higher) BHI <label> (with label written on 8 bits as imm8)"""
            return "11011000" + __get_label_offset(instruction_number, args[0], 8)

        def __bls(args: list, instruction_number: int = None) -> str:
            """Parse the bls instruction. (Branch if lower or same) BLS <label> (with label written on 8 bits as imm8)"""
            return "11011001" + __get_label_offset(instruction_number, args[0], 8)

        def __bge(args: list, instruction_number: int = None) -> str:
            """Parse the bge instruction. (Branch if greater or equal) BGE <label> (with label written on 8 bits as imm8)"""
            return "11011010" + __get_label_offset(instruction_number, args[0], 8)

        def __blt(args: list, instruction_number: int = None) -> str:
            """Parse the blt instruction. (Branch if less than) BLT <label> (with label written on 8 bits as imm8)"""
            return "11011011" + __get_label_offset(instruction_number, args[0], 8)

        def __bgt(args: list, instruction_number: int = None) -> str:
            """Parse the bgt instruction. (Branch if greater than) BGT <label> (with label written on 8 bits as imm8)"""
            return "11011100" + __get_label_offset(instruction_number, args[0], 8)

        def __ble(args: list, instruction_number: int = None) -> str:
            """Parse the ble instruction. (Branch if less or equal) BLE <label> (with label written on 8 bits as imm8)"""
            return "11011101" + __get_label_offset(instruction_number, args[0], 8)

        def __bal(args: list, instruction_number: int = None) -> str:
            """Parse the bal instruction. (Branch and link) BAL <label> (with label written on 8 bits as imm8)"""
            return "11011110" + __get_label_offset(instruction_number, args[0], 8)

        def __b(args: list, instruction_number: int = None) -> str:
            """Parse the b instruction. (Branch) B <label> (with label written on 11 bits as imm11)"""
            return "11100" + __get_label_offset(instruction_number, args[0], 11)

        i = 0
        for instruction in parsed_asm_code:

            keyword = instruction[0].lower()

            if keyword.endswith(':') or keyword.startswith(('@', '.')):
                continue

            fun = locals()["_Parser__" + keyword]
            binary = fun(instruction[1:], i)
            machine_code += Parser.__convert(binary, 2,
                                             16).zfill(DEFAULT_HEXADECIMAL_SIZE) + " "

            i += 1

        return machine_code[:-1]


# -------------------- MAIN FUNCTION --------------------


def main() -> None:
    test_folder = TESTS_PATH if TESTS_PATH.endswith('/') else TESTS_PATH + '/'  # Ensure we have a well-formed path
    asm_files = glob(f"{test_folder}**/*.s", recursive=True)

    for asm_file in asm_files:
        print(f"Testing {asm_file}...")

        # Getting the machine code from the parser
        with open(asm_file, "r") as f:
            asm_code = f.read()
            machine_code = Parser.parse_asm_into_machine_code(asm_code)

        # Checking if the content of the machine code is the same as the content of the .bin file in the same directory
        bin_file = ''.join(asm_file.split('.')[:-1]) + ".bin"
        with open(bin_file, "r") as f:
            expected_machine_code = ''.join(f.readlines()[1:])
            if machine_code.strip() != expected_machine_code.strip():
                print(f"Error in: {asm_file}:")
                print(f"1: {expected_machine_code}", end='')
                print(f"2: {machine_code}")
                exit(1)

            else:
                print(f"Test passed for {asm_file}")


# -------------------- MAIN CALL --------------------


if __name__ == "__main__":
    main()
