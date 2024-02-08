# From the ghidra , found logic it via &1 to decide to +5 or -2 character and append to rev_this file, so i reverse this logic and get the original flag.
rev_this = 'picoCTF{w1{1wq85jc=2i0<}'
answer = 'picoCTF{'
for i in range(8,24):
    if i%2 == 0:
        answer = answer + chr(ord(rev_this[i]) - 5)
    else:
        answer = answer + chr(ord(rev_this[i]) + 2)
answer = answer + '}'
print(f'answer: {answer}')
