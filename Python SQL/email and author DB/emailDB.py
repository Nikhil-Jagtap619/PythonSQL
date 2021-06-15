import sqlite3
conn = sqlite3.connect("emailDB.sqlite");
cur = conn.cursor();
cur.executescript('''
DROP TABLE IF EXISTS Email;
CREATE TABLE Email (email TEXT, count INTEGER, date INTEGER, month TEXT, time INTEGER) ''');
fname = input("enter your file name: ");
if len(fname) < 1:
    fname = "mbox-short.txt";
fh = open(fname);
for line in fh:
    line = line.rstrip();
    if line.startswith("From"):
        arr = line.split();
        if len(arr) > 2:
            email = arr[1];
            date = arr[4];
            month = arr[3];
            time = arr[5];
            #SQL 
            cur.execute('''SELECT count FROM Email WHERE email = ?  ''',(email,));
            row = cur.fetchone();
            if row is None:
                cur.execute('''INSERT INTO Email (email, count, date, month, time) VALUES (?, 1, ?, ?, ?) ''', (email, date, month, time));
            else:
                cur.execute('''UPDATE Email SET count = count + 1 WHERE email = ? ''', (email,));
            
    conn.commit();
        
        

