import random as r
import os
import math as m
import time as t
from colorama import init, Fore, Back, Style

init()

class RandomNunberGame():

    def __init__(self):
        self.sword_lv = 28

        self.loan_num = 0

        self.sword_name = {
            '골든 스워드':{'effect': f'{Fore.YELLOW}마이다스의 손{Fore.WHITE}: 파괴 및 판매 시 (레벨×2400)원 획득', 'level':25, 'amount':2400},
            '다마스커스 검':{'effect': f'{Fore.CYAN}페이백{Fore.WHITE}: 강화 시 (레벨×270)원 획득', 'level':28, 'amount':270},
            '엑스칼리버':{'effect': f'{Fore.BLUE}성스러운 빛{Fore.WHITE}: 강화 성공 시 75-(레벨×3)%로 2단계 강화', 'level':30},
            '다이아몬드 스워드':{'effect': f'{Fore.LIGHTCYAN_EX}아름다움의 정수{Fore.WHITE}: 파괴 및 판매 시 (보유 골드×0.0002)%로 다이아몬드 파편 획득,\n다이아몬드 파편은 15번의 강화동안 비용 100%절감, 성공 확률 1.5배, 성공 시 10000원 획득 효과 부여', 'level':32, 'count':0},
            '다인슬라이프':{'effect': f'{Fore.RED}불타는 가호{Fore.WHITE}: 검마다 25회에 한하여 파괴 시 보호', 'level':35, 'count':25},
            '붉은 자루의 검':{'effect': f'{Fore.MAGENTA}희미한 빛{Fore.WHITE}: 파괴 시 50%로 실패로 변경', 'level':38},
            '레바테인':{'effect': f'{Fore.RED}불타는 뜨거움{Fore.WHITE}: 성공 확률 (1+레벨×0.007)배 증가', 'level':40},
        }

        self.sword_list = [sword for sword, _ in self.sword_name.items()]

        self.sword_inventory = [0] * 2

        self.success_per = 100

        self.fail_per = 0

        self.coins = 100000
        
        self.total_price = 0

        self.price = 0

        self.sword_shards = 0
        self.item = {
            '파괴 방어권':{"effect":f"파괴 방어권을 {Fore.MAGENTA}(레벨)개{Fore.WHITE} 소모하여 파괴를 1회 방어합니다.(10 묶음)", "price": 100000, "count":0},
            '성공 강화권':{"effect":f"성공확률이 {Fore.GREEN}1.1배{Fore.WHITE} 증가합니다 성공에 실패해도 소모됩니다.(15 묶음)", "price": 35000, "count":0},
            '실패 유지권':{"effect":"실패시 레벨 퇴보가 없습니다.(15 묶음)", "price": 90000, "count":0},
        }

        self.item_list = [item for item, _ in self.item.items()]

    def percentage(self):
        self.success_per = 0
        self.fail_per = 0

        self.success_per += self.sword_lv
        if self.sword_lv >= 15:
            self.success_per += self.sword_lv * 1.00999

        if self.item['성공 강화권']['count'] > 0:
            self.success_per = self.success_per - ((100 - self.success_per) * 0.1)
        if '레바테인' in self.sword_inventory:
            self.success_per = self.success_per - ((100 - self.success_per) * 0.007 * self.sword_lv)
        if self.sword_name['다이아몬드 스워드']['count'] > 0:
            self.success_per = self.success_per - ((100 - self.success_per) * 0.5 * self.sword_lv)

        if self.success_per > 100:
            self.success_per = 100
        
        if self.sword_lv >= 20:
            self.fail_per += 3 * (self.sword_lv - 19)

    def enchant(self, choice):
        self.percentage()
        result = r.uniform(0, 100)
        if self.item['성공 강화권']['count'] > 0:
            self.item['성공 강화권']['count'] -= 1
        if self.sword_name['다이아몬드 스워드']['count'] > 0:
            self.sword_name['다이아몬드 스워드']['count'] -= 1

        if result >= self.success_per:
            self.sword_lv += 1
            if '엑스칼리버' in self.sword_inventory:
                if (75 - (self.sword_lv * 3)) > r.uniform(100, 0):
                    self.sword_lv += 1
                    print(f'{Fore.MAGENTA}엑스칼리버{Fore.WHITE} 효과로 레벨이 추가로 올랐다.')
                    t.sleep(0.5)
            return 'success'
        elif result <= self.fail_per:
            if '붉은 자루의 검' in self.sword_inventory and 50 > r.uniform(0, 100):
                input(f'검이 깨졌으나 {Fore.MAGENTA}붉은 자루의 검{Fore.WHITE} 효과로 방어했다.')
                if self.item['실패 유지권']['count'] > 0:
                    self.item['실패 유지권']['count'] -= 1
                    return 'down_save'
                else:
                    self.sword_lv -= 1
                    return 'down'
            elif '다인슬라이프' in self.sword_inventory and self.sword_name['다인슬라이프']['count'] > 0:
                self.sword_name['다인슬라이프']['count'] -= 1
                if choice == '10':
                    print(f'검이 깨졌으나 {Fore.MAGENTA}다인슬라이프{Fore.WHITE} 효과로 방어했다.')
                    t.sleep(0.5)
                else:
                    input(f'검이 깨졌으나 {Fore.MAGENTA}다인슬라이프{Fore.WHITE} 효과로 방어했다.')
                return 'down_save'
            elif self.item['파괴 방어권']['count'] >= self.sword_lv:
                self.item['파괴 방어권']['count'] -= self.sword_lv
                print(f'파괴 방어권 {self.sword_lv}개 소모')
                t.sleep(0.2)
                return 'fail_save'
            elif self.sword_shards >= self.sword_lv:
                if choice != '10':
                    while True:
                        sel = input(f'검 파편 {Fore.RED}{self.sword_lv}{Fore.WHITE}개를 소모하여 파괴를 방어(현재 {self.sword_shards}개 보유)\n[1]: 방어 [2]: 포기\n: ')
                        if sel == '1':
                            self.sword_shards -= self.sword_lv
                            print('검 파괴를 방어했다.')
                            t.sleep(0.3)
                            return 'fail_save'
                        elif sel == '2':
                            t.sleep(0.3)
                            return 'fail'
                        else:
                            print('잘못된 선택')
                            t.sleep(0.3)
                            os.system('cls')
                            continue
                else:
                    if self.sword_shards >= self.sword_lv:
                        print(f'검 파편 {Fore.RED}{self.sword_lv}{Fore.WHITE}개를 소모하여 파괴를 방어했다')
                        return 'fail_save'
            else:
                if '골든 스워드' in self.sword_inventory:
                    earn_coins = self.sword_lv * self.sword_name['골든 스워드']['amount']
                    self.coins += earn_coins
                    if choice == '10':
                        print(f'{Fore.MAGENTA}골든 스워드{Fore.WHITE}의 효과로 {earn_coins}코인을 얻었다.')
                        t.sleep(0.5)
                    else:
                        input(f'{Fore.MAGENTA}골든 스워드{Fore.WHITE}의 효과로 {earn_coins}코인을 얻었다.')
                
                self.sword_name['다인슬라이프']['count'] = 25
                if '다이아몬드 스워드' in self.sword_inventory:
                    self.sword_name['다이아몬드 스워드']['count'] = 15

                return 'fail'
        else:
            if self.sword_lv > 15:
                if self.item['실패 유지권']['count'] > 0:
                    self.item['실패 유지권']['count'] -= 1
                    return 'down_save'
                else:
                    self.sword_lv -= 1
                    return 'down'
            else:
                return 'down_save'
            
    def enchant_result(self, result, choice):
        if result == 'success':
            print(f'{Fore.GREEN}강화 성공!{Fore.WHITE}')
            if self.sword_name['다이아몬드 스워드']['count'] > 0:
                self.coins += 10000
        elif result == 'fail':
            if choice == 10:
                print(f'{Fore.RED}검이 깨졌다.{Fore.WHITE}')
                t.sleep(0.3)
            else:
                input(f'{Fore.RED}검이 깨졌다.{Fore.WHITE}')
            if self.sword_lv >= 20:
                max = self.sword_lv * 10
                earn_shard = r.randint(max - 199, max)
                print(f'검의 파편 {earn_shard}개 획득')
                self.sword_shards += earn_shard
                t.sleep(0.3)
            self.define_price()
            self.sword_lv = 0
            self.total_price = 0

        elif result == 'fail_save':
            if choice == '10':
                print(f'{Fore.RED}검이 깨졌으나 {Fore.CYAN}방어했다.{Fore.WHITE}')
                t.sleep(0.1)
            else:
                input(f'{Fore.RED}검이 깨졌으나 {Fore.CYAN}방어했다.{Fore.WHITE}')
        elif result == 'down':
            print(f'강화 실패로 {Fore.RED}한단계 내려갔다.{Fore.WHITE}')
            self.total_price = 0
        elif result == 'down_save':
            print(f'강화에 실패했으나 {Fore.CYAN}단계는 유지됐다.{Fore.WHITE}')
            self.total_price = 0
        t.sleep(0.3)
        os.system('cls')

    def shop(self): 
        while True:
            i = 0

            print(f'[{self.coins}코인 보유]')
        
            for item, info in self.item.items():
                i += 1
                print(f'[{i}][{Fore.YELLOW}{item}{Fore.WHITE}]: {info['effect']} ({info['price']}코인)')
            print(f'[{Fore.RED}X{Fore.WHITE}]: 나가기')
            choice = input(': ')

            try:
                choice = int(choice)
            except:
                if choice.capitalize() == 'X':
                    os.system('cls')
                    break
                else:
                    print('잘못된 선택. 다시 선택하세요')
                    t.sleep(0.3)
                    os.system('cls')
                    continue

            if choice > len(self.item_list) or choice <= 0:
                print('잘못된 선택. 다시 선택하세요')
                t.sleep(0.3)
                os.system('cls')
                continue

            item = self.item_list[choice - 1]

            if self.coins >= self.item[item]['price']:
                print(f'{Fore.YELLOW}{item}{Fore.WHITE} 구매완료!')
                self.coins -= self.item[item]['price']
                if item == '파괴 방어권':
                    self.item[item]['count'] += 10
                if item == '성공 강화권':
                    self.item[item]['count'] += 15
                if item == '실패 유지권':
                    self.item[item]['count'] += 15
                t.sleep(0.3)
                os.system('cls')
                continue
            else:
                print('돈이 부족합니다.')
                t.sleep(0.3)
                os.system('cls')
                continue

    def get_sword(self):
        no_item = 0
        for sword, info in self.sword_name.items():
            if self.sword_lv == info['level']:
                self.define_price()
                self.sword_lv = 0
                self.total_price = 0
                print('해당 검을 보관했다.')
                self.sword_inventory.insert(0, sword)
            else:
                no_item += 1
            if len(self.sword_inventory) > 3:
                t.sleep(0.5)
                if self.sword_inventory[2] != 0:
                    print(f'{Fore.MAGENTA}{sword}{Fore.WHITE}을(를) 보관한 대신 {Fore.MAGENTA}{self.sword_inventory[2]}{Fore.WHITE}을(를) {Fore.RED}버렸다{Fore.WHITE}.')
                    t.sleep(0.7)
                self.sword_inventory.pop(2)
        if no_item >= len(self.sword_list):
            print('이 검은 보관할 수 없다.')

        self.sword_name['다인슬라이프']['count'] = 25
        
    def define_price(self):
        self.price = 0
        self.price = m.ceil(self.sword_lv ** 1.5) * 60
        if self.loan_num > 0:
            self.price = m.ceil(self.price * (1.1 ** self.loan_num))

    def select(self):
        while True:
            self.percentage()
            self.define_price()

            print(f'[{self.coins}코인 보유] [현재 {self.sword_lv}.Lv] ', end = '')

            if self.sword_name['다이아몬드 스워드']['count'] > 0:
                print(f'[+{Fore.LIGHTCYAN_EX}다이아몬드 파편{Fore.WHITE}]({self.sword_name['다이아몬드 스워드']['count']}개)', end = '')

            for sword in self.sword_inventory:
                if sword != 0:
                    print(f'[+{Fore.MAGENTA}{sword}{Fore.WHITE}]', end = '')
                    if sword == '다인슬라이프':
                        print(f"({self.sword_name[sword]['count']}회 남음)", end = '')
                    print(' ', end = '')

            for item, info in self.item.items():
                if info['count'] > 0:
                    print(f'[+{item} ({info['count']})] ', end = '')
                    
            for sword, info in self.sword_name.items():
                if self.sword_lv == info['level']:
                    print(f'\n[{Fore.MAGENTA}{sword}{Fore.WHITE}| {info['effect']}]', end = '')

            print('')

            choice = input(f"[1 or Enter]: {Fore.YELLOW}강화하기{Fore.WHITE}(비용: {self.price}코인)({Fore.GREEN}성공:{100 - self.success_per}%{Fore.WHITE}, {Fore.RED}파괴:{self.fail_per}%{Fore.WHITE})\n[10]: {Fore.YELLOW}10연속 강화하기{Fore.WHITE}\n[2]: {Fore.YELLOW}판매하기{Fore.WHITE}(5강부터 판매 가능)\n[3]: {Fore.YELLOW}보관하기{Fore.WHITE}\n[4]: {Fore.YELLOW}상점{Fore.WHITE}\n[5]: {Fore.YELLOW}대출받기{Fore.WHITE}(대출 시 강화비용 {Fore.RED}1.1{Fore.WHITE}배 증가)({self.loan_num}번 대출받음)\n: ")
            if choice == '1':
                if self.coins > self.price:
                    self.coins -= self.price
                    self.total_price += self.price 
                    if self.sword_lv >= 20:
                        self.total_price += 100

                    if '다마스커스 검' in self.sword_inventory:
                        self.coins += self.sword_lv * self.sword_name['다마스커스 검']['amount']

                    result = self.enchant(choice)

                    self.enchant_result(result, choice)

                else:
                    print('돈이 부족합니다.')
                    t.sleep(0.3)
                    os.system('cls')
                    continue

            elif choice == '2':
                if self.sword_lv >= 5:
                    earn_coins = self.total_price - 10000 + (self.sword_lv * 6000) 
                    self.coins += earn_coins
                    print(f"{earn_coins}코인을 획득했다.")
                    if '골든 스워드' in self.sword_inventory:
                            earn_coins = self.sword_lv * self.sword_name['골든 스워드']['amount']
                            self.coins += earn_coins
                            input(f'{Fore.MAGENTA}골든 스워드{Fore.WHITE}의 효과로 {earn_coins}코인을 추가로 얻었다.')
                    
                    if self.sword_lv >= 20:
                        max = self.sword_lv * 10
                        earn_shard = r.randint(max - 199, max)
                        print(f'검의 파편 {earn_shard}개 획득')
                        t.sleep(0.3)

                    self.sword_name['다인슬라이프']['count'] = 25
                    if '다이아몬드 스워드' in self.sword_inventory:
                        self.sword_name['다이아몬드 스워드']['count'] = 15
                    self.define_price()
                    self.sword_lv = 0
                    self.total_price = 0
                    t.sleep(0.3)
                    os.system('cls')
                    break
                else:
                    print("판매 불가")
                    t.sleep(0.3)
                    os.system('cls')
                    continue

            elif choice == '3':
                self.get_sword()
                t.sleep(0.5)
                os.system('cls')
                break

            elif choice == '4':
                os.system('cls')
                self.shop()

            elif choice == '5':
                print(f'{Fore.YELLOW}20000{Fore.WHITE}원을 대출받았다.')
                self.coins += 20000
                self.loan_num += 1
                print(f"대출을 받고 강화비용이 영구히 {Fore.RED}1.1{Fore.WHITE}배 증가했다.")
                t.sleep(0.5)
                os.system('cls')

            elif choice == '10':
                same_lv = 0
                return_break = 0
                os.system('cls')
                for i in range(10):
                    self.percentage()
                    self.define_price()
                    if self.coins > self.price:
                        print(f'[{self.coins}코인 보유] [현재 {self.sword_lv}.Lv] ', end = '')

                        if self.sword_name['다이아몬드 스워드']['count'] > 0:
                            print(f'[+{Fore.LIGHTCYAN_EX}다이아몬드 파편{Fore.WHITE}]({self.sword_name['다이아몬드 스워드']['count']}개)', end = '')

                        for sword in self.sword_inventory:
                            if sword != 0:
                                print(f'[+{Fore.MAGENTA}{sword}{Fore.WHITE}]', end = '')
                                if sword == '다인슬라이프':
                                    print(f"({self.sword_name[sword]['count']}회 남음)", end = '')
                                print(' ', end = '')

                        for item, info in self.item.items():
                            if info['count'] > 0:
                                print(f'[+{item} ({info['count']})] ', end = '')
                        
                        print(f'\n({Fore.GREEN}성공:{100 - self.success_per}%{Fore.WHITE}, {Fore.RED}파괴:{self.fail_per}%{Fore.WHITE})')
                        
                        for sword, info in self.sword_name.items():
                            if self.sword_lv == info['level'] and same_lv != info['level']:
                                print(f'[{Fore.MAGENTA}{sword}{Fore.WHITE}| {info['effect']}]를 보관한다.\n[1]: 한다  [2]: 안한다')
                                choice_1 = input(': ')

                                if choice_1 == '1':
                                    self.get_sword()
                                    t.sleep(0.5)
                                    os.system('cls')
                                    return_break = 1
                                    break
                                elif choice_1 == '2':
                                    same_lv = info['level']
                                    pass
                        
                        if return_break == 1:
                            break

                        self.coins -= self.price
                        self.total_price += self.price 
                        if self.sword_lv >= 20:
                            self.total_price += 100

                        if '다마스커스 검' in self.sword_inventory:
                            self.coins += self.sword_lv * self.sword_name['다마스커스 검']['amount']

                        result = self.enchant(choice)

                        print(f'[{i + 1}] ', end = '')

                        self.enchant_result(result, choice)
                        
                        if result == 'fail':
                            break
                    else:
                        print('돈이 부족합니다.')
                        t.sleep(0.3)
                        os.system('cls')
                        break
        

            else:
                if self.coins > self.price:
                    self.coins -= self.price
                    self.total_price += self.price 
                    if self.sword_lv >= 20:
                        self.total_price += 100
                    
                    if '다마스커스 검' in self.sword_inventory:
                        self.coins += self.sword_lv * self.sword_name['다마스커스 검']['amount']

                    result = self.enchant(choice)

                    self.enchant_result(result, choice)

                else:
                    print('돈이 부족합니다.')
                    t.sleep(0.3)
                    os.system('cls')
                    continue

    def in_game(self):
        while True:
            if self.sword_lv == 50:
                print(f'{Fore.GREEN}[YOU WIN!]{Fore.WHITE}')
                break
            self.select()

rng = RandomNunberGame() 

os.system('cls')
rng.in_game()