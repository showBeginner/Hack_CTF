# Easy as GDB

## Question:
_Author: McKade_
### Description
The flag has got to be checked somewhere... File: brute
## Analysis
From `ghidra` tool to find matching flag 
character funcion as below:
```c
undefined4 FUN_000108c4(char *param_1,uint param_2)

{
  char *__dest;
  char *__dest_00;
  uint local_18;
  
  __dest = (char *)calloc(param_2 + 1,1);
  strncpy(__dest,param_1,param_2);
  FUN_000107c2(__dest,param_2,0xffffffff);
  __dest_00 = (char *)calloc(param_2 + 1,1);
  strncpy(__dest_00,&DAT_00012008,param_2);
  FUN_000107c2(__dest_00,param_2,0xffffffff);
  puts("checking solution...");
  local_18 = 0;
  while( true ) {
    if (param_2 <= local_18) {
      return 1;
    }
    if (__dest[local_18] != __dest_00[local_18]) break;
    local_18 = local_18 + 1; // =========>if char match , this variable will plus 1.
  }
  return 0xffffffff;
}
```
So we found this is our check_breakpoint:
```c++
0001099b 83 45       ADD      dword ptr [EBP + local_18],0x1
```
```c
undefined4 FUN_000109af(void)

{
  char *__s;
  size_t sVar1;
  undefined4 uVar2;
  int iVar3;
  
  __s = (char *)calloc(0x200,1);
  printf("input the flag: ");
  fgets(__s,0x200,_stdin);
  sVar1 = strnlen(&DAT_00012008,0x200);
  uVar2 = FUN_0001082b(__s,sVar1);
  FUN_000107c2(uVar2,sVar1,1);
  iVar3 = FUN_000108c4(uVar2,sVar1);
  if (iVar3 == 1) {
    puts("Correct!");
  }
  else {
    puts("Incorrect.");
  }
  return 0;
}
```
```assembly
     00010a60 83 c4 10    ADD      ESP,0x10
     00010a63 83 f8 01    CMP      EAX,0x1
     00010a66 75 14       JNZ      LAB_00010a7c
     00010a68 83 ec 0c    SUB      ESP,0xc
     00010a6b 8d 83       LEA      EAX,[EBX + 0xffffebbe]=>s_Correct!_0  = "Correct!"
             be eb 
             ff ff
     00010a71 50          PUSH     EAX=>s_Correct!_00010b76              = "Correct!"
     00010a72 e8 a9       CALL     <EXTERNAL>::puts                      int puts(char * __s)
             fa ff ff
```
`correct` address is `XXXXXa71`\
So use gdb to find address:
GDB Command:
```console
gef➤  where
#0  0xf7c23800 in __libc_start_main () from /lib/i386-linux-gnu/libc.so.6
#1  0x565555b1 in ?? ()
```
So we use gdb execute address: `0x56555XXX`
```c
Check_breakpoint: 0x5655599b
Solve_breakpoint: 0x56555a71
```
## Resolve

Python gdb script
```python
import gdb
import string


MAX_FLAG_LEN = 0x200

class Checkpoint(gdb.Breakpoint):
    def __init__(self, target_hitcount, *args):
        super().__init__(*args)
        self.silent = True
        self.target_hitcount = target_hitcount
        self.hit = 0

    def stop(self):
        res = []
        self.hit += 1
        return False

class Solvepoint(gdb.Breakpoint):
    def __init__(self, *args):
        super().__init__(*args)
        self.silent = True
        self.hit = 0

    def stop(self):
        self.hit += 1
        return False


gdb.execute("set disable-randomization on")
gdb.execute("delete")
sp = Solvepoint("*0x56555a71")


flag = ""
ALPHABET = string.ascii_letters + string.digits + "{}_"

for i in range(len(flag), MAX_FLAG_LEN):
    for c in ALPHABET:
        bp = Checkpoint(len(flag) + 1, '*0x5655599b')
        gdb.execute("run <<< {}{}".format(flag, c))
        print("trying: ", flag+c)
        if bp.hit == len(flag)+1:
            flag += c
            print("\n\n{}\n\n".format(flag))
            bp.delete()
            break
        else:
            bp.delete()

    if sp.hit > 0:
        print("Found flag: {}".format(flag))
        gdb.execute("q")
```

```c++
$ gdb ./brute 
gef➤  source solve.py 
....
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
input the flag: checking solution...
Incorrect.
[Inferior 1 (process 2930806) exited normally]
trying:  picoCTF{I_5D3_A11DA7_0db137a9{
Breakpoint 1196 at 0x5655599b
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
input the flag: checking solution...
Correct!
[Inferior 1 (process 2930807) exited normally]
trying:  picoCTF{I_5D3_A11DA7_0db137a9}


picoCTF{I_5D3_A11DA7_0db137a9}

Found flag: picoCTF{I_5D3_A11DA7_0db137a9}
```

## Reference:
1. [CTFs/2021_picoCTF
/Easy_as_GDB.md](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Easy_as_GDB.md) -- by Dvd848
2. [picoCTF 2021 Easy as GDB](https://www.youtube.com/watch?v=KYWxsxOugu4)
