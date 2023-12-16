from enum import Enum
import tldextract as tld
from resolveSOA import getSOA
import sys
from utils import DEP_TYPE
from getCA import getSAN

def main():
    f = open('ns', 'r')
    out = open(sys.argv[1], 'w')
    out_method = open(sys.argv[2], 'w')
    matches = {'tld': 0, 'san': 0, 'soa': 0, 'total': 0}
    for line in f:
        ns_type = DEP_TYPE.UNKNOWN
        if 'NXDOMAIN' in line or 'SERVFAIL' in line or not line:
            out.write(f"{'failed'}\n")
            continue
        host = ''
        line = line.split(':')
        w = line[0]
        ns = line[1].split(' ')[1:]
        
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
        tld_ns = [".".join([tld.extract(n).domain,tld.extract(n).suffix]) for n in ns]
        SANs = getSAN(w)
        # print(SANs)
        # print(tld_w)
        # print(tld_ns)
        SOA_w = getSOA(w)
        SOA_ns = [getSOA(n) for n in ns]
        inSOA = [SOA_w != soa for soa in SOA_ns]
        # conc_ns = [getConcentration(n) for n in ns]
        inSAN = [tld_ns[0] in SAN for SAN in SANs]
                
        # check if tld matches
        if tld_w in tld_ns:
            ns_type = DEP_TYPE.PRIVATE
            matches['tld'] += 1
        # check if HTTPS and tld(ns) in SAN(w)
        # note only checking first tld as in practice, tld(ns) had 1 unique within ns
        elif (SANs and any(inSAN)):
            print(tld_ns[0])
            print(SANs)
            ns_type = DEP_TYPE.PRIVATE
            matches['san'] += 1
        # check if SOA(ns) != SOA(w)
        elif (any(inSOA)):
            ns_type = DEP_TYPE.THIRD
            matches['soa'] += 1
        # check if concentration(ns) >= 50
        # elif (conc_ns >= 50):
        #     ns_type = DEP_TYPE.THIRD
        matches['total'] += 1
        
        if ns_type == DEP_TYPE.UNKNOWN:
            final = 'UNKNOWN'
        elif ns_type == DEP_TYPE.PRIVATE:
            final = 'PRIVATE'
        else:
            final = 'THIRD'

        out.write(f"{w} {final} {tld_ns[0]}\n")
                
    for key, value in matches.items():
        out_method.write(f"{key}:{value}\n")

    out.close()
    out_method.close()
    f.close()
if __name__ == '__main__':
    main()