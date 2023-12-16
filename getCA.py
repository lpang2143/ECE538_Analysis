def getSAN(site):
    f = open('certificates_line.txt', 'r')
    for line in f:
        if 'Error' in line:
            continue
        line = line.split('/')
        w = line[0].strip(':')
        if site != w:
            continue
        sub = line[3].split(':')[1].replace('(', '').replace(')', '').replace('\'', '').replace(' ', '')
        return [x for x in sub.split(',') if 'DNS' not in x]
    return ''


# if __name__ == "__main__":
#     main()