import sqlite3

def create_database():
    conn = sqlite3.connect('C:/Users/lenovo/Desktop/proje/kafe_siparis.db')
    cursor = conn.cursor()

    # Kategoriler tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )''')
    
    # Menü öğeleri tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MenuItems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES Categories(id)
    )''')
    
    # Siparişler tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        masa_no TEXT NOT NULL,
        tatli TEXT,
        sicak TEXT,
        soguk TEXT,
        fiyat REAL NOT NULL
    )''')
    
    # Kategorileri ekle
    categories = ['Tatlılar', 'Sıcak İçecekler', 'Soğuk İçecekler']
    for category in categories:
        cursor.execute('INSERT OR IGNORE INTO Categories (name) VALUES (?)', (category,))
    
    # Menü öğelerini ekle
    menu_items = [
        ('Cheesecake',110, 'Tatlılar'),
        ('Tiramisu', 125, 'Tatlılar'),
        ('Profiterol', 100, 'Tatlılar'),
        ('Trileçe', 110, 'Tatlılar'),
        ('Havuçlu Kek',110, 'Tatlılar'),
        ('Çikolatalı Pasta',110, 'Tatlılar'),
        ('San Sebastian',140, 'Tatlılar'),
        ('Brownie',110, 'Tatlılar'),
        ('Sufle',110, 'Tatlılar'),
        ('Waffle',100, 'Tatlılar'),
        
        ('Çay', 35, 'Sıcak İçecekler'),
        ('Türk Kahvesi', 70, 'Sıcak İçecekler'),
        ('Double Türk Kahvesi', 100, 'Sıcak İçecekler'),
        ('Sütlü Türk Kahvesi', 80, 'Sıcak İçecekler'),
        ('Dibek Kahvesi', 85, 'Sıcak İçecekler'),
        ('Expresso', 75, 'Sıcak İçecekler'),
        ('Latte', 110, 'Sıcak İçecekler'),
        ('Mocha', 120, 'Sıcak İçecekler'),
        ('Sütlü Filtre Kahve', 115, 'Sıcak İçecekler'),
        ('Sıcak Çikolata', 110, 'Sıcak İçecekler'),
        ('Ihlamur', 115, 'Sıcak İçecekler'),
        ('Nane Limon', 115, 'Sıcak İçecekler'),
        ('Papatya Çayı', 115, 'Sıcak İçecekler'),

       
        ('Iced Americano', 110, 'Soğuk İçecekler'),
        ('Iced Latte', 110, 'Soğuk İçecekler'),
        ('Iced Mocha', 110, 'Soğuk İçecekler'),
        ('Iced Flat White', 110, 'Soğuk İçecekler'),
        ('Hibiscus', 110, 'Soğuk İçecekler'),   
        ('Limonata', 90, 'Soğuk İçecekler'),
        ('Kutu İçecekler', 65, 'Soğuk İçecekler'),
        ('Su', 20, 'Soğuk İçecekler'),    

    ]

    for item in menu_items:
        cursor.execute('''
        INSERT OR IGNORE INTO MenuItems (name, price, category_id)
        VALUES (?, ?, (SELECT id FROM Categories WHERE name = ?))
        ''', (item[0], item[1], item[2]))
    
    conn.commit()
    conn.close()
    print("Veritabanı başarıyla oluşturuldu ve veri eklendi!")

if __name__ == "__main__":
    create_database()
