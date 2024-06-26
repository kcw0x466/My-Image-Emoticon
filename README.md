# My-Image-Emoticon
나만의 이미지들을 채팅 프로그램(카카오톡 PC버전, 디스코드 등)에 이모티콘으로 바로 사용할수있는 프로그램

## 개발 동기
예전부터 여러 커뮤니티 사이트에서 사용하는 이미지들(디시콘, 아카콘 등)을 직접 찾아서 채팅 이모티콘으로 많이 사용해왔는데 직접 이미지 파일들을 찾어서 전송하는 과정이 오래걸려 좀 더 빠르게 이모티콘(이미지 파일)을 선택해서 전송하는 프로그램을 개발하고 싶었습니다. 

## 기능
  * <img src="./icon/add_box.svg" width="18px" height="18px"> 버튼으로 탭과 탭 내에 들어갈 이모티콘들(이미지 파일들)을 추가
    * 추가된 이미지들은 100(가로) * 100(세로) 사이즈로 변경 후 저장됨 &rarr; 큰 사이즈의 이미지를 이모티콘으로 사용하기에는 부적절함
    * .jpg .jpeg .png 이미지 파일 지원
    * 움직이는 .gif 이미지 파일들은 지원 안함
  * <img src="./icon/delete.svg" width="18px" height="18px"> 버튼으로 이모티콘 탭 삭제 (탭 내에 들어있는 이모티콘 모두 삭제됨)
  * 전송할 이모티콘(이미지) 선택하면 바로 이미지 파일을 클립보드에 저장

## 사용법
전송할 이모티콘(이미지)를 선택해서 채팅 프로그램에 붙여넣기(Ctrl + V)를 하고 전송하면 됩니다.

## 언어, 라이브러리, 프레임워크
  * Python
  * Python 표준 라이브러리 - sys, os, shutil, io
  * PySide2
  * win32clipboard
  * Pillow
## 기타 사항
 * win32clipboard 라이브러리를 사용했으므로 윈도우에서만 사용 가능
