from enum import Enum
import tldextract as tld
from resolveSOA import getSOA
import sys
from utils import DEP_TYPE

ca_map = {'Amazon': 'https://www.amazontrust.com', 'Google Trust Services LLC': 'https://pki.goog/', }

def main():
    # f = open('certificates.txt', 'r')
    f = ["aan.amazon.com/Issuer: ((('countryName', 'US'),), (('organizationName', 'Amazon'),), (('commonName', 'Amazon RSA 2048 M01'),))/Subject: ((('commonName', 'aan.amazon.com'),),)/SubjectAltName: (('DNS', 'aan.amazon.com'),)"]
    out = open(sys.argv[1], 'w')
    print(f)
    for line in f:
        line = line.split('/')
        w = line[0]
        ca_line = line[1]
        if 'ERROR' in ca_line:
            if 'CERTIFICATE_VERIFY_FAILED' in ca_line:
                out.write(f"{w} {'failed'}\n")
            else:
                out.write(f"{w} {'address_error'}\n")
            continue
        ca_type = DEP_TYPE.UNKNOWN
        host = ''
        line = line.split('/')
        w = line[0]
        ca_name = line[1].partition('organizationName,')[2].split(')')[0]
        print(w)
        print(ca_name)
        
        
        # things we need:
        # -tld(w)
        # -tld(ca_url)
        # -isHTTPS(w)
        # -SAN(w)
        # -SOA(w)
        # -SOA(ca_url)

        # w_ext = tld.extract(w)
        # tld_w = ".".join([w_ext.domain, w_ext.suffix])
        # ca_ext = tld.extract(ca)
        # tld_ca = ".".join([ca_ext.domain, ca_ext.suffix])
        # isHTTPS_w = isHTTPS(w)
        # SAN_w = getSAN(w)
        # SOA_w = getSOA(w)
        # SOA_ca = getSOA(ca)

        # check if tld matches
        # if tld_w == tld_ca:
        #     ca_type = DEP_TYPE.PRIVATE
        # # check if HTTPS and tld(ca) in SAN(w)
        # elif (isHTTPS_w and tld_ca in SAN_w):
        #     ca_type = DEP_TYPE.PRIVATE
        # # check if SOA(ca) != SOA(w)
        # elif (SOA_ca != SOA_w):
        #     ca_type = DEP_TYPE.THIRD

        
        # if ca_type == DEP_TYPE.UNKNOWN:
        #     final = 'UNKNOWN'
        # elif ca_type == DEP_TYPE.PRIVATE:
        #     final = 'PRIVATE'
        # else:
        #     final = 'THIRD'

        # out.write(f"{w} {final} {host}\n")
    f.close()
    out.close()
        