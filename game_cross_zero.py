import os
import time

class Games:
    pole = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-'],
    ]
    lin_a = [' ', 'A', 'B', 'C']
    lin_1 = [' ', '1', '2', '3']
    players = []
    message = ''
    def __init__(self):
        self.input_player(2)
        self.draw()

    def input_player(self, count_player: int):
        players = self.players
        for i in range(count_player):
            while True:
                name = input(f'Игрок {i+1}, введите ваше имя: ')
                if name:
                    players.append(name)
                    break
                else:
                    print('Вы не ввели ваше имя, попробуйте еще раз')


    def draw(self):
        for j in range(4):
            for i in range(4):
                if j == 0:
                    print(f' {self.lin_a[i]} ', end='')
                elif i == 0:
                    print(f' {self.lin_1[j]} ', end='')
                else:
                    print(f' {self.pole[j-1][i-1]} ', end='')
            print()
        if self.message:
            print(self.message)
            self.message = ''

    def go(self, player: int, hod: str):
        self.hod = hod
        self.player = player
        not_error = True
        ch = '-'
        if player == 1:
            ch = 'X'
        else:
            ch = 'O'
        if len(hod) == 2:
            i = hod[0]
            j = int(hod[1]) - 1
            if i.upper() in self.lin_a and str(j+1) in self.lin_1:
                for index, el in enumerate(['a', 'b', 'c'], 0):
                    if i == el:
                        if self.pole[j][index] == '-':
                            self.pole[j][index] = ch
                        else:
                            self.message = 'Место уже занято!'
                            not_error = False
            else:
                self.message = 'Ошибка ввода команды'
                not_error = False
        else:
            self.message = 'Ход некорректный'
            not_error = False
        return not_error

    def win_lose(self, player: int):
        pole = self.pole
        win = False
        count = 0
        if player == 1:
            ch = 'X'
        else:
            ch = 'O'
        for i in range(len(pole)):
            for j in range(len(pole[0])):
                if pole[i][j] == ch:
                    count += 1
                else:
                    break
            if count == 3:
                win = True
                break
            else:
                count = 0
        if not win:
            for i in range(len(pole)):
                for j in range(len(pole[0])):
                    if pole[j][i] == ch:
                        count += 1
                    else:
                        break
                if count == 3:
                    win = True
                    break
                else:
                    count = 0
        if not win:
            for i in range(len(pole)):
                if pole[i][i] == ch:
                    count += 1
                else:
                    break
            if count == 3:
                win = True
            else:
                win = False
                count = 0
        if not win:
            for i in range(len(pole)):
                if pole[(len(pole)-1)-i][i] == ch:
                    count += 1
                else:
                    break
            if count == 3:
                win = True
            else:
                win = False
                count = 0

        return win

    def game_go(self):
        play = True
        command = ''
        while True:
            if play:
                command = input(f'{self.players[0]} ваш ход: ')
                if self.go(1, command):
                    if self.win_lose(1):
                        self.message = f'{self.players[0]} - Вы победили'
                        self.draw()
                        break
                    else:
                        play = False
            else:
                command = input(f'{self.players[1]} ваш ход: ')
                if self.go(2, command):
                    if self.win_lose(2):
                        self.message = f'{self.players[1]} - Вы победили'
                        self.draw()
                        break
                    else:
                        play = True
            if self.full():
                self.message = 'У нас ничья, хорошо играем'
                self.draw()
                break
            self.draw()

    def full(self):
        pole = self.pole
        full = True
        for i in range(len(pole)):
            for j in range(len(pole[i])):
                if pole[i][j] == '-':
                    full = False
                    break
            if not full:
                break
        return full

x = Games()
x.game_go()
