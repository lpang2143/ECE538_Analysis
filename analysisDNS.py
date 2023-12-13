from enum import Enum
import tldextract as tld
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
        
        # things we need:
        # -tld(w)
        # -tld(ns)
        # -isHTTPS(w)
        # -SAN(w)
        # -SOA(w)
        # -SOA(ns)
        # -concentration(ns)

        w_ext = tld.extract(w)
        tld_w = ".".join([w_ext.domain, w_ext.suffix])
        tld_ns = [".".join([tld.extract(n).domain+tld.extract(n).suffix]) for n in ns]
        isHTTPS_w = isHTTPS(w)
        SAN_w = getSAN(w)
        SOA_w = getSOA(w)
        SOA_ns = [getSOA(n) for n in ns]
        conc_ns = [getConcentration(n) for n in ns]
                
        # check if tld matches
        if tld_w in tld_ns:
            ns_type = NS_TYPE.PRIVATE
        # check if HTTPS and tld(ns) in SAN(w)
        elif (isHTTPS_w and any(n in SAN_w for n in tld_ns)):
            ns_type = NS_TYPE.PRIVATE
        # check if SOA(ns) != SOA(w)
        elif (SOA_ns != SOA_w):
            ns_type = NS_TYPE.THIRD
        # check if concentration(ns) >= 50
        elif (conc_ns >= 50):
            ns_type = NS_TYPE.THIRD
        
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