import gym
#import gym_go
#import random
#from IPython.display import clear_output
#import time
#import gym_go
from gym.envs.registration import register
#import sys
import torch
#from IPython.display import clear_output
import torch.nn as nn
import torch.nn.functional as F
#import time
#from gym_go import gogame
import numpy as np
from model import SimpleCNN
import warnings

warnings.filterwarnings("ignore")


register(id='go_v0',  entry_point='gym_go.envs:GoEnv')



# 加載您的模型
from os.path import abspath, dirname
script_path = dirname(abspath(__file__))
model = SimpleCNN(num_classes=81)
model = torch.load(f'{script_path}\\sigmago.pt', map_location=torch.device('cpu'))
model.eval()

global go_env
go_env = gym.make('go_v0', size=9, komi=0, reward_method='real')
state = go_env.reset()

def get_idx(result, invalid):
    steps = np.argsort(result)[0,::-1]
   
    got_idx = -1

    for idx in steps:
        if invalid[idx] == 0:
            got_idx = idx
            break
    if got_idx == -1:
        got_idx = 81
    return got_idx

def xy_to_go_coord(x, y):
    columns = "ABCDEFGHJKLMNOPQRSTUVWXYZ"  # I is omitted in Go
    coord = columns[x] + str(y + 1)
    return coord

def go_coord_to_xy(coord):
    columns = "ABCDEFGHJKLMNOPQRSTUVWXYZ"  # I is omitted in Go
    x = columns.index(coord[0].upper())
    y = int(coord[1:]) - 1
    return (x, y)

def op_move(coord): #opponent move
    if coord == 'pass':
        player_step = 81
    else:
        player_step = go_coord_to_xy(coord) # 將圍棋座標轉成X, Y型式，從零開始
    state, reward, done, info = go_env.step(player_step)
    return 1


def get_next_step(player_move,color):

    if player_move == 'pass':
        result = 81
        state, reward, done, info = go_env.step(81)
        return 'pass'

    state = go_env.state()
    board = state[0]*-1 + state[1]
    #print(board)
    #print(player_move)
    if color == 'B':
        board *= -1
    board_d = board[None,...][None, ...]
    board_d = torch.from_numpy(board_d).to('cpu').float()
    logits = model(board_d)
    result0 = logits.cpu().detach().numpy()
    result = get_idx(result0, state[3].flatten())

    next_step_x = result // 9
    next_step_y = result % 9
    x = (next_step_x, next_step_y)
    state, reward, done, info = go_env.step(x)
    #print(x)
    
    #go_env.render('terminal')
    #clear_output(wait=True)

    go_step = xy_to_go_coord(next_step_x, next_step_y)

    return go_step

def cmd_reset(komi):
    global go_env
    go_env = gym.make('go_v0', size=9, komi=komi, reward_method='real')
    go_env.reset()
    return 1