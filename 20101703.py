# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

visited = []
fail_list = []
rootUrl = "http://cspro.sogang.ac.kr/~gr120150253/"

def get(url, visited):
    if url+"\n" in visited:
        return 1
    else:
        return 0  # fill this.

def dfs(url, visited):
    addr = ""

    try:
        code = requests.get(url)
    except requests.exceptions:
        return
    
    # request 의 결과가 ok 이면 pass
    # 아니면 실패 리스트에 저장
    if code.ok == True:
        pass
    else:
        fail_list.append(url)
        return
    
    # 이미 방문했던 곳은 다시 방문 안함
    if get(url, visited) == 1:
        return

    if get(url, fail_list) == 1:
        return

    visited.append(url+"\n")

    soup = BeautifulSoup(code.content)
    content = soup.get_text()

    # Text 저장
    filename = "Output_" + str(("%04d" % len(visited))) + ".txt"
    fp_content = open(filename, "w")
    fp_content.write(content)
    fp_content.close()

    for link in soup.find_all('a'):
        url = link.get('href')
        txtUrl =  str(url)
        if len(txtUrl) > 0:     # href 가 null일 수 있으니 길이 체크
            if txtUrl[0] == "?" or txtUrl[0] == "#":    # ? 나 # 으로 시작하는 주소는 무시
                pass
            else:   # 상대 주소인지 절대 주소인지 확인
                if txtUrl.split("://")[0] == "http":
                    addr = txtUrl
                else:
                    addr = rootUrl + txtUrl
                dfs(addr,visited)

# 프로그램의 시작
dfs(rootUrl+"index.html", visited)
# URL 저장
fp_url = open("URL.txt", "w")
fp_url.writelines(visited)
fp_url.close()
