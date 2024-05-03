import urllib.request
import pandas as pd
import json
import re

# 네이버 API 클라이언트 ID와 시크릿
client_id = 'uxBMxwJzw_zJHEfayokT'
client_secret = 'Naxf078JUD'

# 사용자로부터 검색어와 엑셀 파일명, 가져올 결과 수를 입력받음
print("\n\n-------------------------------------------------------------")
query = input("검색어 입력 : ")
query_encoded = urllib.parse.quote(query)
my_xlsx = input("엑셀 파일로 저장할 파일 이름 입력 : ")
end = int(input("가져올 데이터의 양 입력 : "))
print("-------------------------------------------------------------\n\n")

# 한 번에 가져올 결과 수 (API 요청 당 최대 100개의 결과)
display = 100

# 결과를 저장할 리스트
total_results = []

# 요청 헤더에 클라이언트 ID와 시크릿 추가
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

# 결과를 가져오기 위해 반복문 사용
start = 1

# 총 결과 수(end 값)까지 반복하여 가져오기
while start <= end:

    # 한 번에 가져올 결과 수가 남은 결과 수보다 많을 경우에는 최대 값으로 설정
    if end - start + 1 < display:
        display = end - start + 1

    # 네이버 검색 API 호출을 위한 URL 생성
    url = f"https://openapi.naver.com/v1/search/blog.json?query={query_encoded}&display={display}&start={start}"

    # HTTP 요청을 보내고 응답을 받음
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)

    # 응답 코드 확인
    if response.getcode() == 200:
        # 응답 본문을 읽어옴
        response_dict = json.loads(response.read().decode("utf-8"))
        # 검색 결과 중 내용만 추출하여 결과 리스트에 추가
        items = response_dict.get("items", [])
        for item in items:
            result = {
                "제목": re.sub('<.+?>', '', item["title"]),
                "게시글 링크": item["link"],
                "게시글 내용": re.sub('<.+?>', '', item["description"]),
                "블로그 이름": item["bloggername"],
                "블로그 링크": item["bloggerlink"],
                "게시 날짜": item["postdate"]
            }
            total_results.append(result)

    start += display  # 다음 요청을 위해 start 값 업데이트

# 결과를 데이터프레임으로 변환
result_df = pd.DataFrame(total_results)

# 데이터프레임을 엑셀 파일로 저장
output_path = f"./TestData/{my_xlsx}.xlsx"
result_df.to_excel(output_path, index=False)

print("저장이 완료되었습니다.")
print("\n\n-------------------------------------------------------------\n\n")
