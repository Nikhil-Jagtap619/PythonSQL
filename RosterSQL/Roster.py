import sqlite3
import json

conn = sqlite3.connect("learning_management_system.sqlite");
cur = conn.cursor();
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User (
    id    INTEGER PRIMARY KEY NOT NULL UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER PRIMARY KEY NOT NULL UNIQUE,
    title  TEXT UNIQUE
);
CREATE TABLE Member (
    user_id      INTEGER,
    course_id    INTEGER,
    role         TEXT,
    PRIMARY KEY  (user_id, course_id)

);
 ''');

fname = input("enter your file name: ");
if len(fname) < 1:
    fname = "data.json";
fhandle = open(fname).read();
json_data = json.loads(fhandle);
for line in json_data:
    user = line[0];
    course = line[1];
    if line[2] == 0:
        role = "Student";
    else:
        role = "Teacher";
    # role = line[2];   #0 for student and 1 for mentor
    print("User: ", user, "Course :", course, "Role :", role);
    cur.execute('''INSERT OR IGNORE INTO User (name) VALUES (?) ''', (user,));
    cur.execute('''SELECT id FROM User WHERE name = ? ''',(user,));
    user_id = cur.fetchone()[0];

    cur.execute('''INSERT OR IGNORE INTO Course (title) VALUES (?) ''',(course,));
    cur.execute('''SELECT id FROM Course WHERE title = ? ''',(course,));
    course_id = cur.fetchone()[0];

    cur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id) VALUES (?, ?) ''',(user_id, course_id));
    cur.execute('''UPDATE Member SET role = ? WHERE user_id = ? ''', (role, user_id));
    conn.commit();




