import sys
import sqlite3
from PyQt5.QtWidgets import ( QApplication, QWidget, QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QListWidget, QMessageBox,
QTabWidget, QTableWidget, QTableWidgetItem, QAbstractItemView,QSizePolicy, QHeaderView,QComboBox)

# Giriş Ekranı 
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")
        self.setGeometry(150, 150, 350, 250)

        layout = QVBoxLayout()

        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Şifreyi gizli göster
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Sabit giriş bilgileri
        if username == "zeynep" and password == "12345":
            self.main_window = KafeSiparisApp()  # Ana uygulamayı aç
            self.main_window.show()
            self.close()  # Giriş ekranını kapat
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

class KitchenWindow(QWidget):
    def __init__(self, order_table):
        super().__init__()
        self.setWindowTitle("Mutfak Ekranı")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.order_table = QTableWidget()
        self.order_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(["Masa No", "Tatlılar", "Sıcak İçecekler", "Soğuk İçecekler", "Toplam Fiyat", "Durum"])
        self.order_table.setColumnHidden(0, True)  # Masa No
        self.order_table.setColumnHidden(4, True)  # Toplam Fiyat
        self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.order_table)

        self.update_orders(order_table)

    def update_orders(self, source_table):
        self.order_table.setRowCount(source_table.rowCount())

        for row_num in range(source_table.rowCount()):
            for col_num in range(source_table.columnCount()):
                item = source_table.item(row_num, col_num)
                if item and col_num not in [0, 4]:
                    self.order_table.setItem(row_num, col_num, QTableWidgetItem(item.text()))

            combo = QComboBox()
            combo.addItems([
                "Hazırlanıyor", "Tamamlandı", "Servis Edildi",
                "İptal Edildi", "Gecikmeli", "Servise Hazır"
            ])
            combo.setCurrentText("Hazırlanıyor")
            combo.currentIndexChanged.connect(lambda _, r=row_num, c=combo: self.update_order_status(r, c))
            self.order_table.setCellWidget(row_num, 5, combo)


    def update_order_status(self, row, combo):
        yeni_durum = combo.currentText()
        print(f"Sipariş {row + 1} durumu güncellendi: {yeni_durum}")
        
        # Durumu tabloya yaz
        self.order_table.setItem(row, 5, QTableWidgetItem(yeni_durum))

# Ana Uygulama 
class KafeSiparisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kafe Sipariş Takip")
        self.setGeometry(100, 100, 700, 500)
        self.conn = sqlite3.connect('kafe_siparis.db')  # SQLite veritabanına bağlanmanızı sağlar
        self.cursor = self.conn.cursor()  # veritabanı üzerinde sorgular yapabilmemizi sağlar
        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
 
 # Sekmeler oluşturuldu
        self.order_tab = self.init_order_tab()
        self.view_tab = self.init_view_tab()
        self.update_tab = self.init_update_tab()
        self.kitchen_tab = self.init_kitchen_tab()
        self.help_tab = self.init_help_tab()

        tabs.addTab(self.order_tab, "Sipariş Ekle")
        tabs.addTab(self.view_tab, "Siparişleri Görüntüle")
        tabs.addTab(self.update_tab, "Siparişi Güncelle")
        tabs.addTab(self.kitchen_tab, "Mutfak")  
        tabs.addTab(self.help_tab, "Yardım")
        self.tabs = tabs
        
    def init_kitchen_tab(self): 
        kitchen_button = QPushButton("Mutfak Ekranını Aç")
        kitchen_button.clicked.connect(self.open_kitchen_window)
        layout = QVBoxLayout()
        layout.addWidget(kitchen_button)
        kitchen_tab = QWidget()
        kitchen_tab.setLayout(layout)
        return kitchen_tab
    
    def open_kitchen_window(self):
        self.kitchen_window = KitchenWindow(self.order_table)
        self.kitchen_window.show()

    # Sipariş Ekle 
    def init_order_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.masa_input = QLineEdit()
        layout.addWidget(QLabel("Masa Numarası:"))
        layout.addWidget(self.masa_input)

        self.tatli_list = self.create_menu_list(layout, "Tatlılar")
        self.sicak_list = self.create_menu_list(layout, "Sıcak İçecekler")
        self.soguk_list = self.create_menu_list(layout, "Soğuk İçecekler")
        add_button = QPushButton("Siparişi Ekle")
        add_button.clicked.connect(self.add_order)
        layout.addWidget(add_button)

        tab.setLayout(layout)
        return tab

# Listwidget oluşturan metot 
    def create_menu_list(self, layout, category):
        label = QLabel(category + ":")
        list_widget = QListWidget()
        list_widget.setSelectionMode(QAbstractItemView.MultiSelection) # QListWiget ta birden çok seçeneği seçebilmemizi sağlar
        self.load_items_for_category(category, list_widget) 
        layout.addWidget(label)
        layout.addWidget(list_widget)
        return list_widget

    def load_items_for_category(self, category_name, list_widget):  # Bu fonksiyon, menü öğelerini veritabanından alır ve bunları QListWidget'a ekler.
        list_widget.clear()
        self.cursor.execute('''
            SELECT DISTINCT name FROM MenuItems 
            WHERE category_id = (SELECT id FROM Categories WHERE name = ?)
        ''', (category_name,))  # veri tabanına sorgu gönderiyor
        for item in self.cursor.fetchall(): # Veri tabanından gelen öğeyi döngü olarak işler
            list_widget.addItem(item[0]) # öğeleri listeye ekler

    def add_order(self):

        masa = self.masa_input.text()
        tatli_items = [i.text() for i in self.tatli_list.selectedItems()]
        sicak_items = [i.text() for i in self.sicak_list.selectedItems()]
        soguk_items = [i.text() for i in self.soguk_list.selectedItems()]
    
        tatli = ", ".join(tatli_items)
        sicak = ", ".join(sicak_items)
        soguk = ", ".join(soguk_items)
    
        # Toplam fiyatı hesapla
        toplam = 0
        for urun in tatli_items + sicak_items + soguk_items:
            self.cursor.execute("SELECT price FROM MenuItems WHERE name = ?", (urun,))
            result = self.cursor.fetchone()
            if result:
                toplam += result[0]
    
        row = self.order_table.rowCount()
        self.order_table.insertRow(row)
        self.order_table.setItem(row, 0, QTableWidgetItem(masa))
        self.order_table.setItem(row, 1, QTableWidgetItem(tatli))
        self.order_table.setItem(row, 2, QTableWidgetItem(sicak))
        self.order_table.setItem(row, 3, QTableWidgetItem(soguk))
        self.order_table.setItem(row, 4, QTableWidgetItem(f"{toplam:.2f} TL"))  # Fiyat eklendi
    
        self.masa_input.clear()
        self.tatli_list.clearSelection()
        self.sicak_list.clearSelection()
        self.soguk_list.clearSelection()
    

     # Siparişleri Görüntüle 
    def init_view_tab(self):

        tab = QWidget()
        layout = QVBoxLayout()

        self.order_table = QTableWidget()
        self.order_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Masa No", "Tatlılar", "Sıcak İçecekler", "Soğuk İçecekler","Toplam Fiyat"])
        layout.addWidget(self.order_table)
       

        delete_button = QPushButton("Siparişi Sil")
        delete_button.clicked.connect(self.delete_order)
        layout.addWidget(delete_button)

        update_button = QPushButton("Siparişi Güncelle")
        update_button.clicked.connect(self.open_update_tab)
        layout.addWidget(update_button)

        tab.setLayout(layout)
        return tab
    
    
    def delete_order(self):
        selected = self.order_table.currentRow()
        if selected >= 0:
            self.order_table.removeRow(selected)

    def open_update_tab(self):
        row = self.order_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Güncellenecek bir sipariş seçin.")
            return

        self.update_masa_input.setText(self.order_table.item(row, 0).text())
        self.select_items_in_list(self.update_tatli_list, self.order_table.item(row, 1).text())
        self.select_items_in_list(self.update_sicak_list, self.order_table.item(row, 2).text())
        self.select_items_in_list(self.update_soguk_list, self.order_table.item(row, 3).text())
        self.tabs.setCurrentWidget(self.update_tab)

    def select_items_in_list(self, list_widget, items_string):
        items = [i.strip() for i in items_string.split(',')]
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setSelected(item.text() in items)

    # Sipariş Güncelle 
    def init_update_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.update_masa_input = QLineEdit()
        layout.addWidget(QLabel("Masa Numarası:"))
        layout.addWidget(self.update_masa_input)

        self.update_tatli_list = QListWidget()
        self.update_sicak_list = QListWidget()
        self.update_soguk_list = QListWidget()

        for widget, name in [(self.update_tatli_list, "Tatlılar"),
                             (self.update_sicak_list, "Sıcak İçecekler"),
                             (self.update_soguk_list, "Soğuk İçecekler")]:
            widget.setSelectionMode(QAbstractItemView.MultiSelection)
            layout.addWidget(QLabel(name + ":"))
            layout.addWidget(widget)
            self.load_items_for_category(name, widget)

        save_button = QPushButton("Güncellemeyi Kaydet")
        save_button.clicked.connect(self.update_selected_order)
        layout.addWidget(save_button)

        tab.setLayout(layout)
        return tab

    def update_selected_order(self):
        row = self.order_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Güncellenecek sipariş yok.")
            return

        masa = self.update_masa_input.text()
        tatli = ", ".join([i.text() for i in self.update_tatli_list.selectedItems()])
        sicak = ", ".join([i.text() for i in self.update_sicak_list.selectedItems()])
        soguk = ", ".join([i.text() for i in self.update_soguk_list.selectedItems()])

        # Toplam fiyatı hesapla
        selected_items = tatli.split(", ") + sicak.split(", ") + soguk.split(", ")
        total_price = 0
        for item in selected_items:
            if item:  # boş string varsa atla
                self.cursor.execute("SELECT price FROM MenuItems WHERE name = ?", (item,))
                result = self.cursor.fetchone()
                if result:
                    total_price += result[0]

        # Veritabanında siparişi güncelle
        siparis_id_item = self.order_table.item(row, 5)  # 5. sütun ID ise
        if siparis_id_item:
            siparis_id = siparis_id_item.text()
            self.cursor.execute("""
                UPDATE Siparisler
                SET masa = ?, tatli = ?, sicak = ?, soguk = ?, toplam_fiyat = ?
                WHERE id = ?
            """, (masa, tatli, sicak, soguk, total_price, siparis_id))
            self.conn.commit()

        # Tabloyu güncelle
        self.order_table.setItem(row, 0, QTableWidgetItem(masa))
        self.order_table.setItem(row, 1, QTableWidgetItem(tatli))
        self.order_table.setItem(row, 2, QTableWidgetItem(sicak))
        self.order_table.setItem(row, 3, QTableWidgetItem(soguk))
        self.order_table.setItem(row, 4, QTableWidgetItem(f"{total_price:.2f}"))

        QMessageBox.information(self, "Başarılı", "Sipariş güncellendi!")



    def init_help_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
    
    
        help_text = QLabel('''
               <div style="font-size: 16px; line-height: 1.5; width: 90%; margin: auto; color: #4A4A4A;">
                   <h2 style="color: #8B4513;">☕ Yardım & SSS</h2>
        
                   <p><b>🟢 1. Nasıl giriş yapabilirim?</b><br>
                   Uygulama açıldığında karşınıza giriş ekranı gelir.<br>
                   <b>Kullanıcı adı:</b> zeynep<br>
                   <b>Parola:</b> <code>12345</code></p>
        
                   <p><b>➕ 2. Sipariş nasıl eklenir?</b><br>
                   “Sipariş Ekle” sekmesinde masa numarasını ve ürünleri seçin.<br>
                   “Sipariş Ekle” butonuna tıklayın.</p>
        
                   <p><b>📋 3. Siparişleri nasıl görebilirim?</b><br>
                   “Siparişler” sekmesinde tüm mevcut siparişleri listeleyebilirsiniz.</p>
        
                   <p><b>❌ 4. Sipariş nasıl silinir?</b><br>
                   Listeden bir sipariş seçin.<br>
                   “Siparişi Sil” butonuna basın.</p>
        
                   <p><b>🔧 5. Mutfak ekranında sipariş durumu nasıl güncellenir?</b><br>
                   Mutfak sekmesindeki sipariş listesinde durum sütunundan bir siparişi seçin.<br>
                   Durum değiştirmek için açılır menüden yeni bir durum seçin.</p>
        
                   <p><b>⚠️ 6. Hatalar ve Uyarılar:</b><br>
                   Yanlış bir işlem yapıldığında veya eksik bilgi girildiğinde bir hata mesajı görüntülenir.<br>
                   Mesajdaki talimatlara göre doğru adımı izleyin.</p>
        
                   <p><b>📞 Yardım ve Destek:</b><br>
                   Geliştiriciye e-posta atabilirsiniz:<br>
                   ✉️ <i>zeynep.destek@kafesistem.com</i></p>
               </div>
               ''')
        
        help_text.setWordWrap(True)  # metin kutusundaki metnin satır sonuna geldiğinde, kelimenin tamamının bir alt satıra taşınmasını sağlar.
        layout.addWidget(help_text)
    
        tab.setLayout(layout)
        return tab

def apply_stylesheet(app):
    style = """
        QWidget {
            font-family: 'Segoe UI', Arial;
            font-size: 14px;
            background-color: #fdf6f0;
        }

        QMainWindow {
            background-color: #fdf6f0;
        }

        QPushButton {
            background-color: #a0522d;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 12px;
        }

        QPushButton:hover {
            background-color: #c1703c;
        }

        QLineEdit, QListWidget, QTableWidget {
            background-color: #ffffff;
            border: 1px solid #d3c4b6;
            border-radius: 6px;
            padding: 6px;
        }

        QTabWidget::pane {
            border: 2px solid #d3c4b6;
            border-radius: 12px;
            background-color: #fffdf9;
        }

        QTabBar::tab {
            background: #e3d5c0;
            border: 1px solid #cbb89f;
            padding: 10px 18px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            margin-right: 4px;
        }

        QTabBar::tab:selected {
            background: #fffaf3;
            border-bottom: none;
            font-weight: bold;
        }

        QLabel {
            font-weight: bold;
            color: #5c3a21;
        }

        QListWidget::item:selected {
            background-color: #ffe4b5;
            color: #5c3a21;
        }

        QTableWidget {
            gridline-color: #d3c4b6;
            background-color: #fffdf9;
            alternate-background-color: #f7f1ea;
        }

        QHeaderView::section {
            background-color: #a0522d;
            color: white;
            padding: 6px;
            border: none;
        }
    """
    app.setStyleSheet(style)



# Uygulama Başlat
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
