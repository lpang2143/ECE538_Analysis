from enum import Enum
import tldextract as tld
from resolveSOA import getSOA
import sys
from utils import DEP_TYPE

def main():
    f = open('domains', 'r')
    out = open(sys.argv[1], 'w')
    for line in f:
        cdn_type = DEP_TYPE.UNKNOWN
        host = ''
        w = line.strip('\n').split()[1]
        
        
        # things we need:
        # -cdn(w)
        # -cnames(cdn, w)
        # -isHTTPS(w)
        # -tld(w)
        # -isHTTPS(w)
        # -SAN(w)
        # -SOA(w)
        # -SOA(cnames)

        w_ext = tld.extract(w)
        tld_w = ".".join([w_ext.domain, w_ext.suffix])
        cnames = getCNAMES(cdn, w)
        isHTTPS_w = isHTTPS(w)
        SAN_w = getSAN(w)
        SOA_w = getSOA(w)

        for cname in cnames:
            cname_ext = tld.extract(cname)
            tld_cname = ".".join([cname_ext.domain, cname_ext.suffix])
            SOA_cname = getSOA(cname)
            # check if tld matches
            if tld_w == tld_cname:
                cdn_type = DEP_TYPE.PRIVATE
            # check if HTTPS and tld(cname) in SAN(w)
            elif (isHTTPS_w and tld_cname in SAN_w):
                cdn_type = DEP_TYPE.PRIVATE
            # check if SOA(cname) != SOA(w)
            elif (SOA_cname != SOA_w):
                cdn_type = DEP_TYPE.THIRD

        
        if ca_type == DEP_TYPE.UNKNOWN:
            final = 'UNKNOWN'
        elif ca_type == DEP_TYPE.PRIVATE:
            final = 'PRIVATE'
        else:
            final = 'THIRD'

        out.write(f"{w} {final} {host}\n")
    f.close()
    out.close()


