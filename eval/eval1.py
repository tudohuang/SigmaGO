#!/usr/bin/env python

from subprocess import Popen, PIPE

from gtp import parse_vertex, gtp_move, gtp_color
from gtp import BLACK, WHITE, PASS
import sys
import io

class GTPSubProcess(object):

    def __init__(self, label, args):
        self.label = label
        self.subprocess = Popen(args, stdin=PIPE, stdout=PIPE)
        print("{} subprocess created".format(label))
   
    def send(self, data):
        print("sending {}: {}".format(self.label, data))
        self.subprocess.stdin.write(data.encode())  # 將字符串轉換為字節串
        self.subprocess.stdin.flush()  # 確保數據被寫入
        result = ""
        while True:
            line = self.subprocess.stdout.readline().decode()  # 從字節串解碼為字符串
            if not line.strip():
                break
            result += line
        print("got: {}".format(result))
        return result

    def close(self):
        print("quitting {} subprocess".format(self.label))
        self.subprocess.communicate("quit\n".encode())  # 將字符串轉換為字節串


class GTPFacade(object):

    def __init__(self, label, args):
        self.label = label
        self.gtp_subprocess = GTPSubProcess(label, args)

    def name(self):
        self.gtp_subprocess.send("name\n")

    def version(self):
        self.gtp_subprocess.send("version\n")

    def boardsize(self, boardsize):
        self.gtp_subprocess.send("boardsize {}\n".format(boardsize))

    def komi(self, komi):
        self.gtp_subprocess.send("komi {}\n".format(komi))

    def clear_board(self):
        self.gtp_subprocess.send("clear_board\n")

    def genmove(self, color):
        message = self.gtp_subprocess.send(
            "genmove {}\n".format(gtp_color(color)))
        assert message[0] == "="
        return parse_vertex(message[1:].strip())

    def showboard(self):
        #self.gtp_subprocess.send("showboard\n")
        pass

    def play(self, color, vertex):
        self.gtp_subprocess.send("play {}\n".format(gtp_move(color, vertex)))

    def final_scoreX(self):
        self.gtp_subprocess.send("final_score\n")
        
    def final_score(self):
        result = self.gtp_subprocess.send("final_score\n")
        print(result)
        return result.strip()

    def close(self):
        self.gtp_subprocess.close()
# 解析分數並決定勝者
def parse_score(score):
    if score.startswith('= B+'):
        return -1
    elif score.startswith('= W+'):
        return 1
    else:
        return 0

GNUGO = ["C:\\GO\\gnugo-3.8\\gnugo-3.8\\gnugo.exe", "--mode", "gtp"]
GNUGO_LEVEL_ONE = ["C:\\GO\\gnugo-3.8\\gnugo-3.8\\gnugo.exe", "--mode", "gtp", "--level", "10"]
GNUGO_MONTE_CARLO = ["C:\\GO\\gnugo-3.8\\gnugo-3.8\\gnugo.exe", "--mode", "gtp", "--monte-carlo"]
SIGMAGO = ["c:\\Anaconda4\\python.exe", "C:\\GO\\SigmaGo\\sigmago.py", "-m" ,"sigmago_v1.pt"]



print(GNUGO_LEVEL_ONE)
print(SIGMAGO)


eng1 = GTPFacade("GNUGO", GNUGO_LEVEL_ONE)
eng2 = GTPFacade("SIGMAGO", SIGMAGO)

import tqdm
for black, white in ([eng1, eng2], [eng2, eng1]):
    pbar = tqdm.tqdm(range(50))
    white_win = 0
    for ii in pbar:
        # 創建一個 StringIO 物件來捕獲輸出
        temp_output = io.StringIO()
        sys.stdout = temp_output

        #black = GTPFacade("GNUGO", GNUGO_LEVEL_ONE)
        #white = GTPFacade("SIGMAGO", SIGMAGO)

        black.name()
        black.version()

        white.name()
        white.version()

        black.boardsize(9)
        white.boardsize(9)

        black.komi(6.5)
        white.komi(6.5)

        black.clear_board()
        white.clear_board()

        first_pass = False

        while True:
            vertex = black.genmove(BLACK)
            if vertex == PASS:
                if first_pass:
                    break
                else:
                    first_pass = True
            else:
                first_pass = False

            black.showboard()

            white.play(BLACK, vertex)
            white.showboard()

            vertex = white.genmove(WHITE)
            if vertex == PASS:
                if first_pass:
                    break
                else:
                    first_pass = True
            else:
                first_pass = False

            white.showboard()

            black.play(WHITE, vertex)
            black.showboard()

        black_score = parse_score(black.final_score())
        white_score = parse_score(white.final_score())

        score = black_score + white_score
        # 恢復標準輸出
        #sys.stdout = sys.__stdout__
        if score > 0:
            print('White won!!')
            white_win += 1
        else:
            print('Black won!!')


        
        white_rate = white_win/(ii+1)
        black_rate = 1 - white_rate

        pbar.set_description(f'Game: {ii+1}, W->{white.label}:{white_rate*100:.2f} %,  B->{black.label}:{black_rate*100:.2f} %')

black.close()
white.close()