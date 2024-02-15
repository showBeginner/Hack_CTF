# OTP Implementation
**Tag:** picoCTF 2020 Mini-Competition, Reverse Engineer
## Question:
_Author: madStacks_
### Description
Yay reversing! Relevant files: **otp**, **flag.txt**
>**Hint**
> 1. https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html
> 2. I think GDB Python is very useful, you can solve this problem without it, but can you solve future problems (hint hint)?
> 3. Also test your skills by solving this with ANGR!
## Analysis
From Tool: `ghidra`, we can found function: `valid_char` and `jumble`.
```c
// Character range: 0~9, a~f
undefined8 valid_char(char param_1){
  undefined8 uVar1;
  if ((param_1 < '0') || ('9' < param_1)) {
    if ((param_1 < 'a') || ('f' < param_1)) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}
```
`valid_char` is check if user_input is correct range character.\
`jumble` is the special operation with user_input.======> We can pass this function logical.

```c
for (i = 0; i < local_f0; i = i + 1) {
  encrypt_user_input[i] = encrypt_user_input[i] + 'a';
}
iVar3 = strncmp(encrypt_user_input
                "mlaebfkoibhoijfidblechbggcgldicegjbkcmolhdjihgmmieabohpdhjnciacbjjcnpcfaopigkpdfnoaknjlnlaohboimombk"
                ,100);
```
After encrypt user_input, user_input compare to `string`.\
We can reverse: `char + 'a'` it to compare to our brute user_input.
```c
      else {
        cVar2 = jumble(user_input[local_f0]);
        bVar1 = (byte)((int)cVar2 + (int)encrypt_user_input[local_f0 + -1] >> 0x1f);
        encrypt_user_input[local_f0] =
             ((char)((int)cVar2 + (int)encrypt_user_input[local_f0 + -1]) + (bVar1 >> 4) & 0xf) -
             (bVar1 >> 4);
      }
      local_f0 = local_f0 + 1;
```
```assembly
      0010092f 48 98         CDQE
      00100931 88 54 05      MOV       byte ptr [RBP + RAX*0x1 + -0x70],DL
               90
                         LAB_00100935                              XREF[1]:   001008e2(j)  
      00100935 83 85 18      ADD       dword ptr [RBP + local_f0],0x1
               ff ff ff 
               01
```
We can find 00100935 that represents user_input have been encrypted.
So we set this address is `Breakpoint:checkpoint`.
Our brute user_input compare to `$DL`.
And found correct user_input address `Breakpoint:solvepoint` `0x5555554009e5`.
## Resolve

```python
import gdb
import string
from queue import Queue, Empty

answer = "mlaebfkoibhoijfidblechbggcgldicegjbkcmolhdjihgmmieabohpdhjnciacbjjcnpcfaopigkpdfnoaknjlnlaohboimombk"

class Checkpoint(gdb.Breakpoint):
    def __init__(self, queue, target_hitcount, *args):
        super().__init__(*args)
        self.silent = True
        self.queue = queue
        self.target_hitcount = target_hitcount
        self.hit = 0

    def stop(self):
        self.hit += 1
        if self.hit == self.target_hitcount:
            correct_char = ord(answer[self.hit-1]) - ord('a')
            dl = int(gdb.parse_and_eval("$dl"))
            print(f'self.hit: {self.hit}, self.target_hitcount: {self.target_hitcount}')
            print(f'courrect_char: {correct_char}, dl: {dl}')
            self.queue.put( correct_char == dl )
        return False

class Solvepoint(gdb.Breakpoint):
    def __init__(self, *args):
        super().__init__(*args)
        self.silent = True
        self.hit = 0

    def stop(self):
        #gdb.execute("q")
        self.hit += 1
        return False


gdb.execute("set disable-randomization on")
gdb.execute("delete")
sp = Solvepoint("*0x5555554009e5")
queue = Queue()

flag = ""
ALPHABET = "abcdef0123456789"

while True:
    for c in ALPHABET:
      # If hit this address, it represent we need to compare current char and answer.
        bp = Checkpoint(queue, len(flag)+1, '*0x555555400935') 
        print("trying: ", flag+c)
        gdb.execute("run {}{}".format(flag, c))
        try:
          #if true : match current char and answer
            result = queue.get(timeout = 1) 
            bp.delete()
            if result: 
                flag += c
                print("\n\n{}\n\n".format(flag))
                break
        except Empty:
            print("Error empty")
            gdb.execute("q")
    #check flag len and whethe it hit the sovlepoint
    if len(flag) == 100 and  sp.hit > 0:
        print("Found flag: {}".format(flag))
        gdb.execute("q")
```
we can capture key.\
Answer is `key xor flag`.
```python
def str_xor_str(flag:str, key:str):
    flag_bytes = bytes.fromhex(flag)
    key_bytes = bytes.fromhex(key)
    result = ''.join([chr( x ^ y) for x,y in zip(flag_bytes, key_bytes)])
    return result
```

## Reference
1. [hacking-lab](https://github.com/onealmond/hacking-lab/blob/master/picoctf-2020/otp-implementation/writeup.md) - by onealmond
2. [CTFs/2021_picoCTF
/Easy_as_GDB.md](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Easy_as_GDB.md) -- by Dvd848