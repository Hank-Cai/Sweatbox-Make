#coding=utf-8
import json
import os
import random
import sys

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QSpinBox, QComboBox, QMessageBox,
                             QGroupBox, QGridLayout, QTabWidget, QFileDialog,
                             QInputDialog, QCheckBox)
from adf.model import process_position,validate_coordinate_format,convert_runway,batch_convert

script_dir=os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


class FlightPlanGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 先定义所有属性
        self.topmost_button = QPushButton("置顶")
        self.ini_input = QLineEdit()
        self.dep_input = QComboBox()
        self.arr_input = QComboBox()
        self.rfl_input = QComboBox()
        self.alti_input = QComboBox()
        self.typ_input = QLineEdit("A320")
        self.pos_input = QLineEdit("N30.5,E120.5")
        self.head_input = QSpinBox()
        self.rte_input = QLineEdit()
        self.generate_btn = QPushButton("生成飞行计划")
        self.save_btn = QPushButton("保存到文件")
        self.output_text = QTextEdit()
        self.batch_count = QSpinBox()
        self.batch_ini = QLineEdit()
        self.batch_generate_btn = QPushButton("批量生成")
        self.batch_output = QTextEdit()
        self.tower_ini_input = QLineEdit()
        self.tower_dep_input = QComboBox()
        self.tower_arr_input = QComboBox()
        self.tower_rfl_input = QComboBox()
        self.tower_alti_input= QLineEdit()
        self.tower_typ_input = QLineEdit("A320")
        self.gate_input = QLineEdit("")
        self.tower_rte_input = QLineEdit()
        self.tower_generate_btn = QPushButton("生成飞行计划")
        self.tower_save_btn = QPushButton("保存到文件")
        self.tower_output = QTextEdit()
        self.app_ini_input = QLineEdit()
        self.app_dep_input = QComboBox()
        self.app_arr_input = QComboBox()
        self.app_rfl_input = QComboBox()
        self.app_typ_input = QLineEdit("")
        self.app_alti_input = QComboBox()
        self.app_star_input=QLineEdit("")
        self.app_pos_input=QLineEdit("N30.5,E120.5")
        self.app_head_input = QSpinBox()
        self.app_generate_btn = QPushButton("生成飞行计划")
        self.app_save_btn = QPushButton("保存到文件")
        self.app_output=QTextEdit()
        self.app_start_input=QSpinBox()
        self.rwy_start_input=QLineEdit("")
        self.rwy_end_input=QLineEdit("")
        self.rwy_number_input=QLineEdit("")
        self.rwy_generate_btn=QPushButton("生成跑道信息")
        self.rwy_save_btn=QPushButton("保存到文件")
        self.rwy_output=QTextEdit()
        # 新增：对向跑道勾选框
        self.rwy_opposite_checkbox = QCheckBox("自动创建对向跑道")
        
        # 新增：美化按钮
        self.style_dark_btn = QPushButton("深色主题")
        self.style_light_btn = QPushButton("浅色主题")
        self.style_blue_btn = QPushButton("蓝色主题")
        
        # 当前主题
        self.current_theme = "light"
        
        self.airlines = ["AHK","BJN","BJV","CAO","CBJ","CCA","CCD","CCO","CDC","CDG","CES","CFA","CFI","CFJ","CGZ","CHB","CHH","CJG","CKK","CNM","CPA","CQH","CQN","CSC","CSG","CSH","CSN","CSS","CSZ","CUA","CXA","CYZ","CYN"]
        self.airports = ["ZBAA","ZBAD","ZBDS","ZBDT","ZBER","ZBHH","ZBLA","ZBMZ","ZBOW","ZBTJ","ZBYN","ZGDY","ZGGG","ZGHA","ZGKL","ZGNN","ZGOW","ZGSZ","ZHCC","ZHES","ZHHH","ZHYC","ZJHK","ZJQH","ZJSY","ZLDH","ZLIC","ZLLL","ZLXN","ZLXY","ZPJH","ZPLJ","ZPMS","ZPPP","ZSAM","ZSCG","ZSCN","ZSFZ","ZSHC","ZSJN","ZSLG","ZSLY","ZSNB","ZSNJ","ZSNT","ZSOF","ZSPD","ZSQD","ZSQZ","ZSSH","ZSSS","ZSTX","ZSWH","ZSWX","ZSWZ","ZSYA","ZSYN","ZSYT","ZSYW","ZSZS","ZUCK","ZUGY","ZULS","ZUTF","ZUUU","ZUXC","ZWSH","ZWTN","ZWWW","ZYCC","ZYHB","ZYJM","ZYMD","ZYQQ","ZYTL","ZYTX","ZYYJ"]
        self.ALTI = {"600":2000,"900":3000,"1200":3900,"1500":4900,"1800":5900,"2100":6900,"2400":7900,"2700":8900,"3000":9800,"3300":10800,"3600":11800,"3900":12800,"4200":13800,"4500":14800,"4800":15700,"5100":16700,"5400":17700,"5700":18700,"6000":19700,"6300":20700,"6600":21700,"6900":22600,"7200":23600,"7500":24600,"7800":25600,"8100":26600,"8400":27600,"8900":29100,"9200":30100,"9500":31100,"9800":32100,"10100":33100,"10400":34100,"10700":35100,"11000":36100,"11300":37100,"11600":38100,"11900":39100,"12200":40100,"12500":41100,"13100":43000,"13700":44900,"14300":46900,"14900":48900,"15500":50900}
        self.Cruise = {"29100":89,"30100":92,"31100":95,"32100":98,"33100":101,"34100":104,"35100":107,"36100":110,"37100":113,"38100":116,"39100":119,"40100":122,"41100":125}
        
        
        window_icon=QIcon("window_icon.ico")
        self.route_path = "adf/RouteCheck.csv"
        self.sid_path="adf/STARSID.csv"
        self.gate_path="adf/Gate.json"
        
        # 然后初始化UI
        self.setWindowIcon(window_icon)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('模拟机文本生成器 v1.0')
        self.setGeometry(100, 100, 1000, 750)  # 增大窗口尺寸

        # 应用初始样式
        self.apply_theme("light")
        
        # 创建中心窗口和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建标题和置顶按钮
        title_layout = QHBoxLayout()
        title_label = QLabel("模拟机文本生成器")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3498db, stop:0.5 #2980b9, stop:1 #1f639b);
                color: white;
                border-radius: 8px;
                border: 2px solid #1f639b;
            }
        """)
        title_label.setMinimumHeight(60)

        # 创建置顶按钮
        self.topmost_button.setCheckable(True)
        self.topmost_button.setFixedSize(70, 45)
        self.topmost_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                border: none;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:checked:hover {
                background-color: #c0392b;
            }
        """)
        self.topmost_button.clicked.connect(self.toggle_topmost)
        
        # 创建主题切换按钮
        theme_layout = QHBoxLayout()
        self.style_light_btn.setFixedSize(80, 35)
        self.style_dark_btn.setFixedSize(80, 35)
        self.style_blue_btn.setFixedSize(80, 35)
        
        self.style_light_btn.clicked.connect(lambda: self.apply_theme("light"))
        self.style_dark_btn.clicked.connect(lambda: self.apply_theme("dark"))
        self.style_blue_btn.clicked.connect(lambda: self.apply_theme("blue"))
        
        theme_layout.addWidget(QLabel("主题:"))
        theme_layout.addWidget(self.style_light_btn)
        theme_layout.addWidget(self.style_dark_btn)
        theme_layout.addWidget(self.style_blue_btn)
        theme_layout.addStretch()

        # 添加到布局
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.topmost_button)
        
        main_layout.addLayout(title_layout)
        main_layout.addLayout(theme_layout)
        
        # 创建选项卡
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                margin-top: 5px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 10px 20px;
                margin-right: 3px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                color: #2c3e50;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
                border-bottom: 2px solid #2980b9;
            }
            QTabBar::tab:hover {
                background-color: #d5dbdb;
            }
        """)
        main_layout.addWidget(tabs)
        
        # 创建单个航班选项卡
        single_flight_tab = QWidget()
        single_layout = QVBoxLayout(single_flight_tab)
        single_layout.setSpacing(15)
        single_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建塔台航班选项卡
        tower_flight_tab = QWidget()
        tower_layout = QVBoxLayout(tower_flight_tab)
        tower_layout.setSpacing(15)
        tower_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建进近航班选项卡
        app_flight_tab=QWidget()
        app_layout=QVBoxLayout(app_flight_tab)
        app_layout.setSpacing(15)
        app_layout.setContentsMargins(15,15,15,15)
        
        # 控制权设置
        control_group = QGroupBox("控制权设置")
        control_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #2980b9;
            }
        """)
        control_layout = QHBoxLayout(control_group)
        control_label = QLabel("控制权所有席位:")
        control_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        control_layout.addWidget(control_label)
        self.ini_input.setPlaceholderText("请输入控制权席位...")
        self.ini_input.setMinimumHeight(35)
        self.ini_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        control_layout.addWidget(self.ini_input)
        single_layout.addWidget(control_group)
        
        # 航班信息
        flight_group = QGroupBox("航班信息")
        flight_group.setStyleSheet(control_group.styleSheet())
        flight_layout = QGridLayout(flight_group)
        flight_layout.setVerticalSpacing(12)
        flight_layout.setHorizontalSpacing(20)
        
        # 设置固定尺寸
        label_width = 120
        input_width = 200
        
        # DEP机场
        dep_label = QLabel("DEP机场:")
        dep_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        dep_label.setFixedWidth(label_width)
        flight_layout.addWidget(dep_label, 0, 0)
        self.dep_input.addItems(self.airports)
        self.dep_input.setEditable(True)
        self.dep_input.setFixedWidth(input_width)
        self.dep_input.setMinimumHeight(35)
        flight_layout.addWidget(self.dep_input, 0, 1)
        
        # ARR机场
        arr_label = QLabel("ARR机场:")
        arr_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        arr_label.setFixedWidth(label_width)
        flight_layout.addWidget(arr_label, 1, 0)
        self.arr_input.addItems(self.airports)
        self.arr_input.setEditable(True)
        self.arr_input.setFixedWidth(input_width)
        self.arr_input.setMinimumHeight(35)
        flight_layout.addWidget(self.arr_input, 1, 1)
        
        # 巡航高度
        rfl_label = QLabel("巡航高度:")
        rfl_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        rfl_label.setFixedWidth(label_width)
        flight_layout.addWidget(rfl_label, 2, 0)
        self.rfl_input.addItems(["29100", "30100", "31100", "32100", "33100", "34100",
                                "35100", "36100", "37100", "38100", "39100", "40100", "41100"])
        self.rfl_input.setFixedWidth(input_width)
        self.rfl_input.setMinimumHeight(35)
        flight_layout.addWidget(self.rfl_input, 2, 1)
        
        # 当前米制高度
        alti_label = QLabel("当前米制高度:")
        alti_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        alti_label.setFixedWidth(label_width)
        flight_layout.addWidget(alti_label, 3, 0)
        self.alti_input.addItems(list(self.ALTI.keys()))
        self.alti_input.setFixedWidth(input_width)
        self.alti_input.setMinimumHeight(35)
        flight_layout.addWidget(self.alti_input, 3, 1)
        
        # 机型
        typ_label = QLabel("机型:")
        typ_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        typ_label.setFixedWidth(label_width)
        flight_layout.addWidget(typ_label, 4, 0)
        self.typ_input.setFixedWidth(input_width)
        self.typ_input.setMinimumHeight(35)
        flight_layout.addWidget(self.typ_input, 4, 1)
        
        # 经纬度
        pos_label = QLabel("经纬度:")
        pos_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        pos_label.setFixedWidth(label_width)
        flight_layout.addWidget(pos_label, 5, 0)
        self.pos_input.setPlaceholderText("格式: N30.5,E120.5")
        self.pos_input.setFixedWidth(input_width)
        self.pos_input.setMinimumHeight(35)
        flight_layout.addWidget(self.pos_input, 5, 1)
        
        # 头朝向
        head_label = QLabel("头朝向:")
        head_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        head_label.setFixedWidth(label_width)
        flight_layout.addWidget(head_label, 6, 0)
        head_layout = QHBoxLayout()
        self.head_input.setRange(0, 360)
        self.head_input.setValue(0)
        self.head_input.setFixedWidth(100)
        self.head_input.setMinimumHeight(35)
        head_layout.addWidget(self.head_input)
        head_layout.addWidget(QLabel("度"))
        head_layout.addStretch()
        flight_layout.addLayout(head_layout, 6, 1)
        
        # 实际航路
        rte_label = QLabel("实际航路:")
        rte_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        rte_label.setFixedWidth(label_width)
        flight_layout.addWidget(rte_label, 7, 0)
        self.rte_input.setPlaceholderText("留空则使用数据库航路")
        self.rte_input.setFixedWidth(input_width)
        self.rte_input.setMinimumHeight(35)
        flight_layout.addWidget(self.rte_input, 7, 1)
        
        single_layout.addWidget(flight_group)
        
        # 按钮区域
        button_group = QGroupBox("操作")
        button_group.setStyleSheet(control_group.styleSheet())
        button_layout = QHBoxLayout(button_group)
        self.generate_btn.clicked.connect(self.generate_single_flight)
        self.generate_btn.setMinimumHeight(40)
        self.generate_btn.setIcon(QIcon.fromTheme("document-new"))
        button_layout.addWidget(self.generate_btn)

        self.save_btn.clicked.connect(self.save_single_to_file)
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setIcon(QIcon.fromTheme("document-save"))
        button_layout.addWidget(self.save_btn)
        
        single_layout.addWidget(button_group)
        
        # 输出区域
        output_group = QGroupBox("输出")
        output_group.setStyleSheet(control_group.styleSheet())
        output_layout = QVBoxLayout(output_group)
        self.output_text.setMinimumHeight(250)
        self.output_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background-color: #f8f9fa;
            }
        """)
        output_layout.addWidget(self.output_text)
        single_layout.addWidget(output_group)
        
        # 批量航班选项卡
        batch_flight_tab = QWidget()
        batch_layout = QVBoxLayout(batch_flight_tab)
        batch_layout.setSpacing(15)
        batch_layout.setContentsMargins(15, 15, 15, 15)
        
        batch_group = QGroupBox("批量生成设置")
        batch_group.setStyleSheet(control_group.styleSheet())
        batch_grid = QGridLayout(batch_group)
        batch_grid.setVerticalSpacing(12)
        batch_grid.setHorizontalSpacing(20)
        
        batch_grid.addWidget(QLabel("机组数量:"), 0, 0)
        self.batch_count.setRange(1, 100)
        self.batch_count.setValue(5)
        self.batch_count.setFixedWidth(100)
        self.batch_count.setMinimumHeight(35)
        batch_grid.addWidget(self.batch_count, 0, 1)
        
        batch_grid.addWidget(QLabel("控制权所有席位:"), 1, 0)
        self.batch_ini.setPlaceholderText("请输入控制权席位...")
        self.batch_ini.setFixedWidth(input_width)
        self.batch_ini.setMinimumHeight(35)
        batch_grid.addWidget(self.batch_ini, 1, 1)
        
        batch_layout.addWidget(batch_group)
        
        batch_button_group = QGroupBox("操作")
        batch_button_group.setStyleSheet(control_group.styleSheet())
        batch_button_layout = QHBoxLayout(batch_button_group)
        self.batch_generate_btn.clicked.connect(self.generate_batch_flights)
        self.batch_generate_btn.setMinimumHeight(40)
        batch_button_layout.addWidget(self.batch_generate_btn)
        batch_layout.addWidget(batch_button_group)
        
        batch_output_group = QGroupBox("批量输出")
        batch_output_group.setStyleSheet(control_group.styleSheet())
        batch_output_layout = QVBoxLayout(batch_output_group)
        self.batch_output.setMinimumHeight(300)
        self.batch_output.setStyleSheet(self.output_text.styleSheet())
        batch_output_layout.addWidget(self.batch_output)
        batch_layout.addWidget(batch_output_group)
        
        # 塔台选项卡
        # 控制权设置
        control_grooup = QGroupBox("控制权设置")
        control_grooup.setStyleSheet(control_group.styleSheet())
        control_layout = QHBoxLayout(control_grooup)
        control_layout.addWidget(QLabel("控制权所有席位:"))
        self.tower_ini_input.setPlaceholderText("请输入控制权席位...")
        self.tower_ini_input.setMinimumHeight(35)
        control_layout.addWidget(self.tower_ini_input)
        tower_layout.addWidget(control_grooup)
        
        # 航班信息
        flight_grooup = QGroupBox("航班信息")
        flight_grooup.setStyleSheet(control_group.styleSheet())
        flight_layout = QGridLayout(flight_grooup)
        flight_layout.setVerticalSpacing(12)
        flight_layout.setHorizontalSpacing(20)
        
        flight_layout.addWidget(QLabel("DEP机场:"), 0, 0)
        self.tower_dep_input.setEditable(True)
        self.tower_dep_input.addItems(self.airports)
        self.tower_dep_input.setFixedWidth(input_width)
        self.tower_dep_input.setMinimumHeight(35)
        flight_layout.addWidget(self.tower_dep_input, 0, 1)
        
        flight_layout.addWidget(QLabel("ARR机场:"), 1, 0)
        self.tower_arr_input.setEditable(True)
        self.tower_arr_input.addItems(self.airports)
        self.tower_arr_input.setFixedWidth(input_width)
        self.tower_arr_input.setMinimumHeight(35)
        flight_layout.addWidget(self.tower_arr_input, 1, 1)
        
        flight_layout.addWidget(QLabel("巡航高度:"), 2, 0)
        self.tower_rfl_input.addItems(["29100", "30100", "31100", "32100", "33100", "34100",
                                "35100", "36100", "37100", "38100", "39100", "40100", "41100"])
        self.tower_rfl_input.setFixedWidth(input_width)
        self.tower_rfl_input.setMinimumHeight(35)
        flight_layout.addWidget(self.tower_rfl_input, 2, 1)
        
        flight_layout.addWidget(QLabel("机场标高高度:"), 3, 0)
        self.tower_alti_input.setFixedWidth(input_width)
        self.tower_alti_input.setMinimumHeight(35)
        flight_layout.addWidget(self.tower_alti_input, 3, 1)
        
        flight_layout.addWidget(QLabel("机型:"), 4, 0)
        self.tower_typ_input.setFixedWidth(input_width)
        self.tower_typ_input.setMinimumHeight(35)
        flight_layout.addWidget(self.tower_typ_input, 4, 1)
        
        flight_layout.addWidget(QLabel("机位:"), 5, 0)
        self.gate_input.setPlaceholderText("请输入登机口...")
        self.gate_input.setFixedWidth(input_width)
        self.gate_input.setMinimumHeight(35)
        flight_layout.addWidget(self.gate_input, 5, 1)
        
        flight_layout.addWidget(QLabel("实际航路:"), 6, 0)
        self.tower_rte_input.setPlaceholderText("留空则使用数据库航路")
        self.tower_rte_input.setFixedWidth(input_width)
        self.tower_rte_input.setMinimumHeight(35)
        flight_layout.addWidget(self.tower_rte_input, 6, 1)
        
        tower_layout.addWidget(flight_grooup)
        
        # 按钮
        tower_button_group = QGroupBox("操作")
        tower_button_group.setStyleSheet(control_group.styleSheet())
        tower_button_layout = QHBoxLayout(tower_button_group)
        self.tower_generate_btn.clicked.connect(self.generate_tower_flights)
        self.tower_generate_btn.setMinimumHeight(40)
        tower_button_layout.addWidget(self.tower_generate_btn)

        self.tower_save_btn.clicked.connect(self.save_tower_to_file)
        self.tower_save_btn.setMinimumHeight(40)
        tower_button_layout.addWidget(self.tower_save_btn)
        
        tower_layout.addWidget(tower_button_group)
        
        # 输出区域
        tower_output_group = QGroupBox("输出")
        tower_output_group.setStyleSheet(control_group.styleSheet())
        tower_output_layout = QVBoxLayout(tower_output_group)
        self.tower_output.setMinimumHeight(250)
        self.tower_output.setStyleSheet(self.output_text.styleSheet())
        tower_output_layout.addWidget(self.tower_output)
        tower_layout.addWidget(tower_output_group)
        
        # 进近选项卡
        control_app_group=QGroupBox("控制权设置")
        control_app_group.setStyleSheet(control_group.styleSheet())
        control_app_layout=QHBoxLayout(control_app_group)
        control_app_layout.addWidget(QLabel("控制权所有席位:"))
        self.app_ini_input.setPlaceholderText("请输入控制权席位...")
        self.app_ini_input.setMinimumHeight(35)
        control_app_layout.addWidget(self.app_ini_input)
        app_layout.addWidget(control_app_group)
        
        app_flight_group=QGroupBox("航班信息")
        app_flight_group.setStyleSheet(control_group.styleSheet())
        app_flight_layout=QGridLayout(app_flight_group)
        app_flight_layout.setVerticalSpacing(12)
        app_flight_layout.setHorizontalSpacing(20)
        
        app_flight_layout.addWidget(QLabel("DEP机场:"), 0, 0)
        self.app_dep_input.setEditable(True)
        self.app_dep_input.addItems(self.airports)
        self.app_dep_input.setFixedWidth(input_width)
        self.app_dep_input.setMinimumHeight(35)
        app_flight_layout.addWidget(self.app_dep_input, 0, 1)
        
        app_flight_layout.addWidget(QLabel("ARR机场:"), 1, 0)
        self.app_arr_input.setEditable(True)
        self.app_arr_input.addItems(self.airports)
        self.app_arr_input.setFixedWidth(input_width)
        self.app_arr_input.setMinimumHeight(35)
        app_flight_layout.addWidget(self.app_arr_input, 1, 1)
        
        app_flight_layout.addWidget(QLabel("巡航高度:"), 2, 0)
        self.app_rfl_input.addItems(["29100", "30100", "31100", "32100", "33100", "34100",
                                "35100", "36100", "37100", "38100", "39100", "40100", "41100"])
        self.app_rfl_input.setFixedWidth(input_width)
        self.app_rfl_input.setMinimumHeight(35)
        app_flight_layout.addWidget(self.app_rfl_input, 2, 1)
        
        app_flight_layout.addWidget(QLabel("机型:"),3,0)
        self.app_typ_input.setFixedWidth(input_width)
        self.app_typ_input.setMinimumHeight(35)
        app_flight_layout.addWidget(self.app_typ_input,3,1)
        
        app_flight_layout.addWidget(QLabel("当前米制高度:"), 4, 0)
        self.app_alti_input.addItems(list(self.ALTI.keys()))
        self.app_alti_input.setFixedWidth(input_width)
        self.app_alti_input.setMinimumHeight(35)
        app_flight_layout.addWidget(self.app_alti_input,4 , 1)
        
        app_flight_layout.addWidget(QLabel("进/离场程序:"),5,0)
        self.app_star_input.setPlaceholderText("")
        self.app_star_input.setFixedWidth(input_width)
        self.app_star_input.setMinimumHeight(35)
        app_flight_layout.addWidget(self.app_star_input,5,1)
        
        app_flight_layout.addWidget(QLabel("经纬度:"),6,0)
        self.app_pos_input.setFixedWidth(input_width)
        self.app_pos_input.setMinimumHeight(35)
        app_flight_layout.addWidget(self.app_pos_input,6,1)
        
        app_flight_layout.addWidget(QLabel("头朝向:"), 7, 0)
        app_head_layout = QHBoxLayout()
        self.app_head_input.setRange(0, 360)
        self.app_head_input.setValue(0)
        self.app_head_input.setFixedWidth(100)
        self.app_head_input.setMinimumHeight(35)
        app_head_layout.addWidget(self.app_head_input)
        app_head_layout.addWidget(QLabel("度"))
        app_head_layout.addStretch()
        app_flight_layout.addLayout(app_head_layout, 7, 1)
        
        app_flight_layout.addWidget(QLabel("刷新时间："),8,0)
        app_start_layout=QHBoxLayout()
        self.app_start_input.setRange(0,3600)
        self.app_start_input.setValue(0)
        self.app_start_input.setFixedWidth(100)
        self.app_start_input.setMinimumHeight(35)
        app_start_layout.addWidget(self.app_start_input)
        app_start_layout.addWidget(QLabel("分钟"))
        app_start_layout.addStretch()
        app_flight_layout.addLayout(app_start_layout,8,1)

        app_layout.addWidget(app_flight_group)
        
        app_button_group = QGroupBox("操作")
        app_button_group.setStyleSheet(control_group.styleSheet())
        app_button_layout = QHBoxLayout(app_button_group)
        self.app_generate_btn.clicked.connect(self.generate_app_flights)
        self.app_generate_btn.setMinimumHeight(40)
        app_button_layout.addWidget(self.app_generate_btn)

        self.app_save_btn.clicked.connect(self.save_app_to_file)
        self.app_save_btn.setMinimumHeight(40)
        app_button_layout.addWidget(self.app_save_btn)
        
        app_layout.addWidget(app_button_group)
        
        app_output_group=QGroupBox("输出")
        app_output_group.setStyleSheet(control_group.styleSheet())
        app_output_layout=QVBoxLayout(app_output_group)
        self.app_output.setMinimumHeight(250)
        self.app_output.setStyleSheet(self.output_text.styleSheet())
        app_output_layout.addWidget(self.app_output)
        app_layout.addWidget(app_output_group)
        
        # 创建跑道信息选项卡的布局
        rwy_tab = QWidget()
        rwy_main_layout = QVBoxLayout(rwy_tab)
        rwy_main_layout.setSpacing(15)
        rwy_main_layout.setContentsMargins(15, 15, 15, 15)

        # 创建跑道信息设置的组框
        rwy_group = QGroupBox("跑道信息设置")
        rwy_group.setStyleSheet(control_group.styleSheet())
        rwy_grid_layout = QGridLayout(rwy_group)

        # 第1行：跑道编号
        rwy_grid_layout.addWidget(QLabel("跑道编号:"), 0, 0)
        self.rwy_number_input.setFixedWidth(input_width)
        self.rwy_number_input.setMinimumHeight(35)
        rwy_grid_layout.addWidget(self.rwy_number_input, 0, 1)
        
        # 第2行：对向跑道设置
        rwy_grid_layout.addWidget(QLabel(""), 1, 0)
        self.rwy_opposite_checkbox.setChecked(True)
        self.rwy_opposite_checkbox.setToolTip("勾选后自动生成对向跑道信息（如18R会自动生成36L）")
        rwy_grid_layout.addWidget(self.rwy_opposite_checkbox, 1, 1)
        
        # 第3行：起始跑道经纬度
        rwy_grid_layout.addWidget(QLabel("起始跑道经纬度:"), 2, 0)
        self.rwy_start_input.setFixedWidth(input_width)
        self.rwy_start_input.setMinimumHeight(35)
        rwy_grid_layout.addWidget(self.rwy_start_input, 2, 1)

        # 第4行：结束跑道经纬度
        rwy_grid_layout.addWidget(QLabel("结束跑道经纬度:"), 3, 0)
        self.rwy_end_input.setFixedWidth(input_width)
        self.rwy_end_input.setMinimumHeight(35)
        rwy_grid_layout.addWidget(self.rwy_end_input, 3, 1)

        rwy_main_layout.addWidget(rwy_group)

        # 创建操作按钮组
        rwy_button_group = QGroupBox("操作")
        rwy_button_group.setStyleSheet(control_group.styleSheet())
        rwy_button_layout = QHBoxLayout(rwy_button_group)
        self.rwy_generate_btn.clicked.connect(self.generate_rwy_info)
        self.rwy_generate_btn.setMinimumHeight(40)
        rwy_button_layout.addWidget(self.rwy_generate_btn)

        self.rwy_save_btn.clicked.connect(self.save_rwy_to_file)
        self.rwy_save_btn.setMinimumHeight(40)
        rwy_button_layout.addWidget(self.rwy_save_btn)

        rwy_main_layout.addWidget(rwy_button_group)

        # 创建输出区域
        rwy_output_group = QGroupBox("输出")
        rwy_output_group.setStyleSheet(control_group.styleSheet())
        rwy_output_layout = QVBoxLayout(rwy_output_group)
        self.rwy_output.setMinimumHeight(250)
        self.rwy_output.setStyleSheet(self.output_text.styleSheet())
        rwy_output_layout.addWidget(self.rwy_output)
        rwy_main_layout.addWidget(rwy_output_group)
        
        # 添加选项卡
        tabs.addTab(single_flight_tab, "单个航班")
        tabs.addTab(batch_flight_tab, "批量生成")
        tabs.addTab(tower_flight_tab, "塔台设置")
        tabs.addTab(app_flight_tab,"进近设置")
        tabs.addTab(rwy_tab,"跑道信息")
        
        # 状态栏
        self.statusBar().showMessage("就绪 - 模拟机文本生成器已启动")
        
    def find_route_by_dep_arr(self, dep_code, arr_code):
        try:
            df = pd.read_csv(self.route_path)
            
            if not all(col in df.columns for col in ['Dep', 'Arr', 'Route']):
                raise ValueError("CSV文件必须包含Dep, Arr和Route列")
            
            matched_routes = df[(df['Dep'] == dep_code) & (df['Arr'] == arr_code)].head(1)
            
            if not matched_routes.empty:
                return matched_routes['Route'].iloc[0], True
            else:
                dep_exists = (df['Dep'] == dep_code).any()
                arr_exists = (df['Arr'] == arr_code).any()
                
                if not dep_exists and not arr_exists:
                    QMessageBox.warning(self, "警告", f"数据库中既不存在Dep代码'{dep_code}'，也不存在Arr代码'{arr_code}'")
                elif not dep_exists:
                    QMessageBox.warning(self, "警告", f"数据库中不存在Dep代码'{dep_code}'")
                elif not arr_exists:
                    QMessageBox.warning(self, "警告", f"数据库中不存在Arr代码'{arr_code}'")
                
                return "", False
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理CSV文件时出错: {e}")
            return "", False
            
    def find_remarks_by_dep_arr(self, dep_code, arr_code):
        try:
            df = pd.read_csv(self.route_path)
            
            if not all(col in df.columns for col in ['Dep', 'Arr', 'Remarks']):
                raise ValueError("CSV文件必须包含Dep, Arr和Remarks列")
            
            matched_remarks = df[(df['Dep'] == dep_code) & (df['Arr'] == arr_code)].head(1)
            
            if not matched_remarks.empty:
                remarks = matched_remarks['Remarks'].iloc[0]
                return str(remarks) if pd.notna(remarks) else ""
            else:
                return ""
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理CSV文件时出错: {e}")
            return ""
    
    def find_pos_and_hdg_by_gate(self, adep=None, gate=None):
        """
        根据机场和登机口查找位置和航向

        Args:
            adep: 机场ICAO代码,如果为None则使用界面输入
            gate: 登机口名称,如果为None则使用界面输入

        Returns:
            tuple: (位置, 航向) 或 None(如果未找到)
        """
        # 如果参数为空，从界面获取
        if adep is None:
            adep = self.tower_dep_input.currentText().strip()
        if gate is None:
            gate = self.gate_input.text().strip()

        # 验证输入
        if not adep or not gate:
            print("错误: 机场或登机口不能为空")
            return None

        try:
            with open(self.gate_path, "r", encoding="utf-8") as f:
                gt = json.load(f)

            # 检查机场是否存在
            if adep not in gt:
                print(f"错误: 机场 {adep} 不存在于数据中")
                return None

            airport = gt[adep]

            # 检查登机口是否存在
            if gate not in airport:
                print(f"错误: 登机口 {gate} 在机场 {adep} 中不存在")
                return None

            gates = airport[gate]

            # 检查必要字段
            if "pos" not in gates or "hdg" not in gates:
                print(f"错误: 登机口 {gate} 数据不完整，缺少 pos 或 hdg 字段")
                return None

            pos = gates["pos"]
            hdg = gates["hdg"]

            return pos, hdg

        except FileNotFoundError:
            print(f"错误: 文件 {self.gate_path} 不存在")
            return None
        except json.JSONDecodeError:
            print(f"错误: 文件 {self.gate_path} 格式错误")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None
   
    # 修复后的函数：正确保存多个机位信息
    def write_pos_and_hdg_into_json(self, pos, hdg):
        """将位置和航向写入JSON文件，修复只能保存一个机位的问题"""
        adep = self.tower_dep_input.currentText().strip()
        gate = self.gate_input.text().strip()

        # 验证输入
        if not adep or not gate:
            print("错误: 机场或登机口不能为空")
            return False

        try:
            # 读取现有数据
            try:
                with open(self.gate_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except FileNotFoundError:
                # 如果文件不存在，创建空字典
                data = {}
            except json.JSONDecodeError:
                # 如果JSON格式错误，创建空字典
                print("JSON文件格式错误，将创建新文件")
                data = {}

            # 修复：构建要添加的数据
            gate_data = {
                "pos": pos,
                "hdg": hdg
            }

            # 修复：如果机场不存在，创建机场字典
            if adep not in data:
                data[adep] = {}
            
            # 修复：添加或更新机位，不覆盖其他机位
            data[adep][gate] = gate_data

            # 写回文件
            with open(self.gate_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"成功写入数据: {adep}/{gate} - 位置: {pos}, 航向: {hdg}")
            
            # 显示保存成功的消息
            QMessageBox.information(self, "保存成功", 
                                  f"已成功保存机位信息：\n机场：{adep}\n机位：{gate}\n位置：{pos}\n航向：{hdg}")
            
            return True

        except Exception as e:
            print(f"写入数据时出错: {e}")
            QMessageBox.critical(self, "保存失败", f"保存机位信息时出错：{e}")
            return False
            
    def generate_single_flight(self):
        # 获取输入值
        airline = random.choice(self.airlines)
        numbers = str(random.randint(100,9999))
        callsign = airline + numbers
        adep = self.dep_input.currentText()
        dest = self.arr_input.currentText()
        rfl = self.rfl_input.currentText()
        alti_key = self.alti_input.currentText()
        alt = self.ALTI[alti_key]
        typ = self.typ_input.text()
        ppos = self.pos_input.text()
        head = self.head_input.value()
        hdg = int(head * 2.88 * 4 + 2)
        pos = ppos.replace(",", ":")
        if self.Cruise[str(rfl)]%2==0:
            EO="SE"
        else:
            EO="SO"
        Name=str(adep)+"-"+str(dest)
        
        # 查找航路
        route, found = self.find_route_by_dep_arr(adep, dest)
        if not found:
            reply = QMessageBox.question(self, "未找到航路", 
                                        f"未找到从{adep}到{dest}的路线,是否手动输入?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                route, ok = QInputDialog.getText(self, "手动输入航路", "请输入航路:")
                with open(self.route_path,"a",encoding='utf-8') as file:
                    file.write('{},{},{},{},,,{},\n'.format(adep,dest,Name,EO,route))
                if not ok or not route:
                    return
            else:
                return
                
        remark = self.find_remarks_by_dep_arr(adep, dest)
        rte = self.rte_input.text() or route
        
        # 生成输出
        output = f"PSEUDOPILOT:ALL\n"
        output += f"@N:{callsign}:2000:1:{pos}:{alt}:0:{hdg}:0\n"
        output += f"$FP{callsign}:*A:I:{typ}:420:{adep}:0000:0000:{rfl}:{dest}:00:00:0:0::/V/PBN/A1B1C1D1L1O1S2;{remark}:{route}\n"
        output += f"$ROUTE:{rte}\n"
        output += f"DELAY:1:8\n"
        output += f"REQALT::{alt}\n"
        output += f"INITIALPSEUDOPILOT:{self.ini_input.text()}\n"
        output += f"\n"
        
        self.output_text.setPlainText(output)
        self.statusBar().showMessage("单个航班计划生成完成")
        
    def generate_batch_flights(self):
        flights = self.batch_count.value()
        ini = self.batch_ini.text()
        
        output = "PSEUDOPILOT:ALL\n\n"
        
        for i in range(flights):
            airline = random.choice(self.airlines)
            numbers = str(random.randint(100,9999))
            callsign = airline + numbers
            
            # 随机选择不同的起降机场
            adep, dest = random.sample(self.airports, 2)
            
            rfl = random.choice(list(self.Cruise.keys()))
            alti_key = random.choice(list(self.ALTI.keys()))
            alt = self.ALTI[alti_key]
            typ = "A320"  # 默认机型
            ppos = "N30.5,E120.5"  # 默认位置
            head = random.randint(0, 360)
            hdg = int(head * 2.88 * 4 + 2)
            pos = ppos.replace(",", ":")
            
            # 查找航路
            route, found = self.find_route_by_dep_arr(adep, dest)
            if not found:
                route = "DIRECT"  # 默认航路
                
            remark = self.find_remarks_by_dep_arr(adep, dest)
            
            # 生成输出
            output += f"PSEUDOPILOT:ALL\n"
            output += f"@N:{callsign}:2000:1:{pos}:{alt}:0:{hdg}:0\n"
            output += f"$FP{callsign}:*A:I:{typ}:420:{adep}:0000:0000:{rfl}:{dest}:00:00:0:0::/V/PBN/A1B1C1D1L1O1S2;{remark}:{route}\n"
            output += f"$ROUTE:{route}\n"
            output += f"DELAY:1:8\n"
            output += f"REQALT::{alt}\n"
            output += f"INITIALPSEUDOPILOT:{ini}\n"
            output += f"\n"
        
        self.batch_output.setPlainText(output)
        self.statusBar().showMessage(f"批量生成完成 - 共生成 {flights} 个航班计划")
    
    def generate_tower_flights(self):
        airline = random.choice(self.airlines)
        numbers = str(random.randint(100,9999))
        callsign = airline + numbers
        adep = self.tower_dep_input.currentText()
        dest = self.tower_arr_input.currentText()
        rfl = self.tower_rfl_input.currentText()
        alt = self.tower_alti_input.text()
        typ = self.tower_typ_input.text()
        gate = self.gate_input.text()
        result = self.find_pos_and_hdg_by_gate(adep, gate)
        if result:
                pos, hdg = result
        else:
                reply = QMessageBox.question(self, "未找到登机口数据", f"未找到{adep}的{gate}数据，是否手动输入？",
                                           QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    pos, ok = QInputDialog.getText(self, "手动输入登机口数据", "请输入经纬度:")
                    if not ok or not pos:
                        return
                    hdg, ok = QInputDialog.getInt(self, "手动输入登机口数据", "请输入头朝向:", 0, 0, 360, 1)
                    if not ok:
                        return
                    # 保存到JSON文件
                    self.write_pos_and_hdg_into_json(pos, str(hdg))
                else:
                    return
        pos = pos.replace(",", ":")
        hdg = str(int(hdg) * 2.88 * 4 + 2)
        if self.Cruise[str(rfl)]%2==0:
            EO="SE"
        else:
            EO="SO"
        Name = str(adep)+"-"+str(dest)
        
        # 查找航路
        route, found = self.find_route_by_dep_arr(adep, dest)
        if not found:
            reply = QMessageBox.question(self, "未找到航路", 
                                        f"未找到从{adep}到{dest}的路线,是否手动输入?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                route, ok = QInputDialog.getText(self, "手动输入航路", "请输入航路:")
                with open(self.route_path,"a",encoding='utf-8') as file:
                    file.write('{},{},{},{},,,{},\n'.format(adep,dest,Name,EO,route))
                if not ok or not route:
                    return
            else:
                return
        remark = self.find_remarks_by_dep_arr(adep, dest)
        rte = self.tower_rte_input.text() or route
        
        # 生成输出
        tower_output = f"PSEUDOPILOT:ALL\n"
        tower_output += f"@N:{callsign}:2000:1:{pos}:{alt}:0:{hdg}:0\n"
        tower_output += f"$FP{callsign}:*A:I:{typ}:420:{adep}:0000:0000:{rfl}:{dest}:00:00:0:0::/V/PBN/A1B1C1D1L1O1S2;{remark}:{route}\n"
        tower_output += f"$ROUTE:{rte}\n"
        tower_output += f"DELAY:1:8\n"
        tower_output += f"REQALT::{alt}\n"
        tower_output += f"INITIALPSEUDOPILOT:{self.tower_ini_input.text()}\n"
        tower_output += f"\n"
        
        self.tower_output.setPlainText(tower_output)
        self.statusBar().showMessage("塔台航班计划生成完成")
        
    def generate_app_flights(self):
        airline = random.choice(self.airlines)
        numbers = str(random.randint(100,9999))
        callsign = airline + numbers
        adep = self.app_dep_input.currentText()
        dest = self.app_arr_input.currentText()
        rfl = self.app_rfl_input.currentText()
        alti_key = self.app_alti_input.currentText()
        alt = self.ALTI[alti_key]
        typ = self.app_typ_input.text()
        pos=self.app_pos_input.text()
        pos = pos.replace(",", ":")
        hdg=self.app_head_input.text()
        hdg = str(int(hdg) * 2.88 * 4 + 2)
        start=self.app_start_input.value()
        star_input=self.app_star_input.text()
        if self.Cruise[str(rfl)]%2==0:
            EO="SE"
        else:
            EO="SO"
        Name = str(adep)+"-"+str(dest)
        route, found = self.find_route_by_dep_arr(adep, dest)
        if not found:
            reply = QMessageBox.question(self, "未找到航路", 
                                        f"未找到从{adep}到{dest}的路线,是否手动输入?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                route, ok = QInputDialog.getText(self, "手动输入航路", "请输入航路:")
                with open(self.route_path,"a",encoding='utf-8') as file:
                    file.write('{},{},{},{},,,{},\n'.format(adep,dest,Name,EO,route))
                if not ok or not route:
                    return
            else:
                return
            
        star=self.get_rte_options(star_input)
        if not star:
            reply=QMessageBox.question(self,"未找到程序航路",
                                       f"未找到{star_input}程序，是否手动输入航路?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply==QMessageBox.Yes:
                star,ok=QInputDialog.getText(self,"手动输入航路","请输入航路")
                with open(self.sid_path,"a",encoding='utf-8') as file:
                    file.write('\n,{},,{},{},'.format(adep,star_input,star))
                if not ok or not star:
                    return
            else:
                return
            
        remark = self.find_remarks_by_dep_arr(adep, dest)
        # 生成输出
        app_output = f"PSEUDOPILOT:ALL\n"
        app_output += f"@N:{callsign}:2000:1:{pos}:{alt}:0:{hdg}:0\n"
        app_output += f"$FP{callsign}:*A:I:{typ}:420:{adep}:0000:0000:{rfl}:{dest}:00:00:0:0::/V/PBN/A1B1C1D1L1O1S2;{remark}:{route}\n"
        app_output += f"$ROUTE:{star}\n"
        app_output += f"DELAY:1:8\n"
        app_output += f"REQALT::{alt}\n"
        app_output += f"START:{start}\n"
        app_output += f"INITIALPSEUDOPILOT:{self.app_ini_input.text()}\n"
        app_output += f"\n"
        
        self.app_output.setPlainText(app_output)
        self.statusBar().showMessage("进近航班计划生成完成")
    
    def generate_rwy_info(self):
        """生成跑道信息 - 使用外置模块处理坐标"""
        rwy_num = self.rwy_number_input.text()
        start_pos = self.rwy_start_input.text()
        end_pos = self.rwy_end_input.text()

        if not rwy_num:
            QMessageBox.warning(self, "警告", "请输入跑道编号！")
            return

        if not start_pos or not end_pos:
            QMessageBox.warning(self, "警告", "请输入起始和结束跑道经纬度！")
            return

        # 验证坐标格式（只支持点分隔格式）
        if not validate_coordinate_format(start_pos):
            QMessageBox.warning(self, "格式错误", 
                              "起始跑道经纬度格式错误！\n"
                              "要求格式：N031.12.37.142,E121.19.54.741\n"
                              "说明：\n"
                              "- N031.12.37.142 表示北纬31度12分37.142秒\n"
                              "- E121.19.54.741 表示东经121度19分54.741秒\n"
                              "- 使用点号分隔度、分、秒")
            return

        if not validate_coordinate_format(end_pos):
            QMessageBox.warning(self, "格式错误", 
                              "结束跑道经纬度格式错误！\n"
                              "要求格式：N031.12.37.142,E121.19.54.741\n"
                              "说明：\n"
                              "- N031.12.37.142 表示北纬31度12分37.142秒\n"
                              "- E121.19.54.741 表示东经121度19分54.741秒\n"
                              "- 使用点号分隔度、分、秒")
            return

        # 使用外置模块处理坐标
        start_pos_processed = process_position(start_pos)
        end_pos_processed = process_position(end_pos)
        
        # 生成主跑道信息
        output = f"ILS{rwy_num}:{start_pos_processed}:{end_pos_processed}\n"
        
        # 根据勾选状态决定是否生成对向跑道
        if self.rwy_opposite_checkbox.isChecked():
            rwy_num2 = convert_runway(rwy_num)
            output += f"ILS{rwy_num2}:{end_pos_processed}:{start_pos_processed}\n"
        
        self.rwy_output.setPlainText(output)
        self.statusBar().showMessage("跑道信息生成完成")
    
    def get_rte_options(self, pro_input: str) -> str:
        """
        根据PRO输入从CSV文件中获取所有包含该PRO的行对应的RTE选项的重合部分
        使用最简单的版本，手动处理CSV格式问题
        """
        try:
            rte_values = []
            
            with open(self.sid_path, 'r', encoding='utf-8') as file:
                for i, line in enumerate(file):
                    line = line.strip()
                    if not line:
                        continue
                        
                    fields = line.split(',')
                    
                    # 第一行是表头
                    if i == 0:
                        if 'PRO' in fields and 'RTE' in fields:
                            pro_index = fields.index('PRO')
                            rte_index = fields.index('RTE')
                        else:
                            return ""
                        continue
                    
                    # 数据行：只取前5个字段，忽略多余的
                    if len(fields) >= 5:
                        pro_value = fields[pro_index] if pro_index < len(fields) else ""
                        rte_value = fields[rte_index] if rte_index < len(fields) else ""
                        
                        # 检查PRO是否包含输入值且RTE不为空
                        if pro_input in pro_value and rte_value and rte_value.strip():
                            rte_values.append(rte_value.strip())
            
            if not rte_values:
                return ""
            
            # 计算所有RTE值的交集（共同部分）
            # 这里我们找出所有匹配行中都出现的RTE值
            from collections import Counter
            rte_counter = Counter(rte_values)
            
            # 获取出现次数等于总匹配行数的RTE值（即所有行都有的共同值）
            total_matches = len(rte_values)
            common_rte = [rte for rte, count in rte_counter.items() if count == total_matches]
            
            # 如果没有完全相同的共同值，返回所有去重后的值
            if not common_rte:
                # 或者可以返回出现次数最多的值
                # common_rte = [rte_counter.most_common(1)[0][0]] if rte_counter else []
                
                # 或者返回所有去重值
                common_rte = list(set(rte_values))
            
            return ','.join(common_rte) if common_rte else ""
            
        except Exception as e:
            print(f"读取文件出错: {e}")
            return ""
        
    def save_single_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(self.output_text.toPlainText())
                QMessageBox.information(self, "成功", "文件已保存")
                self.statusBar().showMessage(f"文件已保存至: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件时出错: {e}")
                self.statusBar().showMessage("文件保存失败")
                
    def save_tower_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(self.tower_output.toPlainText())
                QMessageBox.information(self, "成功", "文件已保存")
                self.statusBar().showMessage(f"文件已保存至: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件时出错: {e}")
                self.statusBar().showMessage("文件保存失败")
                
    def save_app_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(self.app_output.toPlainText())
                QMessageBox.information(self, "成功", "文件已保存")
                self.statusBar().showMessage(f"文件已保存至: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件时出错: {e}")
                self.statusBar().showMessage("文件保存失败")
                
    def save_rwy_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(self.rwy_output.toPlainText())
                QMessageBox.information(self, "成功", "文件已保存")
                self.statusBar().showMessage(f"文件已保存至: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件时出错: {e}")
                self.statusBar().showMessage("文件保存失败")
    
    def apply_theme(self, theme_name):
        """应用不同主题样式"""
        self.current_theme = theme_name
        
        if theme_name == "light":
            style_sheet = """
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #cccccc;
                    border-radius: 8px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #2c3e50;
                }
                QPushButton {
                    background-color: #3498db;
                    border: none;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
                QLineEdit, QComboBox, QSpinBox, QTextEdit {
                    padding: 6px;
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                    background-color: white;
                }
                QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                    border-color: #3498db;
                }
                QTextEdit {
                    font-family: 'Courier New', monospace;
                }
            """
        elif theme_name == "dark":
            style_sheet = """
                QMainWindow {
                    background-color: #2c3e50;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #34495e;
                    border-radius: 8px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: #34495e;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #ecf0f1;
                }
                QPushButton {
                    background-color: #1abc9c;
                    border: none;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #16a085;
                }
                QPushButton:pressed {
                    background-color: #1e824c;
                }
                QLineEdit, QComboBox, QSpinBox, QTextEdit {
                    padding: 6px;
                    border: 1px solid #7f8c8d;
                    border-radius: 4px;
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    selection-background-color: #1abc9c;
                }
                QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                    border-color: #1abc9c;
                }
                QLabel {
                    color: #ecf0f1;
                }
                QTextEdit {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 1px solid #7f8c8d;
                    font-family: 'Courier New', monospace;
                }
                QTabBar::tab {
                    background-color: #34495e;
                    color: #ecf0f1;
                }
                QTabBar::tab:selected {
                    background-color: #1abc9c;
                }
            """
        elif theme_name == "blue":
            style_sheet = """
                QMainWindow {
                    background-color: #ecf0f1;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #3498db;
                    border-radius: 8px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #2980b9;
                }
                QPushButton {
                    background-color: #2980b9;
                    border: none;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #1f639b;
                }
                QPushButton:pressed {
                    background-color: #154b75;
                }
                QLineEdit, QComboBox, QSpinBox, QTextEdit {
                    padding: 6px;
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                    background-color: white;
                }
                QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                    border-color: #2980b9;
                }
                QTextEdit {
                    font-family: 'Courier New', monospace;
                }
            """
        
        # 更新按钮样式以反映当前主题
        self.style_light_btn.setStyleSheet("")
        self.style_dark_btn.setStyleSheet("")
        self.style_blue_btn.setStyleSheet("")
        
        if theme_name == "light":
            self.style_light_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        elif theme_name == "dark":
            self.style_dark_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        elif theme_name == "blue":
            self.style_blue_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        
        self.setStyleSheet(style_sheet)
        
    def toggle_topmost(self, checked):
        """切换窗口置顶状态"""
        if checked:
            # 开启置顶
            self.setWindowFlags(self.windowFlags()|Qt.WindowStaysOnTopHint)
            self.topmost_button.setText("取消置顶")
            self.topmost_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    border: none;
                    color: white;
                    padding: 5px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
        else:
            # 关闭置顶
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.topmost_button.setText("置顶")
            self.topmost_button.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    border: none;
                    color: white;
                    padding: 5px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)

        # 重新显示窗口以使设置生效
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 设置应用字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    window = FlightPlanGenerator()
    window.show()
    sys.exit(app.exec_())