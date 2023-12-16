import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import pandas as pd


# print(nx.__version__)

ca_map = {'Amazon': 'amazontrust.com', 'Google Trust Services LLC': 'pki.goog', 'Entrust, Inc.': 'entrust.com', 
            'DigiCert Inc': 'digicert.com', 'Sectigo Limited': 'sectigo.com', 'COMODO CA Limited': 'comodoca.com', 'Microsoft Corporation': 'microsoft.com',
            'Let\'s Encrypt': 'letsencrypt.org', 'Cloudflare, Inc.': 'cloudflare.com', 'GlobalSign nv-sa': 'globalsign.com', 'ZeroSSL': 'zerossl.com'}

def digraphPlot():
    f = open('ca_categorized.txt', 'r')
    count = 0
    labels = {}
    DG = nx.DiGraph()
    for line in f:
        if 'failed' in line or 'address_error' in line:
            continue
        line = line.split(':')
        trust = line[2].strip('\n')
        DG.add_edge(f"{str(count)}", trust, weight = 1)
        count += 1

    for node in DG.nodes():
        # print(node)
        if node in ca_map.keys():
            # print(node)
            labels[node] = node

    d = dict(DG.degree)

    # values = [val_map.get(node, 0.25) for node in DG.nodes()]
    # print(d)
    
    nx.draw(DG, nodelist=list(d.keys()), node_size=[v * 100 for v in d.values()], with_labels=False, cmap=plt.get_cmap('jet'))
    pos = nx.drawing.nx_agraph.graphviz_layout(DG)
    nx.draw_networkx_labels(DG, pos, labels, font_size=12, font_color='r')
    
    # pos = nx.spring_layout(DG)
    # nx.draw_networkx_nodes(DG, pos, cmap=plt.get_cmap('jet'),
    #                         node_color=values, node_size=500)
    plt.show()


def piePlot():
    sb.set_theme(style="whitegrid", palette="pastel")
    data = []
    keys = []
    f = open('ca_stats.txt', 'r')
    for line in f:
        line = line.split(":")
        val = line[1].strip('\n')
        data.append(val)
        if int(val) > 20:
            keys.append(line[0])
        else:
            keys.append('')

    # df = pd.DataFrame({'Category': data})
    # sizes = df['Category'].sort_values()

    plt.pie(data, labels=keys)
    # plt.legend(loc=3, labels=keys)
    # plot = plt.get_figure()
    plt.savefig('CA_pie', bbox_inches='tight')

def histPlot():
    sb.set_theme(style="whitegrid", palette="pastel")
    data = []
    f = open('ca_categorized_method.txt', 'r')
    for line in f:
        if 'failed' in line or 'address_error' in line:
            continue
        line = line.split(":")
        val = line[2]
        # print(val)
        data.append(val)

    # df = pd.DataFrame({'Category': data})
    # sizes = df['Category'].sort_values()

    sb.histplot(data, element='bars', legend=True)
    plt.xticks(rotation=45)
    # plt.legend(loc=3, labels=keys)
    plt.show()
    plt.tight_layout()
    # plot = plt.get_figure()
    # plt.savefig('CA_pie', bbox_inches='tight')

if __name__ == "__main__":
    histPlot()