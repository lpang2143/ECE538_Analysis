import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import pandas as pd

def piePlot():
    sb.set_theme(style="whitegrid", palette="pastel")
    data = []
    keys = []
    f = open('dns_categorized_method.txt', 'r')
    f2 = open('domains', 'r')
    w = {'aws': 0, 'aka': 0, 'cloudflare': 0, 'msedge': 0, 'google': 0}
    lines = 0
    default = 0
    notdefault = 0
    defaults = list(w.keys())
    for line in f:
        print("from main", line)
        count = 0
        lines += 1
        if 'failed' in line:
            continue
        line = line.strip('\n').split(' ')
        # print(line)

        # for line2 in f2:
        #     print(line2)
        #     if 'tcp.local' in line2:
        #         continue
        #     if line[0] in line2:
        #         count = int(line2.split()[0])

        # aggregate all similar dns's
        flag = 1
        for dns in defaults:
            if dns in line[2]:
                w[dns] += 1
                flag = 0
                default += 1
                break

        if flag:
            notdefault += 1
            if line[2] in w:
                # w[line[2]] += count
                w[line[2]] += 1
            else:
                # w[line[2]] = count
                w[line[2]] = 1

    # print(w.keys())
    # print(lines)
    # print(sum(w.values()))
    # print(default)
    # print(notdefault)
    vk_pairs = ((value, key) for (key, value) in w.items())
    sorted_w = sorted(vk_pairs, reverse=True)
    print(sorted_w)
    w = {k: v for v, k in sorted_w}
    # print(w)
    labels = []
    for key in w.keys():
        if w[key] < 10:
            labels.append('')
        else:
            labels.append(key)

    plt.pie(w.values(), labels=labels)
    # plt.legend(loc=3, labels=keys)
    # plt.show()
    # plot = plt.get_figure()
    plt.savefig('DNS_pie', bbox_inches='tight')
    f.close()
    f2.close()

def histPlot():
    sb.set_theme(style="whitegrid", palette="pastel")
    data = []
    keys = []
    f = open('dns_categorized_method.txt', 'r')
    f2 = open('domains', 'r')
    w = {'aws': 0, 'aka': 0, 'cloudflare': 0, 'msedge': 0, 'google': 0}
    lines = 0
    default = 0
    notdefault = 0
    defaults = list(w.keys())
    for line in f:
        print("from main", line)
        count = 0
        lines += 1
        if 'failed' in line:
            continue
        line = line.strip('\n').split(' ')
        # print(line)

        # for line2 in f2:
        #     print(line2)
        #     if 'tcp.local' in line2:
        #         continue
        #     if line[0] in line2:
        #         count = int(line2.split()[0])

        # aggregate all similar dns's
        flag = 1
        for dns in defaults:
            if dns in line[2]:
                w[dns] += 1
                flag = 0
                default += 1
                break

        if flag:
            notdefault += 1
            if line[2] in w:
                # w[line[2]] += count
                w[line[2]] += 1
            else:
                # w[line[2]] = count
                w[line[2]] = 1

    # print(w.keys())
    # print(lines)
    # print(sum(w.values()))
    # print(default)
    # print(notdefault)
    vk_pairs = ((value, key) for (key, value) in w.items())
    sorted_w = sorted(vk_pairs, reverse=True)
    print(sorted_w)
    w = {k: v for v, k in sorted_w}
    # print(w)
    labels = []
    for key in w.keys():
        if w[key] < 10:
            labels.append('')
        else:
            labels.append(key)

    plt.pie(w.values(), labels=labels)
    # plt.legend(loc=3, labels=keys)
    # plt.show()
    # plot = plt.get_figure()
    plt.savefig('DNS_pie', bbox_inches='tight')
    f.close()
    f2.close()

if __name__ == "__main__":
    piePlot()