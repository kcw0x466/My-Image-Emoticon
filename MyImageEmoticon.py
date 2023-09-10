import sys
import os
import shutil
import win32clipboard
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QToolButton, QLineEdit, QTabWidget, QListView, QComboBox, QFileDialog
from PySide2.QtCore import Qt, QCoreApplication, QSize, QPoint
from PySide2.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem
from qt_material import apply_stylesheet
from io import BytesIO
from PIL import Image

emoticonTabs = [] # 탭에 들어갈 모든 이모티콘 관련 객체 및 데이터를 저장하는 리스트(전역 변수)

# 이모티콘 라벨 클래스 (QLabel 상속)
class EmoticonLabel(QLabel):
    selectedEmoticon = None # 선택된 이모티콘

    def __init__(self, imgFile, tab_index, img_index):
        super().__init__()

        # 이모티콘에 대한 데이터(이미지 경로, 탭 위치, 탭 내에 이미지 위치)를 객체 변수에 저장
        self.imgFile = imgFile
        self.tab_index = tab_index
        self.img_index = img_index

        self.setMargin(3) # Margin 3px로 설정
        self.setPixmap(QPixmap(self.imgFile).scaled(100, 100)) # 이미지를 100px * 100px 로 설정
        self.mousePressEvent = self.clickEmoticon # 이모티콘 라벨에 클릭 이벤트 연결

    def clickEmoticon(self, event):
        # 이전에 선택한 이모티콘 선택 해제
        if EmoticonLabel.selectedEmoticon != None:
            EmoticonLabel.selectedEmoticon.setStyleSheet("")

        EmoticonLabel.selectedEmoticon = self # 이모티콘 선택
        self.setStyleSheet("background-color: #2979ff; border-radius: 0px;") # 선택한 이모티콘 이미지 표시

        # 선택한 이모티콘 이미지를 클립보드로 복사 (윈도우 OS에서만 가능)
        image = Image.open(self.imgFile)
        output = BytesIO()
        image.convert("RGBA").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

# 이모티콘 추가 화면(다이얼로그)
class EmoticonTabAdd(QDialog):
    imageFileList = [] # 이미지 파일 경로 리스트
    itemList = QStandardItemModel() # ListView에 넣을 아이템 리스트
    
    def __init__(self):
        super().__init__()
        self.initUI() # UI 구성
        self.show()

    # UI 구성 메소드
    def initUI(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('이모티콘 탭 추가')
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint) # 창 제목, 종료 버튼만 보이기
        self.setWindowIcon(QIcon("./icon/add_box.svg"))
        self.setFixedSize(QSize(460, 360)) # 창 사이즈 460 * 360

        # 레이아웃 및 위젯 설정
        VBox = QVBoxLayout()
        TopHBox = QHBoxLayout()
        MidHBox = QHBoxLayout()
        BottomHBox = QHBoxLayout()

        TopHBox.addWidget(QLabel("탭 이름"))
        self.tabNameInput = QLineEdit()
        TopHBox.addWidget(self.tabNameInput)

        ListView = QListView()
        ListView.setModel(EmoticonTabAdd.itemList)
        emoticon_add_btn = QPushButton("이모티콘 추가")
        emoticon_add_btn.clicked.connect(self.EmoticonAddFileDialog)
        MidHBox.addWidget(ListView)
        MidHBox.addWidget(emoticon_add_btn)

        BottomHBox.addStretch()
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.dialogClose)
        BottomHBox.addWidget(cancel_btn)
        ok_btn = QPushButton("확인")
        ok_btn.clicked.connect(self.OkBtnEvent)
        BottomHBox.addWidget(ok_btn)

        VBox.addLayout(TopHBox)
        VBox.addLayout(MidHBox)
        VBox.addLayout(BottomHBox)

        self.setLayout(VBox)

    # 파일 다이얼로그 및 선택한 파일 경로 ListView로 보여주는 메소드
    def EmoticonAddFileDialog(self):
        EmoticonTabAdd.imageFileList = QFileDialog.getOpenFileNames(self, "이미지 파일들을 선택", "./", "Image File(*.png *.jpg *.jpeg *.bmp);;")[0]
        for path in EmoticonTabAdd.imageFileList:
            EmoticonTabAdd.itemList.appendRow(QStandardItem(path))

    # 확인 버튼 누를시 이모티콘 추가되는 메소드
    def OkBtnEvent(self):
        TabName = self.tabNameInput.text() # 이모티콘 탭 이름
        save_path = './emoticons/' + TabName # 이모티콘 저장 경로
        os.makedirs(save_path, exist_ok = True) # 디렉토리 생성

        # 파일 다이얼로그에서 선택한 이미지 파일들을 100 * 100 사이즈로 저장
        for file in EmoticonTabAdd.imageFileList:
            fileName = file.split('/').pop()
            img = Image.open(file)
            img.resize((100, 100)).save(save_path + '/' + fileName)
        
        # 이모티콘 이미지 다시 불러오기
        emoticonTabs.clear()
        Main.TabWidget.clear()
        Main.loadEmoticon()

        self.dialogClose()

    # 창 종료 메소드
    def dialogClose(self):
        # 파일 다이얼로그에서 선택한 이미지 파일들 모두 지우기
        EmoticonTabAdd.imageFileList.clear()
        EmoticonTabAdd.itemList.clear()
        self.close()

class EmoticonRemove(QDialog):
    comboBox = None
    selectedTab = None

    def __init__(self):
        super().__init__()
        self.initUI() # UI 구성
        self.initComboBox() 
        self.show()
    
    # UI 구성 메소드
    def initUI(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('이모티콘 제거')
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("./icon/delete.svg"))
        self.setFixedSize(QSize(260, 120))

        # 레이아웃 및 위젯 설정
        VBox = QVBoxLayout()
        EmoticonRemove.comboBox = QComboBox()
        EmoticonRemove.comboBox.setStyleSheet("color: rgb(255, 255, 255)") # 콤보박스 글씨 색상 흰색으로 설정
        EmoticonRemove.comboBox.activated[str].connect(self.selectTab) # 콤보박스 선택 이벤트 추가
        HBox = QHBoxLayout()
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.dialogClose)
        ok_btn = QPushButton("확인")
        ok_btn.clicked.connect(self.OkBtnEvent)
        HBox.addWidget(cancel_btn)
        HBox.addWidget(ok_btn)
        VBox.addWidget(EmoticonRemove.comboBox)
        VBox.addStretch()
        VBox.addLayout(HBox)
        self.setLayout(VBox)

    # 콤보박스에 이모티콘 탭 이름들 넣는 메소드
    def initComboBox(self):
        for tabName in os.listdir('./emoticons'):
            EmoticonRemove.comboBox.addItem(tabName)

    # 탭 선택 메소드
    def selectTab(self, text):
        EmoticonRemove.selectedTab = text

    # 확인 버튼 누를시 이모티콘 탭 삭제되는 메소드
    def OkBtnEvent(self):
        del_dir = './emoticons/' + EmoticonRemove.selectedTab
        shutil.rmtree(del_dir)
        emoticonTabs.clear()
        Main.TabWidget.clear()
        Main.loadEmoticon()
        self.dialogClose()

    # 창 종료 메소드
    def dialogClose(self):
        self.close()

class Main(QMainWindow):
    TabWidget = None

    def __init__(self):
        super().__init__()
        self.initUI() # UI 구성
        Main.loadEmoticon() # 이모티콘 이미지들 불러오기
        
    # UI 구성 메소드
    def initUI(self):
        self.setFixedSize(QSize(490, 600)) # 창 사이즈 490 * 600
        self.setWindowFlags(Qt.FramelessWindowHint) # 창 프레임 없애기
        self.setWindowTitle('My Image Emoticon')

        # 이모티콘 추가 버튼, 이모티콘 제거 버튼, 프로그램 종료 버튼 설정
        add_btn = QToolButton()
        add_btn.clicked.connect(self.addEmoticon)
        del_btn = QToolButton()
        del_btn.clicked.connect(self.removeEmoticonTab)
        close_btn = QToolButton()
        add_btn.setIcon(QIcon("./icon/add_box.svg"))
        del_btn.setIcon(QIcon("./icon/delete.svg"))
        close_btn.setIcon(QIcon("./icon/close.svg"))
        add_btn.setIconSize(QSize(40, 40))
        del_btn.setIconSize(QSize(40, 40))
        close_btn.setIconSize(QSize(40, 40))
        close_btn.clicked.connect(QCoreApplication.instance().quit)

        # 레이아웃 설정
        Vbox = QVBoxLayout()
        Top_Hbox = QHBoxLayout()
        Bottom_HBox = QHBoxLayout()
        TopWidget = QWidget()
        Main.TabWidget = QTabWidget()
        TopWidget.mousePressEvent = self.window_mousePressEvent
        TopWidget.mouseMoveEvent = self.window_mouseMoveEvent
        Top_Hbox.addWidget(TopWidget)
        Top_Hbox.addWidget(close_btn)
        Bottom_HBox.addWidget(add_btn)
        Bottom_HBox.addWidget(del_btn)
        Bottom_HBox.addStretch()
        
        Vbox.addLayout(Top_Hbox)
        Vbox.addWidget(Main.TabWidget)
        Vbox.addLayout(Bottom_HBox)

        MainWidget = QWidget()
        MainWidget.setLayout(Vbox)

        self.setCentralWidget(MainWidget)

    # 이모티콘 탭 및 이미지들을 추가할수있는 창을 불러오는 메소드
    def addEmoticon(self):
        emoticonAddWindow = EmoticonTabAdd()
        emoticonAddWindow.exec_()

    # 이모티콘 탭을 제거할수있는 창을 불러오는 메소드
    def removeEmoticonTab(self):
        emoticonRemoveWindow = EmoticonRemove()
        emoticonRemoveWindow.exec_()

    # 이모티콘 이미지들을 불러오는 메소드
    @staticmethod
    def loadEmoticon():
        i = 0 # 탭 인덱스
        path = "./emoticons" # 이모티콘 이미지들을 불러오는 경로

        # 이모티콘 이미지들을 불러와서 탭 추가 및 그리드 레이아웃으로 정렬하는 알고리즘 
        for tabName in os.listdir(path):
            emoticonTabs.append((QScrollArea(), QWidget(), QGridLayout(), list()))
            emoticonTabs[i][1].setLayout(emoticonTabs[i][2])
            emoticonTabs[i][0].setWidgetResizable(True)
            emoticonTabs[i][0].setWidget(emoticonTabs[i][1])

            img_list = os.listdir(path + '/' + tabName)
            img_count = len(img_list)

            # 기본 4행 4열 그리드 레이아웃 
            col_count = 4
            row_count = 4
            
            # 행이 더 필요할 경우 행 추가
            if (img_count // col_count) >= 4:
                row_count = img_count // col_count
                if (img_count % col_count) > 0:
                    row_count += 1
             
            img_index = 0 # 탭 내에 이미지 순서

            for row in range(row_count):
                for col in range(col_count):
                    if img_index > img_count - 1: # 그리드 레이아웃에 남는 칸들을 빈 라벨로 채움
                        empty_label = QLabel()
                        empty_label.setStyleSheet("background-color: #31363b;")
                        emoticonTabs[i][2].addWidget(empty_label, row, col)
                    else:
                        imgFile = path + '/' + tabName + '/' + img_list[img_index] # 이모티콘 이미지 파일 경로
                        emoticonTabs[i][3].append(EmoticonLabel(imgFile, i, img_index))
                        emoticonTabs[i][2].addWidget(emoticonTabs[i][3][img_index], row, col, alignment=Qt.AlignmentFlag.AlignTop)
                        img_index += 1

            Main.TabWidget.addTab(emoticonTabs[i][0], tabName) # 탭 추가
            i += 1

    # 프로그램 창 상단 부분을 잡고 창을 움직이게하는 메소드
    def window_mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def window_mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    apply_stylesheet(app, theme = 'dark_blue.xml') # qt-material 테마 설정
    window.show()
    app.exec_()