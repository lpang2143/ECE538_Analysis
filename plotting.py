# import matplotlib.pyplot as plt
# import numpy as np
import pandas
from collections import Counter

def histogram_plot():
    f = open('categorized', 'r')
    f2 = open('domains', 'r')
    w = {}
    for line in f:
        line = line.strip('\n').split(' ')
        # if 'THIRD' in line:
        #     third += 1
        # else:
        #     private += 1
        # w.append(line[2])
        for line2 in f2:
            if 'tcp.local' in line2:
                continue
            if line[0] in line2:
                count = int(line2.split()[0])

        if line[2] in w:
            w[line[2]] += count
        else:
            w[line[2]] = count


    f.close()
    # print(third)
    # print(private)
    # print(w)
    w = dict(sorted(w.items(), key=lambda w:w[1], reverse=True))
    w_labels = list(w.keys())

    i = 0
    for label in w_labels:
        if i > 10:
            w_labels[i] = "_" + label
        i += 1

    print(w_labels)
    df = pandas.DataFrame({'hosts': w.keys(), 'counts': w.values()}, index=w.keys())
    plt = df.plot.pie(y='counts', labels=None)
    plt.legend(loc='lower right', bbox_to_anchor=(1.5, 0.4), labels=w_labels)
    plot = plt.get_figure()
    plot.savefig('plot3.png', bbox_inches='tight')



    # host_count = dict(Counter(w).most_common(15))
    # df = pandas.DataFrame.from_dict(host_count, orient='index')
    # plt = df.plot(kind='bar', rot=45, legend=False)
    # plt.set_xticklabels(host_count.keys(), fontsize=8)
    # plt.set_ylabel('Counts',fontdict={'fontsize':15})
    # plt.set_xlabel('Host DNS',fontdict={'fontsize':15})
    # plot = plt.get_figure()
    # plot.subplots_adjust(bottom=0.25)
    # plot.savefig('plot2.png')

if __name__ == '__main__':
    histogram_plot()