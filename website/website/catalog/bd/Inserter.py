import sqlite3
import numpy as np
import pandas as pd


class Inserter():
    def __init__(self, DB):
        self.connector = sqlite3.connect(DB)
        self.c = self.connector.cursor()
        self.c.execute("PRAGMA foreign_keys = ON")
        self.connector.commit()
        np.random.seed(4404)
        

    def insertArticle(self, idd, name, keywords, pages, year, volume, issue, abstract):
        kw = ';'.join(keywords)
        teststatement = 'SELECT Article.ID ' \
                        'FROM Article ' \
                        'WHERE Article.ID = ?'
        self.c.execute(teststatement, [idd])
        self.connector.commit()
        q = np.array(self.c.fetchall())
        if len(q) == 0:
            values = np.hstack((idd, name, year, volume, issue, pages, kw, abstract))
            self.c.executemany("INSERT INTO Article VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [values])
            self.connector.commit()
            return True
        return False
    
    def updateKeywords(self, idd, keywords):
        kw = ';'.join(keywords)
        teststatement = 'SELECT Article.ID ' \
                        'FROM Article ' \
                        'WHERE Article.ID = ?'
        self.c.execute(teststatement, [idd])
        self.connector.commit()
        q = np.array(self.c.fetchall())
        values = np.hstack((kw, idd))
        if len(q) != 0:
            teststatement = 'UPDATE Article '\
                            'SET KeyWords = ? '\
                            'WHERE ID = ?'
            self.c.execute(teststatement, values)
            self.connector.commit()
    
    def updateYear(self, idd, year):
        teststatement = 'SELECT Article.ID ' \
                        'FROM Article ' \
                        'WHERE Article.ID = ?'
        self.c.execute(teststatement, [idd])
        self.connector.commit()
        q = np.array(self.c.fetchall())
        values = np.hstack((year, idd))
        if len(q) != 0:
            teststatement = 'UPDATE Article '\
                            'SET Year = ? '\
                            'WHERE ID = ?'
            self.c.execute(teststatement, values)
            self.connector.commit()
    
    def updateName(self, idd, name):
        teststatement = 'SELECT Article.ID ' \
                        'FROM Article ' \
                        'WHERE Article.ID = ?'
        self.c.execute(teststatement, [idd])
        self.connector.commit()
        q = np.array(self.c.fetchall())
        values = np.hstack((name, idd))
        if len(q) != 0:
            teststatement = 'UPDATE Article '\
                            'SET ArticleName = ? '\
                            'WHERE ID = ?'
            self.c.execute(teststatement, values)
            self.connector.commit()

    def insertAuthor(self, Name):
        teststatement = 'SELECT Author.Name FROM Author ' \
                        'WHERE Author.Name = ?'
        self.c.execute(teststatement, [Name])
        self.connector.commit()
        q = np.array(self.c.fetchall())
        if len(q) == 0:
            self.c.executemany("INSERT INTO Author VALUES( ?)", [[Name]])
            self.connector.commit()

    def insertHas(self, Article_id, Author_name):
        #selectStatement = 'SELECT Article.ID FROM Article ' \
        #                  'WHERE Article.ID = ?'
        #self.c.execute(selectStatement, [Article_id])
        #self.connector.commit()
        #res = np.array(self.c.fetchall())
        #print(res)
        values = np.hstack((Article_id, Author_name))
        teststatement = 'SELECT Has.Article_ID FROM Has ' \
                        'WHERE Has.Article_ID = ? AND Has.Author_Name = ?'
        self.c.execute(teststatement, values)
        self.connector.commit()
        q = np.array(self.c.fetchall())
        if len(q) == 0:
            self.c.executemany("INSERT INTO Has VALUES( ?, ?)", [values])
            self.connector.commit()

    def insertCitations(self, Article_id_f, Article_id_s):
        selectStatement = 'SELECT Article.ID FROM Article ' \
                          'WHERE Article.ID = ?'
        self.c.execute(selectStatement, [Article_id_f])
        self.connector.commit()
        res = np.array(self.c.fetchall())
        if len(res) == 0:
            return
        selectStatement = 'SELECT Article.ID FROM Article ' \
                          'WHERE Article.ID = ?'
        self.c.execute(selectStatement, [Article_id_s])
        self.connector.commit()
        res = np.array(self.c.fetchall())
        if len(res) == 0:
            return
        selectStatement = 'SELECT Citation.Article_FID FROM Citation ' \
                          'WHERE Citation.Article_FID = ? AND Citation.Article_SID = ?'
        values = np.hstack((Article_id_f, Article_id_s))
        self.c.execute(selectStatement, values)
        self.connector.commit()
        res = np.array(self.c.fetchall())
        if len(res) == 0:
            self.c.executemany("INSERT INTO Citation VALUES( ?, ?)", [values])
            self.connector.commit()

    def closeConnect(self):
        self.connector.close()


