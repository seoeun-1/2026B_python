

numbers = [273, 103, 5, 32, 65, 9, 72, 800, 99]

for number in numbers:
    print(number, "는", len(str(number)), "자릿수입니다.")
    
for number in numbers:
    if number % 2 == 0:
        print(number, "는 홀수입니다.")
    else:
        print(number, "는 짝수입니다.")
        

character = {
    "name": "기사",
    "level": 12,
    "items": {
        "sword": "불꽃의 검",
        "armor": "풀플레이트"
    },
    "skill": ["베기", "세게 베기", "아주 세게 베기"]
}