#Copyright Lewis Yikfung Lau at IIIS, Tsinghua University
import os
import random
from time import sleep
Chinese_name = ["1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
"1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
"1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s"]
class MahjongTable:
  def __init__(self, agent0, agent1, agent2, agent3):
    self.score = [0, 0, 0, 0]#得分
    self.focus = 0#牌序
    self.fulu = []#副露信息
    self.private_tiles = []#玩家自己牌信息
    self.tile_num = [0, 0, 0, 0]#玩家牌数
    self.fulu_num = [0, 0, 0, 0]#玩家副露数
    self.tiles = []#牌山
    self.qipai = []#[tile, from]弃牌堆
    self.public_bin = [0 for _ in range(27)]#所有人都可见的牌数统计
    self.agentList = [agent0, agent1, agent2, agent3]#玩家
    self.player = 0#当前玩家
    self.active = [False, False, False, False]#玩家是否结束
    self.ganghou = False#杠后
    self.declared = [-1, -1, -1, -1]#花色 in [0, 1, 2]
    for i in range(4):
      self.fulu.append([[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]])
      pri_tiles = []
      self.agentList[i].set_order(i)
      for j in range(14):
        pri_tiles.append(27)#27==Empty mark
      self.private_tiles.append(pri_tiles)
    self.intialized = False
  def intialize(self):
    self.public_bin = [0 for _ in range(27)]
    self.ganghou = False
    self.intialized = True
    self.qipai = []
    tiles = []
    self.declared = [-1, -1, -1, -1]
    for i in range(27):
      for _ in range(4):
        tiles.append(i)
    random.shuffle(tiles)
    self.tiles = tiles
    for i in range(4):
      self.private_tiles[i][:13] = sorted(self.tiles[i * 13:(i + 1) * 13])
      self.private_tiles[i][13] = 27#27==Empty mark
      self.tile_num[i] = 13
      self.fulu[i] = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]#[tile, type, from]; type:0 peng, 1 jiagang/angang, 2 minggang, 3 angang
      self.fulu_num[i] = 0
      self.score[i] = 0
      self.active[i] = True
    self.focus = 52
    self.player = random.randint(0, 3)
    for i in range(4):
      self.declared[i] = self.agentList[i].declare(self)
      assert self.declared[i] in [0, 1, 2]
  def getTile(self, player):
    tile = self.private_tiles[player][13] = self.tiles[self.focus]
    self.private_tiles[player].sort()
    self.tile_num[player] += 1
    self.focus += 1
    if self.checkhu(player, -1):
      if self.agentList[player].ifhu(self, tile):
        self.hu(player, player, -1)
        self.ganghou = False
        return False
    elif self.checkgang(player, tile, True):
      if self.agentList[player].ifgang(self, tile):
        self.gang(tile, player, player, 1)
        return False
    return True
  def discardTile(self, player):
    self.player = self.next_player(player)
    num = self.agentList[player].discard(self)
    assert num in range(self.tile_num[player])
    tile = self.private_tiles[player][num]
    self.private_tiles[player] = self.private_tiles[player][:num] + self.private_tiles[player][num + 1:] + [27]#!!!
    self.tile_num[player] -= 1
    if_fangpao = False
    for i in range(1, 4):
      if self.active[(player + i) % 4]:
        if self.checkhu((player + i) % 4, tile):
          if self.agentList[(player + i) % 4].ifhu(self, tile):
            if_fangpao = True
            self.hu((player + i) % 4, player, tile)
    self.ganghou = False
    if if_fangpao:
      self.public_bin[tile] += 1
      return
    for i in range(1, 4):
      if self.active[(player + i) % 4]:
        if self.checkgang((player + i) % 4, tile, False):
          if self.agentList[(player + i) % 4].ifgang(self, tile):
            self.gang(tile, (player + i) % 4, player, 2)
            return
        if self.checkpeng((player + i) % 4, tile):
          if self.agentList[(player + i) % 4].ifpeng(self, tile):
            self.peng(tile, (player + i) % 4, player)
            return
    self.qipai.append([tile, player])
    print(Chinese_name[tile])
    self.public_bin[tile] += 1
  def peng(self, tile, player, from_player):
    self.ganghou = False
    num = self.private_tiles[player].index(tile)
    self.private_tiles[player] = self.private_tiles[player][:num] + self.private_tiles[player][num + 2:] + [27, 27]
    self.fulu[player][self.fulu_num[player]] = [tile, 0, from_player]
    self.public_bin[tile] += 3
    self.fulu_num[player] += 1
    self.tile_num[player] -= 2
    self.discardTile(player)
  def gang(self, tile, player, from_player, type):#1 jiagang/angang, 2 minggang, 3 angang, 不能抢杠, 杠立即结算
    assert type in [1, 2]
    if player == from_player:
      type = 3
      for i in range(self.fulu_num[player]):
        if self.fulu[player][i][0] == tile:
          type = 1#jiagang, else type==3 angang
          self.public_bin[tile] += 1
          num = self.private_tiles[player].index(tile)
          self.private_tiles[player] = self.private_tiles[player][:num] + self.private_tiles[player][num + 1:] + [27]
          self.tile_num[player] -= 1
          self.fulu[player][i][1] = 1
          self.fulu[player][i][2] = player
          for j in range(4):
            if self.active[j]:
              self.score[j] -= 1
              self.score[player] += 1
          break
      if type == 3:
        self.public_bin[tile] += 4
        num = self.private_tiles[player].index(tile)
        self.private_tiles[player] = self.private_tiles[player][:num] + self.private_tiles[player][num + 4:] + [27, 27, 27, 27]
        self.fulu[player][self.fulu_num[player]] = [tile, type, from_player]
        self.fulu_num[player] += 1
        self.tile_num[player] -= 4
        for j in range(4):
          if self.active[j]:
            self.score[j] -= 2
            self.score[player] += 2
    else:
      self.public_bin[tile] += 4
      num = self.private_tiles[player].index(tile)
      self.private_tiles[player] = self.private_tiles[player][:num] + self.private_tiles[player][num + 3:] + [27, 27, 27]
      self.fulu[player][self.fulu_num[player]] = [tile, type, from_player]
      self.fulu_num[player] += 1
      self.tile_num[player] -= 3
      self.score[player] += 2
      self.score[from_player] -= 2
    self.ganghou == True
    self.player = player
  def hu(self, player, from_player, tile):
    pt = 1
    fan = 0
    if self.focus == 108:#海底牌
      fan += 1
    if self.ganghou:
      fan += 1#不呼叫转移
    for fulu_tile in self.fulu[player][:self.fulu_num[player]]:#副露杠
      if fulu_tile[1] > 0:
        fan += 1
    
    bin = [0 for i in range(27)]
    for i in self.private_tiles[player][:self.tile_num[player]]:
      bin[i] += 1
    for i in self.fulu[player][:self.fulu_num[player]]:### #把副露牌转换成手牌
      bin[i[0]] += 3
    if player != from_player:
      bin[tile] += 1
    assert sum_list(bin) == 14
    for i in bin:#内含的杠
      if i == 4:
        fan += 1
    if sum_list(self.private_tiles[player][:9]) == 14 or sum_list(self.private_tiles[player][9:18]) == 14 \
      or sum_list(self.private_tiles[player][18:]) == 14:#清一色
      fan += 2
    
    bin_1 = bin_3 = 0
    for i in bin:
      if i == 1:
        bin_1 += 1
      elif i == 3:
        bin_3 += 1
    if bin_1 == 0:
      fan += 1
      if bin_3 == 0 or self.tile_num[player] == 1:#七对子or大吊车
        fan += 1
    
    pt *= (2 ** (3 if fan > 3 else fan))
    if player == from_player:#自摸
      pt += 1
      for i in range(1, 4):
        if self.active[(player + i) % 4]:
          self.score[player] += pt
          self.score[(player + i) % 4] -= pt
    else:
      self.score[player] += pt
      self.score[from_player] -= pt
      self.private_tiles[player][self.tile_num[player]] = tile
      self.tile_num[player] += 1
      self.private_tiles[player].sort()
    self.player = self.next_player(player)
    self.active[player] = False
  def finals(self):
    if self.get_player_num() > 1:
      ready = []
      not_ready = []
      for player in range(4):
        if self.active[player]:
          ifready = False
          for tile in range(27):
            if self.checkhu(player, tile):
              ready.append(player)
              ifready = True
              break
          if not ifready:
            not_ready.append(player)
      if len(ready) == 0 or len(not_ready) == 0:
        return
      else:#有没听牌的
        for ready_player in ready:
          for not_ready_player in not_ready:
            self.score[ready_player] += 8
            self.score[not_ready_player] -= 8

      
  def checkpeng(self, player, tile):
    if self.private_tiles[player][:self.tile_num[player]].count(tile) > 1:
      return True
    return False
  def checkgang(self, player, tile, ifself):#ifself==True：暗杠、加杠;False:明杠
    if self.focus == 108:
      return False
    if ifself:
      if self.private_tiles[player][:self.tile_num[player]].count(tile) == 4:
        return True
      for fulu in self.fulu[player][:self.fulu_num[player]]:
        if fulu[0] == tile:
          return True
      return False
    else:
      if self.private_tiles[player][:self.tile_num[player]].count(tile) == 3:
        return True
      return False
  def next_player(self, player):
    cur = player + 1
    for i in range(3):
      if self.active[(cur + i)% 4]:
        return (cur + i)% 4
  def checkhu(self, player, tile):
    base = self.declared[player] * 9
    if tile in range(base, base + 9):
      return False    
    for i in range(base, base + 9):
      if self.private_tiles[player][:self.tile_num[player]].count(i) > 0:
        return False
    bin = [0 for i in range(18)]    
    for t in self.private_tiles[player][:self.tile_num[player]]:
      if t > base:
        bin[t - 9] += 1
      else:
        bin[t] += 1
    if tile > -1:
      if tile > base:
        bin[tile - 9] += 1
      else:
        bin[tile] += 1
    sum_1 = sum_list(bin[:9])
    sum_2 = sum_list(bin[9:])
    assert (sum_1 + sum_2) % 3 == 2
    if sum_1 + sum_2 == 14:
      qiduizi = True
      for i in range(18):
        if bin[i] % 2 != 0:
          qiduizi = False
          break
      if qiduizi:
        return True
    if sum_1 % 3 == 1 or sum_2 % 3 == 1:
      return False
    if sum_1 % 3 == 0:
      if self.check_bin_0(bin[:9]) and self.check_bin_2(bin[9:]):
        return True
    else:
      if self.check_bin_0(bin[9:]) and self.check_bin_2(bin[:9]):
        return True
    return False
  def check_bin_0(self, list):
    assert len(list) == 9
    bin = []
    for i in list:
      bin.append(i)
    for i in range(9):
      if bin[i] >= 3:
        bin[i] -= 3
      if bin[i] != 0:
        if i > 6:
          return False
        if bin[i + 1] < bin[i] or bin[i + 2] < bin[i]:
          return False
        bin[i + 1] -= bin[i]
        bin[i + 2] -= bin[i]
        bin[i] = 0
    return True
  def check_bin_2(self, list):
    assert len(list) == 9
    for i in range(9):
      if list[i] >= 2:
        bin = []
        for j in list:
          bin.append(j)
        bin[i] -= 2
        if self.check_bin_0(bin):
          return True
    return False
  def get_player_num(self):
    return sum_list(self.active)
  def game(self):
    self.intialize()
    while self.focus != 108 and self.get_player_num() > 1:
      os.system('cls')
      print(self.player)
      state = self.getTile(self.player)#False == need to discard some tile
      if state:
        self.discardTile(self.player)
      self.ganghou = False
      tile = []
      for i in self.qipai:
        tile.append(Chinese_name[i[0]])
      print(tile)
      for i in range(4):
        tile = []
        for j in self.private_tiles[i][:self.tile_num[i]]:
          tile.append(Chinese_name[j])
        print(tile)
        tile = []
        for fu in self.fulu[i][:self.fulu_num[i]]:
          if fu[1] == 0:
            tile.append(Chinese_name[fu[0]] * 3)
          else:
            tile.append(Chinese_name[fu[0]] * 4)
        if not self.active[i]:
          tile.append('Over')
        print(tile)
      sleep(1.5)
    if self.focus == 108 or self.get_player_num() < 2:
      self.finals()
def sum_list(list):
  num = 0
  for i in list:
    num += i
  return num
class Agent:
  def __init__(self):
    self.player_order = 0
  def set_order(self, player_order):
    self.player_order = player_order
  def declare(self, table:MahjongTable): #[0, 1, 2]
    return 0
  def ifpeng(self, table:MahjongTable, tile): #bool
    pass
  def ifgang(self, table:MahjongTable, tile): #bool
    pass
  def ifhu(self, table:MahjongTable, tile): #bool
    pass
  def discard(self, table:MahjongTable): #in range(self.tile_num[player])
    pass
class shabiAgent(Agent):
  def __init__(self):
      super().__init__()
  def declare(self, table:MahjongTable):
    num = [0, 0, 0]
    for t in table.private_tiles[self.player_order][:13]:
      num[t // 9] += 1
    min_color = 1 if num[1] <= num[0] else 0
    min_color = 2 if num[2] <= num[min_color] else min_color
    return min_color
  def ifpeng(self, table:MahjongTable, tile): #bool
    declared = table.declared[self.player_order] * 9
    if tile < declared or tile >= declared + 9:
      return True
    else:
      return False
  def ifgang(self, table:MahjongTable, tile): #bool
    declared = table.declared[self.player_order] * 9
    if tile < declared or tile >= declared + 9:
      return True
    else:
      return False
  def ifhu(self, table:MahjongTable, tile): #bool
    return True
  def discard(self, table:MahjongTable): #in range(self.tile_num[player])
    declared = table.declared[self.player_order] * 9
    bin = [0 for _ in range(27)]
    for i in range(table.tile_num[self.player_order]):
      tile = table.private_tiles[self.player_order][i]
      if tile >= declared and tile < declared + 9:
        return i
      bin[tile] += 1
    assert sum_list(bin) % 3 == 2
    min_loss = 1000
    discard_tile = 0
    for i in range(table.tile_num[self.player_order]):
      loss = 0
      tile = table.private_tiles[self.player_order][i]
      if bin[tile] == 3:
        loss = 100
      elif bin[tile] == 2:
        loss = 40
      if tile % 9 == 0:
        if bin[tile + 1] > 0:
          if bin[tile + 2] > 0:
            loss += (72 + 2 * table.public_bin[tile])
          else:
            loss += (20 + 2 * table.public_bin[tile + 2])
        elif bin[tile + 2] > 0:
          loss += table.public_bin[tile + 1] * 5
      elif tile % 9 == 1:
        if bin[tile + 1] > 0:
          if bin[tile + 2] > 0:
            loss += (72 + table.public_bin[tile] * 2)
          elif bin[tile - 1] > 0:
            loss += (80 + table.public_bin[tile] * 5)
          else:
            loss += (20 + 2 * (table.public_bin[tile + 2] + table.public_bin[tile - 1]))
        elif bin[tile + 2] > 0:
          loss += table.public_bin[tile + 1] * 5
        elif bin[tile - 1] > 0:
          loss += (20 + 2 * table.public_bin[tile + 1])
      elif tile % 9 == 7:
        if bin[tile - 1] > 0:
          if bin[tile - 2] > 0:
            loss += (72 + table.public_bin[tile] * 2)
          elif bin[tile + 1] > 0:
            loss += (80 + table.public_bin[tile] * 5)
          else:
            loss += (20 + 2 * (table.public_bin[tile - 2] + table.public_bin[tile + 1]))
        elif bin[tile - 2] > 0:
          loss += table.public_bin[tile - 1] * 5
        elif bin[tile + 1] > 0:
          loss += (20 + 2 * table.public_bin[tile - 1])
      elif tile % 9 == 8:
        if bin[tile - 1] > 0:
          if bin[tile - 2] > 0:
            loss += (72 + 2 * table.public_bin[tile])
          else:
            loss += (20 + 2 * table.public_bin[tile - 2])
        elif bin[tile - 2] > 0:
          loss += table.public_bin[tile - 1] * 5
      else:
        if bin[tile + 1] > 0:
          if bin[tile + 2] > 0:
            loss += (72 + table.public_bin[tile] * 2)
          elif bin[tile - 1] > 0:
            loss += (80 + table.public_bin[tile] * 5)
          else:
            loss += (20 + 2 * (table.public_bin[tile + 2] + table.public_bin[tile - 1]))
        elif bin[tile + 2] > 0:
          loss += table.public_bin[tile + 1] * 5
        elif bin[tile - 1] > 0:
          if bin[tile - 2] > 0:
            loss += (72 + table.public_bin[tile] * 2)
          else:
            loss += (20 + 2 * (table.public_bin[tile - 2] + table.public_bin[tile + 1]))
      if loss < min_loss:
        min_loss = loss
        discard_tile = i
    return discard_tile

if __name__ == '__main__':
  agent_list = [shabiAgent(), shabiAgent(), shabiAgent(), shabiAgent()]
  mj = MahjongTable(agent_list[0], agent_list[1], agent_list[2], agent_list[3])
  mj.game()
  