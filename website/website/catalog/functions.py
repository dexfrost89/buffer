from .bd.Selector import Selector
import networkx as nx
import matplotlib.pyplot as plt

name = 'test.db'

def create_df_authors_for_year(year, DB_name=name):
    testDB = Selector(DB_name)
    df = testDB.make_df_for_year(year)
    testDB.closeConnect()
    return df


def create_df_authors_for_period(start, finish, DB_name=name):

    df = create_df_authors_for_year(start, DB_name)
    for year in range(start + 1, finish + 1):
        df = df.append(create_df_authors_for_year(year, DB_name))
    return df


def create_graph_from_pandas_df(df):
    """ Takes pandas dataframe and create networkx graph. We suggest every row in df
        is an article with next columns: 'list of authors' (list of strings)
    """
    G = nx.Graph()

    for num, row in df.iterrows():
        authors_list = row['authors_list']
        # connect every one and update edges
        for i in range(len(authors_list)):
            for j in range(i + 1, len(authors_list)):
                from_, to_ = authors_list[i], authors_list[j]
                new_weight = (G[from_][to_]['weight'] if G.has_edge(from_, to_) else 0) + 1
                G.add_edge(from_, to_, weight=new_weight)

    return G


def create_df_for_citations(DB_name=name):
    testDB = Selector(DB_name)
    df = testDB.make_df_citations()
    testDB.closeConnect()
    return df


def create_df_for_citations_for_year(year, DB_name=name):
    testDB = Selector(DB_name)
    df = testDB.make_df_citations_for_year(year)
    testDB.closeConnect()
    return df


def MakeCitationGraph(table):
    graph = nx.DiGraph()
    grDesc = dict()
    for i in range(len(table["Article unique ID"])):
        grDesc[table["Article unique ID"][i]] = [table["List of key words"][i], table["List of citated articles' IDs in database"][i]]
        #if grDesc[table["Article unique ID"][i]][1] != []:
        graph.add_node(table["Article unique ID"][i])
    #print(grDesc)
    for i in grDesc:
        for j in grDesc[i][1]:
            w = 0
            for k in grDesc[j][0]:
                if(k in grDesc[i][0]):
                    w += 1
            graph.add_weighted_edges_from([(i, j, w)])
    return graph


def getGraph(year, type):
    if type == 'co-authorship':
        df = create_df_authors_for_year(year)
        G = create_graph_from_pandas_df(df)
    elif type == 'citations':
        df = create_df_for_citations_for_year(year)
        G = MakeCitationGraph(df)
    if drawG(G, year, type, 'random') != 0:
        print('something went wrong!')
    return G


def drawG(G, year, type, layout):
    nx.draw(G)
    plt.figure(figsize=(30, 30))
    plt.axis('off')
    if layout == 'random':
        layout = nx.random_layout(G)
    if layout == 'circular':
        layout = nx.circular_layout(G)
    if layout == 'kamada_kawai':
        layout = nx.kamada_kawai_layout(G)
    if layout == 'spring':
        layout = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos=layout)
    nx.draw_networkx_nodes(G, pos=layout, node_color='blue')
    plt.title(type + ' ' + str(year), fontsize=80)
    plt.draw()
    plt.savefig('catalog/static/Graphs/Graph.png')



