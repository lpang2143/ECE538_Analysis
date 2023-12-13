from enum import Enum
import tldextract as tld
from resolveSOA import getSOA
import sys
import DEP_TYPE

def main():
    f = open('ns_unique', 'r')
    out = open(sys.argv[1], 'w')
    for line in f:
        ca_type = DEP_TYPE.UNKNOWN
        host = ''
        line = line.split(':')
        w = line[0]
        ns = line[1].split(' ')[1:]
        if 'NXDOMAIN' in ns or 'SERVFAIL' in ns or not ns:
            continue
        
        # things we need:
        # -tld(w)
        # -tld(ca_url)
        # -isHTTPS(w)
        # -SAN(w)
        # -SOA(w)
        # -SOA(ca_url)

        w_ext = tld.extract(w)
        tld_w = ".".join([w_ext.domain, w_ext.suffix])
        ca = getCA(w)
        ca_ext = tld.extract(ca)
        tld_ca = ".".join([ca_ext.domain, ca_ext.suffix])
        isHTTPS_w = isHTTPS(w)
        SAN_w = getSAN(w)
        SOA_w = getSOA(w)
        SOA_ca = getSOA(ca)

        # check if tld matches
        if tld_w == tld_ca:
            ca_type = DEP_TYPE.PRIVATE
        elif (isHTTPS_w and tld_ca in SAN_w):
            ca_type = DEP_TYPE.PRIVATE
        elif (SOA_ca != SOA_w):
            ca_type = DEP_TYPE.THIRD

        
        if ca_type == DEP_TYPE.UNKNOWN:
            final = 'UNKNOWN'
        elif ca_type == DEP_TYPE.PRIVATE:
            final = 'PRIVATE'
        else:
            final = 'THIRD'

        out.write(f"{w} {final} {host}\n")
    f.close()
    out.close()
        