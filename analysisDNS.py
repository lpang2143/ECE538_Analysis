from enum import Enum
import tldextract
from resolveSOA import getSOA
import sys

class NS_TYPE(Enum):
    UNKNOWN = 1
    PRIVATE = 2
    THIRD = 3

def main():
    f = open('ns_unique', 'r')
    out = open(sys.argv[1], 'w')
    for line in f:
        ns_type = NS_TYPE.UNKNOWN
        host = ''
        line = line.split(':')
        w = line[0]
        ns = line[1].split(' ')[1:]
        if 'NXDOMAIN' in ns or 'SERVFAIL' in ns or not ns:
            continue

        # check if tld matches
        if ns_type == NS_TYPE.UNKNOWN:
            w_ext = tldextract.extract(w)
            w_tld = ".".join([w_ext.domain, w_ext.suffix])
            for n in ns:
                n_ext = tldextract.extract(n)
                n_tld = ".".join([n_ext.domain, n_ext.suffix])
                host = n_tld
                if (w_tld == n_tld):
                    ns_type = NS_TYPE.PRIVATE
                    break;
                

        # check if SOA matches
        if ns_type == NS_TYPE.UNKNOWN:
            w_soa = getSOA(w)
            for n in ns:
                n_soa = getSOA(n)
                if (w_soa != n_soa):
                    ns_type = NS_TYPE.THIRD
                    break;

        
        if ns_type == NS_TYPE.UNKNOWN:
            final = 'UNKNOWN'
        elif ns_type == NS_TYPE.PRIVATE:
            final = 'PRIVATE'
        else:
            final = 'THIRD'

        out.write(f"{w} {final} {host}\n")
                


    f.close()
if __name__ == '__main__':
    main()