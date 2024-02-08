# reverse_cipher
**Tag:** picoCTF 2019, Reverse Engineer
## Question:
_Author: Danny Tunitis_
### Description
We have recovered a binary and a text file. Can you reverse the flag.
>**Hint**\
>objdump and Gihdra are some tools that could assist with this
## Analysis
Via `ghidra` tool to reverse `binary file`.\
We will known `binary file` logic how flag be encrypted.\
**Text file: rev_this**
```console
└─$ cat rev_this
picoCTF{w1{1wq85jc=2i0<} 
```
**Binary file: rev**
```c
  for (local_14 = 8; (int)local_14 < 0x17; local_14 = local_14 + 1) {
    if ((local_14 & 1) == 0) {
      local_9 = local_58[(int)local_14] + '\x05';
    }
    else {
      local_9 = local_58[(int)local_14] + -2;
    }
    fputc((int)local_9,local_28);
  }
```
**Condition:** whether `char` is even or not.\
**Range:** 8 ~ 23,  `'picoCTF{' ~ '}'`.
```
Even: char + '\x05'
Odd: char + -2
```
## Resolve
Because we need reverse so even: -5 and odd: +2.
```python
rev_this = 'picoCTF{w1{1wq85jc=2i0<}'
answer = 'picoCTF{'
for i in range(8,24):
    if i%2 == 0:
        answer = answer + chr(ord(rev_this[i]) - 5)
    else:
        answer = answer + chr(ord(rev_this[i]) + 2)
answer = answer + '}'
print(f'answer: {answer}')
```

## Answer
```
picoCTF{r3v3rs37ee84d27}
```