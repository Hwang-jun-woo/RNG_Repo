import random as r
import time as t
import os
from colorama import init, Fore, Back, Style

init()

class RogueLike():

    def __init__(self):

        self.player_normal_stat = {'hp':100, 'mana':100, 'level':0}

        self.player_add_stat = {'attack':1, 'defense':0, 'agility':0, 'gen_speed':1, 'Luck':0}

        self.player_inventory = [] * 10

        self.player_weapon_slot = {'name':0, 'damage':0, 'durabiity':0}

        self.player_armor_slot = {'head':0, 'body':0, 'arm':0, 'leg':0, 'foot':0, 'accessories':0}

        self.field_enemy = {'enemy1':{'hp':20, 'def':0, 'agility':0, 'level':0, 'skill_1':None, 'skill_2':None},
                            'enemy2':{'hp':20, 'def':0, 'agility':0, 'level':0, 'skill_1':None, 'skill_2':None},
                            'enemy3':{'hp':20, 'def':0, 'agility':0, 'level':0, 'skill_1':None, 'skill_2':None},
                            'enemy4':{'hp':20, 'def':0, 'agility':0, 'level':0, 'skill_1':None, 'skill_2':None}
                            }
        
        self.enemy_list = []

        self.boss_stage = {}

    def random_stat(self):
        random_stat = 0
        comp_stat = 0

        for stat, amount in self.player_add_stat.items():
            random_stat = r.randint(3, 10)
            self.player_add_stat[stat] += random_stat + comp_stat
            comp_stat = 8 - random_stat
            print(f'(+{random_stat} {stat})')

        print(self.player_add_stat)

    def apply_stat(self, enemy):
        damage = self.player_add_stat['attack']
        self.field_enemy[enemy]['hp'] -= damage
        input(f'{Fore.RED}{damage}{Fore.WHITE} 데미지')

    def select_agument(self):
        ag = 0

        ag_list = []
        for i in range(3):
            agt = r.choice([1, 2, 3])
            if agt == 1:
                count = r.randint(3, 8)
                print(f'[{i + 1}]: 최대체력 {count} 증가')
                ag_list.append((agt, count))
            elif agt == 2:
                count = r.randint(1, 3)
                print(f'[{i + 1}]: 기본공격 대미지 {count} 증가')
                ag_list.append((agt, count))
            elif agt == 3:
                count = r.randint(2, 5)
                print(f'[{i + 1}]: 민첩 {count} 증가')
                ag_list.append((agt, count))

        while True:        
            choice = input('증강 선택:')

            try:
                choice = int(choice)
            except:
                input('잘못된 선택')
                continue
            if choice > 3 or choice < 1:
                input('잘못된 선택')
                continue
            
            if ag_list[choice - 1][0] == 1:
                self.player_normal_stat['hp'] += ag_list[choice - 1][1]
            if ag_list[choice - 1][0] == 2:
                self.player_add_stat['attack'] += ag_list[choice - 1][1]   
            if ag_list[choice - 1][0] == 3:
                self.player_add_stat['agility'] += ag_list[choice - 1][1]
            break

        print(f'(+{ag_list[choice - 1][1]})') 
        print(f'{self.player_normal_stat}|{self.player_add_stat}')
    
    def field_setting(self):
        enemy_count = r.randint(1, 4)
        for i in range(enemy_count):
            self.enemy_list.append(f'enemy{i+1}')

    def normal_battle(self):
        self.field_setting()

        while True:
            print('무엇을 할까?\n[1]: 공격\n[2]: 스킬\n[3]: 인벤토리')
            choice = input(': ')

            if choice == '1':
                os.system('cls')
                self.choice_enemy()
            else:
                input('잘못된 선택')
                continue

            for enemy in self.enemy_list:
                if self.field_enemy[enemy]['hp'] <= 0:
                    self.enemy_list.remove(enemy)
            
            if len(self.enemy_list) <= 0:
                print(f'{Fore.GREEN}[전투 승리!]{Fore.WHITE}')
                break
        
    def choice_enemy(self):
        while True:
            i = 0 
            for enemy in self.enemy_list:
                i += 1
                print(f'[{Fore.LIGHTBLUE_EX}{i}{Fore.WHITE}]: {Fore.RED}{enemy}{Fore.WHITE}(hp: {self.field_enemy[enemy]['hp']})')

            choice = input(': ')
            
            try:
                choice = int(choice)
            except:
                input('잘못된 선택')
                continue
            if choice > i or choice < 1:
                input('잘못된 선택')
                continue

            atk_enemy = self.enemy_list[choice - 1]
            self.apply_stat(atk_enemy)
            os.system('cls')
            break

rg = RogueLike()

rg.random_stat()
rg.select_agument()
rg.normal_battle()