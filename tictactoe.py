def plate(s):
    return """
┌─┬─┬─┐
│{0} │{1} │{2} │
├─┼─┼─┤
│{3} │{4} │{5} │
├─┼─┼─┤
│{6} │{7} │{8} │
└─┴─┴─┘
""".format(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8])


def game(s, n):
    marker = ["O","X"]
    coor = int(input(plate(s)+"\n플레이어"+str(n%2+1)+"의 차례입니다. 말을 놓을 칸의 숫자를 입력해주세요 : "))
    while True:
        if coor in s:
            break
        elif coor in [1,2,3,4,5,6,7,8,9]:
            coor = int(input(str(coor)+"자리에는 이미 말이 놓여있습니다. 다시 말을 놓을 칸의 숫자를 입력해주세요 : "))
        else:
            coor = int(input("잘못된 입력입니다. 다시 말을 놓을 칸의 숫자를 입력해주세요 : "))
    s[coor-1] = marker[(n)%2]
    res = end_confirm(s,marker[(n)%2])
    if res == 0 and n == 8:
        return 2, s
    return res, s


def end_confirm(s,m):
    for i in range(3):
        if s[i] == m:
            if s[i+3] == m and s[i+6] == m:
                return 1
        if s[i*3] == m:
            if s[i*3+1] == m and s[i*3+2] == m:
                return 1
    if s[0] == m:
        if s[4] == m and s[8] == m:
            return 1
    if s[2] == m:
        if s[4] == m and s[6] == m:
            return 1
    return 0


def system():
    while True:
        sys = int(input("종료:0, 리겜:1\n: "))
        if sys in [0,1]:
            return sys
        print("잘못된 입력입니다. 다시 입력해주세요.")

while True:
    print("""-------------TicTacToe-------------
    3개의 말을 이어 가로/세로/대각선으로 직선을 만드는 게임입니다.
    플레이어1(선공)은 O, 플레이어2(후공)은 X 표시가 본인의 말입니다.
    -----------------------------------\n\n게임을 시작합니다\n\n\n""")
    s = [1,2,3,4,5,6,7,8,9]
    n = 0
    while True:
        res, s = game(s,n)
        if res == 1:
            print(plate(s)+"\n플레이어"+str(n%2+1)+"의 승리입니다!\n\n")
            break
        elif res == 2:
            print(plate(s)+"\n무승부입니다!")
            break
        n += 1
    if system() == 0:
        print("프로그램을 종료합니다.")
        break
