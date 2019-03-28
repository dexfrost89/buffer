import sqlite3
import numpy as np
import pandas as pd


class Selector():
    def __init__(self, DB):
        self.connector = sqlite3.connect(DB)
        self.c = self.connector.cursor()
        self.c.execute("PRAGMA foreign_keys = ON")
        self.connector.commit()
        np.random.seed(4404)
    
    def make_df_authors(self):
        df = pd.DataFrame({'id':[], 'authors_list':[]})
        statement = 'SELECT Article.ID FROM Article'
        self.c.execute(statement)
        self.connector.commit()
        articlesid = np.array(self.c.fetchall())
        for art in articlesid:
            statement = 'SELECT Has.Author_Name ' \
                        'FROM Has ' \
                        'WHERE Has.Article_ID = ?'
            self.c.execute(statement, art)
            self.connector.commit()
            authors = np.array(self.c.fetchall())
            author_list = []
            for auth in authors:
                author_list.append(auth[0])
            df = df.append({'id':art[0], 'authors_list':author_list}, ignore_index=True)
        return df

    def make_df_for_year(self, year):
        df = pd.DataFrame({'id':[], 'authors_list':[]})
        statement = 'SELECT Article.ID ' \
                    'FROM Article ' \
                    'WHERE Article.Year = ?'
        self.c.execute(statement, [year])
        self.connector.commit()
        articlesid = np.array(self.c.fetchall())
        for art in articlesid:
            statement = 'SELECT Has.Author_Name ' \
                        'FROM Has ' \
                        'WHERE Has.Article_ID = ?'
            self.c.execute(statement, art)
            self.connector.commit()
            authors = np.array(self.c.fetchall())
            author_list = []
            for auth in authors:
                author_list.append(auth[0])
            df = df.append({'id':art[0], 'authors_list':author_list}, ignore_index=True)
        return df
    
    def make_df_citations(self):
        df = pd.DataFrame({"Article unique ID":[], "List of key words":[], "List of citated articles' IDs in database":[]})
        statement = 'SELECT Article.ID, Article.KeyWords FROM Article'
        self.c.execute(statement)
        self.connector.commit()
        articlesid = np.array(self.c.fetchall())
        for art in articlesid:
            statement = 'SELECT Citation.Article_SID ' \
                        'FROM Citation ' \
                        'WHERE Citation.Article_FID = ?'
            self.c.execute(statement, [art[0]])
            self.connector.commit()
            citations = np.array(self.c.fetchall())
            cit_list = []
            for cit in citations:
                cit_list.append(cit[0])
            keywords = art[1].split(';')
            df = df.append({"Article unique ID":art[0], "List of key words":keywords, "List of citated articles' IDs in database":cit_list}, ignore_index=True)
        return df
    
    def make_df_citations_for_year(self, year):
        df = pd.DataFrame({"Article unique ID":[], "List of key words":[], "List of citated articles' IDs in database":[]})
        statement = 'SELECT Article.ID, Article.KeyWords ' \
                    'FROM Article ' \
                    'WHERE Article.Year = ?'
        self.c.execute(statement, [year])
        self.connector.commit()
        articlesid = np.array(self.c.fetchall())
        for art in articlesid:
            statement = 'SELECT Citation.Article_SID ' \
                        'FROM Citation ' \
                        'WHERE Citation.Article_FID = ?'
            self.c.execute(statement, [art[0]])
            self.connector.commit()
            citations = np.array(self.c.fetchall())
            cit_list = []
            for cit in citations:
                statement = 'SELECT Article.Year ' \
                            'FROM Article ' \
                            'WHERE Article.ID = ?'
                self.c.execute(statement, cit)
                self.connector.commit()
                cit_year = np.array(self.c.fetchall())
                if (cit_year[0][0] == year):
                    cit_list.append(cit[0])
            keywords = art[1].split(';')
            df = df.append({"Article unique ID":art[0], "List of key words":keywords, "List of citated articles' IDs in database":cit_list}, ignore_index=True)
        return df

    def closeConnect(self):
        self.connector.close()
