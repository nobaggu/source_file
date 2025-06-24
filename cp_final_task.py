import pickle, datetime

# 사용자의 식당 방문 내역 pickle 파일을 불러 함수
def data_load():
    # 파일을 읽어올때 파일이 존재하지 않을 경우 프로그램이 멈추는 경우를 위해 try문 사용
    try:
        with open('data.pickle', 'rb') as r:
            return pickle.load(r)
    except FileNotFoundError: # 파일이 존재하지 않을 경우의 에러
        return {}

# 사용자의 식당 방문 내역을 pickle 파일로 저장하는 함수
def data_save(data):
    with open('data.pickle', 'wb') as w:
        pickle.dump(data, w)

# 식당 방문 내역 dictionary 변수에 새로운 방문 내역을 업데이트하는 함수
def data_add(data):
    rest_list = list(data.keys())
    rest_name = input("식당 이름을 입력해주세요.\n:")
    rest_type = ""
    # 식당이 기존의 리스트에 없거나 철자를 잘못 쓴 경우 돌아가는 무한루프
    while True:
        if rest_name not in rest_list: # 입력한 식당 이름이 리스트에 없는 경우
            rest_name = input("해당 식당이 안암 식당 리스트에 존재하지 않습니다. 아래 리스트를 참고해서 철자를 확인하시고, 식당이름을 다시 입력해주세요. 만약 식당을 새롭게 리스트에 추가하시려면 '식당추가'를 입력해주세요.\n"+str(rest_list)+"\n:")
            if rest_name == '식당추가': # 리스트에 없는 식당을 새로 추가하는 경우
                rest_name = input("새로운 식당 이름을 입력해주세요.\n:")
                rest_type = input("등록하려는 식당이 양식이면 1, 일식이면 2, 중식이면 3, 한식이면 4, 기타면 5를 입력해주세요\n:")
                print("새로운 식당이 정상적으로 등록되었습니다.")
                break
        else: # 입력한 식당 이름이 리스트에 있는 경우
            break
    rest_date = input("식당 방문 날짜를 입력해주세요. ex)2024-01-01\n:")
    year = rest_date[0:4]
    month = rest_date[5:7]
    day = rest_date[8:10]
    # 식당 방문 날짜 입력이 형식에 따라 잘 이루어졌는지 확인하고 재입력을 받는 무한루프
    while True:
        try:
            # 날짜가 유효한 날짜인지 확인하는 조건문
            if int(year) <= 2024 and int(month) <= 12 and int(day) <= 31 and rest_date[4] == '-' and rest_date[7] == '-':
                break
            else:
                rest_date = input("잘못된 입력입니다. 다시 입력해주세요. ex)2024-01-01\n:")
        except ValueError: # 날짜자리에 잘못한 문자가 들어갈 경우의 에러
            rest_date = input("잘못된 입력입니다. 다시 입력해주세요. ex)2024-01-01\n:")

    # get() 함수를 이용하여 새로 추가된 식당의 경우에도 data의 value를 잘가져옴
    rest_update = data.get(rest_name, [rest_date, rest_type, 0])
    rest_update[0] = rest_date # 방문 날짜 업데이트
    rest_update[2] += 1 # 방문 횟수 업데이트
    data[rest_name] = rest_update # data 변수에 업데이트
    print("식당 방문 내역이 정상적으로 업데이트 되었습니다.")
    return data

# 식당 방문 내역 dictionary를 바탕으로 식당 추천을 해주는 함수
def recommend(data):
    rest_list = list(data.keys())
    rest_name = input("가고 싶은 안암 식당 이름을 입력해주세요.\n")
    rest_type = ""
    # 식당이 기존의 리스트에 없거나 철자를 잘못 쓴 경우 돌아가는 무한루프
    while True:
        if rest_name not in rest_list: # 입력한 식당 이름이 리스트에 없는 경우
            rest_name = input("해당 식당이 안암 식당 리스트에 존재하지 않습니다. 아래 리스트를 참고해서 철자를 확인하시고, 식당이름을 다시 입력해주세요. 만약 식당을 새롭게 리스트에 추가하시려면 '식당추가'를 입력해주세요.\n"+str(rest_list)+"\n:")
            if rest_name == '식당추가': # 리스트에 없는 식당을 새로 추가하는 경우
                rest_name = input("새로운 식당 이름을 입력해주세요.\n:")
                rest_type = input("등록하려는 식당이 양식이면 1, 일식이면 2, 중식이면 3, 한식이면 4, 기타면 5를 입력해주세요\n:")
                return "새로운 식당이 정상적으로 등록되었습니다."
        else: # 입력한 식당 이름이 리스트에 있는 경우
            break
    last_visit_date, food_genre, visit_count = data[rest_name]
    if last_visit_date == '': # 아직 방문하지 않아 식당 방문 날짜가 없는 경우 예외처리
      return "이식당을 방문한 적이 없습니다. 새로운 식당을 가보는 것도 좋은 선택일거 같아요!"
    last_visit_date = datetime.datetime.strptime(last_visit_date, '%Y-%m-%d')
    days_since_last_visit = (datetime.datetime.now() - last_visit_date).days
    result = f"{rest_name} 식당을 방문한 날짜는{last_visit_date.strftime('%Y 년 %m 월 %d 일')}이며, 방문한 횟수는{visit_count}번입니다.\n"
    result += f"마지막 방문으로부터 {days_since_last_visit}일이 지났습니다.\n"
    if visit_count >= 3 and days_since_last_visit >= 30:
        result += "이 식당을 다시 방문해보세요!"
    elif visit_count >= 3 and days_since_last_visit <= 30:
        result += "좋아하는 식당이더라도 최근에 갔으므로 다른 곳을 도전해보시는게 어떨까요?"
    return result

# 메인 함수
def main():
    while True:
        sys = input("식당 추천을 받으시려면 1, 식당 방문 내역을 추가하시려면 2, 종료하시려면 0을 입력해주세요.\n:")
        if sys == '0':
            print('프로그램을 종료합니다.')
            break
        elif sys == '1':
            print(recommend(data_load()))
        elif sys == '2':
            data_save(data_add(data_load()))
        else:
            print("잘못된 입력입니다.")

if __name__ == '__main__':
    main()
