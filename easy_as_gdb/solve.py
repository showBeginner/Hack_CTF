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
