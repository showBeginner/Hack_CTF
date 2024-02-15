#Command:  gdb -n -q -ex "set pagination off" -ex "source resolve.py" ./brute
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
        #print(f"\nhit: {self.hit}, target:{self.target_hitcount}")
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
        bp = Checkpoint(queue, len(flag)+1, '*0x555555400935') # If hit this address, it represent we need to compare current char and answer.
        print("trying: ", flag+c)
        gdb.execute("run {}{}".format(flag, c))
        try:
            result = queue.get(timeout = 1) #if true : match current char and answer
            bp.delete()
            if result: 
                flag += c
                print("\n\n{}\n\n".format(flag))
                break
        except Empty:
            print("Error empty")
            gdb.execute("q")
    
    if len(flag) == 100 and  sp.hit > 0:#check flag len and whethe it hit the sovlepoint
        print("Found flag: {}".format(flag))
        gdb.execute("q")
