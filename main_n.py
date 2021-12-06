from PyQt5 import QtCore, QtGui, QtWidgets
import os
import xml.etree.ElementTree as ET
import csv
from bin import parsefun as pf

class TemplateInfo():
    def __init__(self, name):
        import xml.etree.ElementTree as ET
        
        self.name = name        # Название шаблона
        self.urls = []          # Список Url на целевые страницы
        self.names = []         # Перечень сущностей для выходной таблицы
        self.list_name = ""     # Строка, содержит имя списка карточек товара и имя карточки товара (необходимо для итерации)
        self.selectors = []     # Перечень блоков, содержащих необходимую информацию
        self.types = []         # Перечень типов необходимой информации
        self.pg_iterator = ""   # В разработке # Способ итерации страниц

        tree = ET.parse("templates/" + name)
        root = tree.getroot()

        for top in root:
            if top.tag == "WebList":
                self.list_name = "." + top.attrib.get("list_name") + " > " + "." + top.attrib.get("item_name")
                self.pg_iterator = top.attrib.get("page_iterator")
            elif top.tag == "CSSSelectors":
                for item in top:
                    self.names.append(item.attrib.get("name"))
                    self.selectors.append("." + item.text)
                    self.types.append(item.attrib.get("type"))
            elif top.tag == "DataURL":
                for url in top:
                    self.urls.append(url.text)
    
    def is_ok(self):
        if len(self.names) == len(self.selectors) == len(self.types) and len(self.list_name) > 0 and len(self.urls) > 0:
            return True
        else:
            return False


class Ui_CreateSessionWidget(object):
    def setupUi(self, CreateSessionWidget):
        CreateSessionWidget.setObjectName("CreateSessionWidget")
        CreateSessionWidget.resize(552, 387)
        self.add_button = QtWidgets.QPushButton(CreateSessionWidget)
        self.add_button.setGeometry(QtCore.QRect(250, 190, 51, 31))
        self.add_button.setObjectName("add_button")
        self.del_button = QtWidgets.QPushButton(CreateSessionWidget)
        self.del_button.setGeometry(QtCore.QRect(250, 240, 51, 31))
        self.del_button.setObjectName("del_button")
        self.session_name_edit = QtWidgets.QLineEdit(CreateSessionWidget)
        self.session_name_edit.setGeometry(QtCore.QRect(10, 30, 351, 20))
        self.session_name_edit.setObjectName("session_name_edit")
        self.create_session_button = QtWidgets.QPushButton(CreateSessionWidget)
        self.create_session_button.setGeometry(QtCore.QRect(370, 30, 75, 23))
        self.create_session_button.setObjectName("create_session_button")
        self.cancel_button = QtWidgets.QPushButton(CreateSessionWidget)
        self.cancel_button.setGeometry(QtCore.QRect(460, 30, 75, 23))
        self.cancel_button.setObjectName("cancel_button")
        self.label = QtWidgets.QLabel(CreateSessionWidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(CreateSessionWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(CreateSessionWidget)
        self.label_3.setGeometry(QtCore.QRect(320, 80, 111, 16))
        self.label_3.setObjectName("label_3")
        self.parsing_queue_list = QtWidgets.QListWidget(CreateSessionWidget)
        self.parsing_queue_list.setGeometry(QtCore.QRect(10, 110, 231, 261))
        self.parsing_queue_list.setObjectName("parsing_queue_list")
        self.parsing_templates_list = QtWidgets.QListWidget(CreateSessionWidget)
        self.parsing_templates_list.setGeometry(QtCore.QRect(310, 110, 231, 261))
        self.parsing_templates_list.setObjectName("parsing_templates_list")

        qList = os.listdir(os.getcwd() + "/templates")
        for i in range(len(qList)):
            qList[i] = qList[i].replace(".xml", "")
        self.parsing_templates_list.addItems(qList)

        self.add_funcs()

        

        self.retranslateUi(CreateSessionWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateSessionWidget)

    def retranslateUi(self, CreateSessionWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateSessionWidget.setWindowTitle(_translate("CreateSessionWidget", "Form"))
        self.add_button.setText(_translate("CreateSessionWidget", "ADD"))
        self.del_button.setText(_translate("CreateSessionWidget", "DEL"))
        self.create_session_button.setText(_translate("CreateSessionWidget", "Create"))
        self.cancel_button.setText(_translate("CreateSessionWidget", "Clear"))
        self.label.setText(_translate("CreateSessionWidget", "Session name:"))
        self.label_2.setText(_translate("CreateSessionWidget", "Parsing queue:"))
        self.label_3.setText(_translate("CreateSessionWidget", "Parsing templates list:"))

    def add_funcs(self):
        self.create_session_button.clicked.connect(lambda: self.create_xml_template())
        self.add_button.clicked.connect(lambda: self.add_template())
        self.del_button.clicked.connect(lambda: self.del_template())
        self.cancel_button.clicked.connect(lambda: self.clear_all())

    def create_xml_template(self):
        tmp_name = self.session_name_edit.text()
        data = ET.Element('data')
        parsing_templates = ET.SubElement(data, 'parsing_templates')

        item_list =  list(self.parsing_queue_list.item(i).data(0) + ".xml" for i in range(self.parsing_queue_list.count()) )
        insert_item_list = list()

        for i in range(len(item_list)):
            insert_item_list.append(ET.SubElement(parsing_templates, 'item'))
            insert_item_list[i].text = item_list[i]

        mydata = ET.tostring(data, 'utf-8')

        tmp_session_list = os.listdir(os.getcwd() + "/session templates")
        file_checker = False

        if not len(tmp_session_list):
            myfile = open("session templates/" + tmp_name + ".xml", "wb")
            myfile.write(mydata)
            self.msg_info("Successfully created!").exec_()
        else:
            for item in tmp_session_list:
                if item == (tmp_name + ".xml"):
                    self.msg_info("Template with this name exist!").exec_()
                    file_checker = True
                    break
            if not file_checker:
                myfile = open("session templates/" + tmp_name + ".xml", "wb")
                myfile.write(mydata)
                self.msg_info("Successfully created!").exec_()
        

    def add_template(self):
        self.parsing_queue_list.addItem(self.parsing_templates_list.currentItem().data(0))

    def del_template(self):
        self.parsing_queue_list.takeItem(self.parsing_queue_list.currentRow())

    def clear_all(self):
        while(self.parsing_queue_list.takeItem(0)):
            pass
        self.session_name_edit.clear()
        
    def msg_info(self, info_str):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox().Information)
        msg.setText("[INFO]")
        msg.setInformativeText(info_str)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QtWidgets.QMessageBox().Ok)
        return msg


class Ui_CreateParseTemplateWidget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(948, 469)
        Widget.setStyleSheet("")
        self.gridLayoutWidget = QtWidgets.QWidget(Widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 931, 451))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.str_name_edit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.str_name_edit_3.setObjectName("str_name_edit_3")
        self.gridLayout.addWidget(self.str_name_edit_3, 10, 2, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 0, 0, 15, 1)
        self.parse_type_3 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.parse_type_3.setObjectName("parse_type_3")
        self.parse_type_3.addItem("")
        self.parse_type_3.addItem("")
        self.parse_type_3.addItem("")
        self.gridLayout.addWidget(self.parse_type_3, 10, 8, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 8, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 2, 1, 1)
        self.CSS_sel_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.CSS_sel_3.setObjectName("CSS_sel_3")
        self.gridLayout.addWidget(self.CSS_sel_3, 10, 4, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 0, 10, 15, 1)
        self.line_8 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 1, 7, 1, 1)
        self.urls_edit = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.urls_edit.setObjectName("urls_edit")
        self.gridLayout.addWidget(self.urls_edit, 14, 2, 1, 5)
        self.str_name_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.str_name_2.setObjectName("str_name_2")
        self.gridLayout.addWidget(self.str_name_2, 8, 1, 1, 1)
        self.parse_type_1 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.parse_type_1.setEditable(False)
        self.parse_type_1.setObjectName("parse_type_1")
        self.parse_type_1.addItem("")
        self.parse_type_1.addItem("")
        self.parse_type_1.addItem("")
        self.gridLayout.addWidget(self.parse_type_1, 6, 8, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 4, 1, 1)
        self.createButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.createButton.setObjectName("createButton")
        self.gridLayout.addWidget(self.createButton, 14, 8, 1, 1)
        self.str_name_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.str_name_4.setObjectName("str_name_4")
        self.gridLayout.addWidget(self.str_name_4, 12, 1, 1, 1)
        self.cssedit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.cssedit_3.setObjectName("cssedit_3")
        self.gridLayout.addWidget(self.cssedit_3, 10, 5, 1, 2)
        self.template_name_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.template_name_edit.setObjectName("template_name_edit")
        self.gridLayout.addWidget(self.template_name_edit, 1, 2, 1, 5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 11, 2, 1, 1)
        self.template_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.template_name.setObjectName("template_name")
        self.gridLayout.addWidget(self.template_name, 1, 1, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 4, 7, 9, 1)
        self.cssedit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.cssedit_2.setObjectName("cssedit_2")
        self.gridLayout.addWidget(self.cssedit_2, 8, 5, 1, 2)
        self.cssedit_1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.cssedit_1.setObjectName("cssedit_1")
        self.gridLayout.addWidget(self.cssedit_1, 6, 5, 1, 2)
        self.parse_type_4 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.parse_type_4.setObjectName("parse_type_4")
        self.parse_type_4.addItem("")
        self.parse_type_4.addItem("")
        self.parse_type_4.addItem("")
        self.gridLayout.addWidget(self.parse_type_4, 12, 8, 1, 1)
        self.line = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 1, 1, 9)
        self.CSS_sel_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.CSS_sel_2.setObjectName("CSS_sel_2")
        self.gridLayout.addWidget(self.CSS_sel_2, 8, 4, 1, 1)
        self.CSS_sel_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.CSS_sel_4.setObjectName("CSS_sel_4")
        self.gridLayout.addWidget(self.CSS_sel_4, 12, 4, 1, 1)
        self.parse_type_2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.parse_type_2.setObjectName("parse_type_2")
        self.parse_type_2.addItem("")
        self.parse_type_2.addItem("")
        self.parse_type_2.addItem("")
        self.gridLayout.addWidget(self.parse_type_2, 8, 8, 1, 1)
        self.CSS_sel_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.CSS_sel_1.setObjectName("CSS_sel_1")
        self.gridLayout.addWidget(self.CSS_sel_1, 6, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 2, 1, 1)
        self.str_name_edit_1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.str_name_edit_1.setObjectName("str_name_edit_1")
        self.gridLayout.addWidget(self.str_name_edit_1, 6, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)
        self.str_name_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.str_name_3.setObjectName("str_name_3")
        self.gridLayout.addWidget(self.str_name_3, 10, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 4, 3, 9, 1)
        self.URLs = QtWidgets.QLabel(self.gridLayoutWidget)
        self.URLs.setObjectName("URLs")
        self.gridLayout.addWidget(self.URLs, 14, 1, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout.addWidget(self.line_5, 0, 1, 1, 9)
        self.web_item_name_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.web_item_name_edit.setObjectName("web_item_name_edit")
        self.gridLayout.addWidget(self.web_item_name_edit, 4, 5, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 9, 2, 1, 1)
        self.cssedit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.cssedit_4.setObjectName("cssedit_4")
        self.gridLayout.addWidget(self.cssedit_4, 12, 5, 1, 2)
        self.str_name_edit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.str_name_edit_2.setObjectName("str_name_edit_2")
        self.gridLayout.addWidget(self.str_name_edit_2, 8, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 13, 1, 1, 9)
        self.str_name_edit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.str_name_edit_4.setObjectName("str_name_edit_4")
        self.gridLayout.addWidget(self.str_name_edit_4, 12, 2, 1, 1)
        self.str_name_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.str_name_1.setObjectName("str_name_1")
        self.gridLayout.addWidget(self.str_name_1, 6, 1, 1, 1)
        self.web_list_name_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.web_list_name_edit.setObjectName("web_list_name_edit")
        self.gridLayout.addWidget(self.web_list_name_edit, 4, 2, 1, 1)

        self.retranslateUi(Widget)
        self.parse_type_1.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Widget)

        self.add_funcs()

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Form"))
        self.parse_type_3.setItemText(0, _translate("Widget", "Text"))
        self.parse_type_3.setItemText(1, _translate("Widget", "Number"))
        self.parse_type_3.setItemText(2, _translate("Widget", "URL"))
        self.label.setText(_translate("Widget", "Output type"))
        self.CSS_sel_3.setText(_translate("Widget", "CSS selector"))
        self.str_name_2.setText(_translate("Widget", "Output name"))
        self.parse_type_1.setCurrentText(_translate("Widget", "Text"))
        self.parse_type_1.setItemText(0, _translate("Widget", "Text"))
        self.parse_type_1.setItemText(1, _translate("Widget", "Number"))
        self.parse_type_1.setItemText(2, _translate("Widget", "URL"))
        self.label_3.setText(_translate("Widget", "Web item name:"))
        self.createButton.setText(_translate("Widget", "Save"))
        self.str_name_4.setText(_translate("Widget", "Output name"))
        self.template_name.setText(_translate("Widget", "Template name"))
        self.parse_type_4.setItemText(0, _translate("Widget", "Text"))
        self.parse_type_4.setItemText(1, _translate("Widget", "Number"))
        self.parse_type_4.setItemText(2, _translate("Widget", "URL"))
        self.CSS_sel_2.setText(_translate("Widget", "CSS selector"))
        self.CSS_sel_4.setText(_translate("Widget", "CSS selector"))
        self.parse_type_2.setItemText(0, _translate("Widget", "Text"))
        self.parse_type_2.setItemText(1, _translate("Widget", "Number"))
        self.parse_type_2.setItemText(2, _translate("Widget", "URL"))
        self.CSS_sel_1.setText(_translate("Widget", "CSS selector"))
        self.label_2.setText(_translate("Widget", "Web list name:"))
        self.str_name_3.setText(_translate("Widget", "Output name"))
        self.URLs.setText(_translate("Widget", "URL list"))
        self.str_name_1.setText(_translate("Widget", "Output name"))

    def add_funcs(self):
        self.createButton.clicked.connect(lambda: self.create_xml_template(self))

    def create_xml_template(self):
        tmp_name = self.template_name_edit.text()

        urls = self.urls_edit.toPlainText().split('\n')

        data = ET.Element('data')
        web_list_info = ET.SubElement(data, 'WebList')
        css_sels = ET.SubElement(data, 'CSSSelectors')
        data_urls = ET.SubElement(data, 'DataURL')

        item1 = ET.SubElement(css_sels, 'item')
        item2 = ET.SubElement(css_sels, 'item')
        item3 = ET.SubElement(css_sels, 'item')
        item4 = ET.SubElement(css_sels, 'item')

        durl = list()

        for i in range(len(urls)):
            durl.append(ET.SubElement(data_urls, 'item'))
            durl[i].text = urls[i]

        item1.text = self.cssedit_1.text()
        item2.text = self.cssedit_2.text()
        item3.text = self.cssedit_3.text()
        item4.text = self.cssedit_4.text()

        web_list_info.set("list_name", self.web_list_name_edit.text()) 
        web_list_info.set("item_name", self.web_item_name_edit.text())

        item1.set("name", self.str_name_edit_1.text())
        item2.set("name", self.str_name_edit_2.text())
        item3.set("name", self.str_name_edit_3.text())
        item4.set("name", self.str_name_edit_4.text())

        item1.set("type", self.parse_type_1.currentText())
        item2.set("type", self.parse_type_2.currentText())
        item3.set("type", self.parse_type_3.currentText())
        item4.set("type", self.parse_type_4.currentText())

        tmp_parsing_list = os.listdir(os.getcwd() + "/templates")
        mydata = ET.tostring(data, 'utf-8')
        file_checker = False

        if not len(tmp_parsing_list):
            myfile = open("templates/" + tmp_name + ".xml", "wb")
            myfile.write(mydata)
            self.msg_info("Successfully created!").exec_()
        else:
            for item in tmp_parsing_list:
                if item == (tmp_name + ".xml"):
                    self.msg_info("Template with this name exist!").exec_()
                    file_checker = True
                    break
            if not file_checker:
                myfile = open("templates/" + tmp_name + ".xml", "wb")
                myfile.write(mydata)
                self.msg_info("Successfully created!").exec_()

    def msg_info(info_str):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox().Information)
        msg.setText("[INFO]")
        msg.setInformativeText(info_str)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QtWidgets.QMessageBox().Ok)
        return msg


class Ui_ParserWidget(object):
    def setupUi(self, Parser):
        Parser.setObjectName("Parser")
        Parser.resize(303, 431)
        self.templatesList = QtWidgets.QListWidget(Parser)
        self.templatesList.setGeometry(QtCore.QRect(10, 70, 281, 321))
        self.templatesList.setObjectName("templatesList")    
        self.label = QtWidgets.QLabel(Parser)   
        self.label.setGeometry(QtCore.QRect(10, 40, 281, 20))
        self.label.setText("")
        self.label.setObjectName("label")
        self.searchEdit = QtWidgets.QLineEdit(Parser)
        self.searchEdit.setGeometry(QtCore.QRect(10, 10, 201, 20))
        self.searchEdit.setObjectName("searchEdit")
        self.search_button = QtWidgets.QPushButton(Parser)
        self.search_button.setGeometry(QtCore.QRect(220, 10, 75, 23))
        self.search_button.setObjectName("search_button")
        self.parse_button = QtWidgets.QPushButton(Parser)
        self.parse_button.setGeometry(QtCore.QRect(220, 400, 75, 23))
        self.parse_button.setObjectName("parse_button")
        self.progressBar = QtWidgets.QProgressBar(Parser)
        self.progressBar.setGeometry(QtCore.QRect(10, 40, 281, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setHidden(True)

        pList = os.listdir(os.getcwd() + "/templates")
        pList += os.listdir(os.getcwd() + "/session templates")
        for i in range(len(pList)):
            pList[i] = pList[i].replace(".xml", "")
        self.templatesList.addItems(pList)

        self.add_funcs()
        self.retranslateUi(Parser)
        QtCore.QMetaObject.connectSlotsByName(Parser)

    def retranslateUi(self, Parser):
        _translate = QtCore.QCoreApplication.translate
        Parser.setWindowTitle(_translate("Parser", "Form"))
        self.search_button.setText(_translate("Parser", "Search"))
        self.parse_button.setText(_translate("Parser", "Parse"))
    
    def add_funcs(self):
        self.parse_button.clicked.connect(lambda: self.start_parsing(self.templatesList.currentItem().data(0)))

    def msg_info(info_str):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox().Information)
        msg.setText("[INFO]")
        msg.setInformativeText(info_str)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QtWidgets.QMessageBox().Ok)
        return msg

    def start_parsing(self, to_parse):
        if os.path.exists("session templates/" + to_parse + ".xml"):
            tree = ET.parse("session templates/" + to_parse + ".xml")
            iList = list()
            root = tree.getroot()
            for top in root:
                if top.tag == "parsing_templates":
                    for item in top:
                        iList.append(item.text)
                    print(iList)
            for pars in iList:
                p = TemplateInfo(pars)
                self.label.setText("Processing...")
                pf.parse(p.urls, p.names, p.list_name, p.selectors, p.types, p.name, p.pg_iterator)
                self.label.setText("Success!")
        elif os.path.exists("templates/" + to_parse + ".xml"):
            tree = ET.parse("templates/" + to_parse + ".xml")
            p = TemplateInfo(to_parse + ".xml")
            self.label.setText("Processing...")
            pf.parse(p.urls, p.names, p.list_name, p.selectors, p.types, p.name, p.pg_iterator)
            self.label.setText("Success!")
        else:
            self.msg_info("Can't find files!")


class Ui_MatchWidget(object):
    def setupUi(self, Match):
        Match.setObjectName("Match")
        Match.resize(491, 455)
        self.data_view = QtWidgets.QListView(Match)
        self.data_view.setGeometry(QtCore.QRect(10, 80, 191, 321))
        self.data_view.setObjectName("data_view")
        self.match_view = QtWidgets.QListView(Match)
        self.match_view.setGeometry(QtCore.QRect(290, 80, 191, 321))
        self.match_view.setObjectName("match_view")
        self.label = QtWidgets.QLabel(Match)
        self.label.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Match)
        self.label_2.setGeometry(QtCore.QRect(290, 60, 61, 16))
        self.label_2.setObjectName("label_2")
        self.search_edit = QtWidgets.QLineEdit(Match)
        self.search_edit.setGeometry(QtCore.QRect(10, 10, 191, 20))
        self.search_edit.setObjectName("search_edit")
        self.search_button = QtWidgets.QPushButton(Match)
        self.search_button.setGeometry(QtCore.QRect(130, 40, 75, 23))
        self.search_button.setObjectName("search_button")
        self.add_button = QtWidgets.QPushButton(Match)
        self.add_button.setGeometry(QtCore.QRect(220, 190, 51, 31))
        self.add_button.setObjectName("add_button")
        self.del_button = QtWidgets.QPushButton(Match)
        self.del_button.setGeometry(QtCore.QRect(220, 230, 51, 31))
        self.del_button.setObjectName("del_button")
        self.match_button = QtWidgets.QPushButton(Match)
        self.match_button.setGeometry(QtCore.QRect(400, 40, 75, 23))
        self.match_button.setObjectName("match_button")
        self.progressBar = QtWidgets.QProgressBar(Match)
        self.progressBar.setGeometry(QtCore.QRect(10, 420, 471, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Match)
        QtCore.QMetaObject.connectSlotsByName(Match)

    def retranslateUi(self, Match):
        _translate = QtCore.QCoreApplication.translate
        Match.setWindowTitle(_translate("Match", "Form"))
        self.label.setText(_translate("Match", "Data Tables:"))
        self.label_2.setText(_translate("Match", "To match:"))
        self.search_button.setText(_translate("Match", "Search"))
        self.add_button.setText(_translate("Match", "ADD"))
        self.del_button.setText(_translate("Match", "DEL"))
        self.match_button.setText(_translate("Match", "Match"))


class Ui_MatchReportWidget(object):
    def setupUi(self, MatchReport):
        MatchReport.setObjectName("MatchReport")
        MatchReport.resize(775, 470)
        self.match_view = QtWidgets.QListWidget(MatchReport)
        self.match_view.setGeometry(QtCore.QRect(10, 90, 191, 361))
        self.match_view.setObjectName("match_view")
        self.search_edit = QtWidgets.QLineEdit(MatchReport)
        self.search_edit.setGeometry(QtCore.QRect(10, 10, 191, 20))
        self.search_edit.setObjectName("search_edit")
        self.search_button = QtWidgets.QPushButton(MatchReport)
        self.search_button.setGeometry(QtCore.QRect(130, 40, 75, 23))
        self.search_button.setObjectName("search_button")
        self.label = QtWidgets.QLabel(MatchReport)
        self.label.setGeometry(QtCore.QRect(10, 70, 81, 16))
        self.label.setObjectName("label")
        self.match_table = QtWidgets.QTableView(MatchReport)
        self.match_table.setGeometry(QtCore.QRect(230, 10, 531, 411))
        self.match_table.setObjectName("match_table")
        self.label_2 = QtWidgets.QLabel(MatchReport)
        self.label_2.setGeometry(QtCore.QRect(240, 440, 47, 13))
        self.label_2.setObjectName("label_2")
        self.records_label = QtWidgets.QLabel(MatchReport)
        self.records_label.setGeometry(QtCore.QRect(290, 440, 91, 16))
        self.records_label.setText("")
        self.records_label.setObjectName("records_label")
        self.report_button = QtWidgets.QPushButton(MatchReport)
        self.report_button.setGeometry(QtCore.QRect(690, 430, 75, 23))
        self.report_button.setObjectName("report_button")
        self.label_3 = QtWidgets.QLabel(MatchReport)
        self.label_3.setGeometry(QtCore.QRect(590, 430, 91, 16))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(MatchReport)
        QtCore.QMetaObject.connectSlotsByName(MatchReport)

    def retranslateUi(self, MatchReport):
        _translate = QtCore.QCoreApplication.translate
        MatchReport.setWindowTitle(_translate("MatchReport", "Form"))
        self.search_button.setText(_translate("MatchReport", "Search"))
        self.label.setText(_translate("MatchReport", "Matching tables:"))
        self.label_2.setText(_translate("MatchReport", "Records:"))
        self.report_button.setText(_translate("MatchReport", "Report"))
        self.label_3.setText(_translate("MatchReport", "To get full report"))


class Ui_ParseReportWidget(object):
    def setupUi(self, ParseReport):
        ParseReport.setObjectName("ParseReport")
        ParseReport.resize(700, 464)
        self.parse_list = QtWidgets.QListWidget(ParseReport)
        self.parse_list.setGeometry(QtCore.QRect(10, 70, 191, 381))
        self.parse_list.setObjectName("parse_list")
        self.search_edit = QtWidgets.QLineEdit(ParseReport)
        self.search_edit.setGeometry(QtCore.QRect(10, 10, 191, 20))
        self.search_edit.setObjectName("search_edit")
        self.search_button = QtWidgets.QPushButton(ParseReport)
        self.search_button.setGeometry(QtCore.QRect(120, 40, 75, 23))
        self.search_button.setObjectName("search_button")
        self.parse_table = QtWidgets.QTableView(ParseReport)
        self.parse_table.setGeometry(QtCore.QRect(220, 10, 471, 411))
        self.parse_table.setObjectName("parse_table")
        self.label = QtWidgets.QLabel(ParseReport)
        self.label.setGeometry(QtCore.QRect(220, 430, 51, 16))
        self.label.setObjectName("label")
        self.records_label = QtWidgets.QLabel(ParseReport)
        self.records_label.setGeometry(QtCore.QRect(270, 430, 71, 16))
        self.records_label.setText("")
        self.records_label.setObjectName("records_label")
        self.label_2 = QtWidgets.QLabel(ParseReport)
        self.label_2.setGeometry(QtCore.QRect(520, 430, 91, 16))
        self.label_2.setObjectName("label_2")
        self.report_button = QtWidgets.QPushButton(ParseReport)
        self.report_button.setGeometry(QtCore.QRect(610, 430, 75, 23))
        self.report_button.setObjectName("report_button")
        self.model = QtGui.QStandardItemModel()

        pList = os.listdir(os.getcwd() + "/parsing results")
        for i in range(len(pList)):
            pList[i] = pList[i].replace(".xml", "")
        self.parse_list.addItems(pList)

        if self.parse_list.currentIndex().data(0):
            with open("/parsing results/" + str(self.parse_list.currentIndex().data(0)), "r") as fileInput:
                for row in csv.reader(fileInput):    
                    items = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.model.appendRow(items)
            self.parse_table.setModel(self.model)

        self.add_funcs()
        self.retranslateUi(ParseReport)
        QtCore.QMetaObject.connectSlotsByName(ParseReport)

    def retranslateUi(self, ParseReport):
        _translate = QtCore.QCoreApplication.translate
        ParseReport.setWindowTitle(_translate("ParseReport", "Form"))
        self.search_button.setText(_translate("ParseReport", "Search"))
        self.label.setText(_translate("ParseReport", "Records:"))
        self.label_2.setText(_translate("ParseReport", "To get full report"))
        self.report_button.setText(_translate("ParseReport", "Report"))

    def add_funcs(self):
        self.parse_list.clicked.connect(lambda: self.fill_report())

    def fill_report(self):
        if self.parse_list.currentIndex().data(0):
            try:
                fileInput = open('parsing results/' + str(self.parse_list.currentIndex().data(0)), "r", encoding = "utf-8")
                for row in csv.reader(fileInput):    
                    items = [
                        QtGui.QStandardItem(field) for field in row
                    ]
                    self.model.appendRow(items)
            except UnicodeDecodeError as err:
                fileInput.seek(err.object[err.end] + 1)
                print(err.object[err.end])
                for row in csv.reader(fileInput):    
                    items = [
                        QtGui.QStandardItem(field) for field in row
                    ]
                    self.model.appendRow(items)

            self.parse_table.setModel(self.model)


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1100, 500)
        self.button_1 = QtWidgets.QPushButton(Widget)
        self.button_1.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.button_1.setObjectName("button_1")
        self.button_2 = QtWidgets.QPushButton(Widget)
        self.button_2.setGeometry(QtCore.QRect(10, 40, 91, 31))
        self.button_2.setObjectName("button_2")
        self.button_3 = QtWidgets.QPushButton(Widget)
        self.button_3.setGeometry(QtCore.QRect(10, 100, 91, 31))
        self.button_3.setObjectName("button_3")
        self.button_4 = QtWidgets.QPushButton(Widget)
        self.button_4.setGeometry(QtCore.QRect(10, 70, 91, 31))
        self.button_4.setObjectName("button_4")
        self.button_5 = QtWidgets.QPushButton(Widget)
        self.button_5.setGeometry(QtCore.QRect(10, 130, 91, 31))
        self.button_5.setObjectName("button_5")
        self.button_6 = QtWidgets.QPushButton(Widget)
        self.button_6.setGeometry(QtCore.QRect(10, 160, 91, 31))
        self.button_6.setObjectName("button_6")
        self.stackedWidget = QtWidgets.QStackedWidget(Widget)
        self.stackedWidget.setGeometry(QtCore.QRect(100, 10, 1000, 500))
        self.stackedWidget.setObjectName("stackedWidget")

        csw = QtWidgets.QWidget()
        ui_csw = Ui_CreateSessionWidget()
        ui_csw.setupUi(csw)
        self.page_1 = csw
        self.stackedWidget.addWidget(self.page_1)

        cptw = QtWidgets.QWidget()
        ui_cptw = Ui_CreateParseTemplateWidget()
        ui_cptw.setupUi(cptw)
        self.page_2 = cptw
        self.stackedWidget.addWidget(self.page_2)

        pw = QtWidgets.QWidget()
        ui_pw = Ui_ParserWidget()
        ui_pw.setupUi(pw)
        self.page_3 = pw
        self.stackedWidget.addWidget(self.page_3)

        match = QtWidgets.QWidget()
        ui_match = Ui_MatchWidget()
        ui_match.setupUi(match)
        self.page_4 = match
        self.stackedWidget.addWidget(self.page_4)

        match_report = QtWidgets.QWidget()
        ui_match_report = Ui_MatchReportWidget()
        ui_match_report.setupUi(match_report)
        self.page_5 = match_report
        self.stackedWidget.addWidget(self.page_5)

        parse_report = QtWidgets.QWidget()
        ui_parse_report = Ui_ParseReportWidget()
        ui_parse_report.setupUi(parse_report)
        self.page_6 = parse_report
        self.stackedWidget.addWidget(self.page_6)


        self.add_funcs()
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Form"))
        self.button_1.setText(_translate("Widget", "Session template"))
        self.button_2.setText(_translate("Widget", "Parse Template"))
        self.button_3.setText(_translate("Widget", "Start parsing"))
        self.button_4.setText(_translate("Widget", "Matching"))
        self.button_5.setText(_translate("Widget", "Matching Report"))
        self.button_6.setText(_translate("Widget", "Parsing Report"))

    def add_funcs(self):
        self.button_1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.button_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.button_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.button_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.button_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.button_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())