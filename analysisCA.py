from enum import Enum
import tldextract as tld
from resolveSOA import getSOA
import sys
from utils import DEP_TYPE

ca_map = {'Amazon': 'amazontrust.com', 'Google Trust Services LLC': 'pki.goog', 'Entrust, Inc.': 'entrust.com', 
            'DigiCert Inc': 'digicert.com', 'Sectigo Limited': 'sectigo.com', 'COMODO CA Limited': 'comodoca.com', 'Microsoft Corporation': 'microsoft.com',
            'Let\'s Encrypt': 'letsencrypt.org', 'Cloudflare, Inc.': 'cloudflare.com', 'GlobalSign nv-sa': 'globalsign.com', 'ZeroSSL': 'zerossl.com'}

def main():
    f = open('certificates_line.txt', 'r')
    # f = ["aan.amazon.com/Issuer: ((('countryName', 'US'),), (('organizationName', 'Amazon'),), (('commonName', 'Amazon RSA 2048 M01'),))/Subject: ((('commonName', 'aan.amazon.com'),),)/SubjectAltName: (('DNS', '*.taboola.com'), ('DNS', '*.taboolasyndication.com'), ('DNS', 'taboola.com'), ('DNS', 'taboolasyndication.com'))"]
    out = open(sys.argv[1], 'w')
    out_stats = open(sys.argv[2], 'w')
    # print(f)
    ca_counts = {}
    for line in f:
        print(line)
        if 'Error' in line:
            if 'CERTIFICATE_VERIFY_FAILED' in line:
                out.write(f"{'failed'}\n")
            else:
                out.write(f"{'address_error'}\n")
            continue
        line = line.split('/')
        w = line[0].strip(':')
        ca_line = line[1]
        ca_type = DEP_TYPE.UNKNOWN
        isHTTPS = True
        host = ''
        sub = line[3].split(':')[1].replace('(', '').replace(')', '').replace('\'', '').replace(' ', '')
        SANs = [x for x in sub.split(',') if 'DNS' not in x]
        ca_name = line[1].partition('organizationName\', ')[2].split(')')[0].strip('\'')
        print(w)
        print(ca_name)
        print(SANs)
        
        
        # things we need:
        # -tld(w)
        # -tld(ca_url)
        # -isHTTPS(w)
        # -SAN(w)
        # -SOA(w)
        # -SOA(ca_url)

        w_ext = tld.extract(w)
        tld_w = ".".join([w_ext.domain, w_ext.suffix])
        tld_ca = ''
        if ca_name in ca_map.keys():
            tld_ca = ca_map[ca_name]
        if ca_name in ca_counts.keys():
            ca_counts[ca_name] += 1
        else:
            ca_counts[ca_name] = 1
        SOA_w = getSOA(w)
        SOA_ca = getSOA(ca_name)
        inSAN = [tld_ca in SAN for SAN in SANs]
        print(inSAN)

        #check if tld matches
        if tld_w == tld_ca:
            ca_type = DEP_TYPE.PRIVATE
            print(f"matched {tld_w} and {tld_ca}")
        # check if HTTPS and tld(ca) in SAN(w)
        elif (isHTTPS and any(inSAN)):

            ca_type = DEP_TYPE.PRIVATE
        # check if SOA(ca) != SOA(w)
        elif (SOA_ca != SOA_w):
            ca_type = DEP_TYPE.THIRD

        
        if ca_type == DEP_TYPE.UNKNOWN:
            final = 'UNKNOWN'
        elif ca_type == DEP_TYPE.PRIVATE:
            final = 'PRIVATE'
        else:
            final = 'THIRD'

        out.write(f"{w}:{final}:{ca_name}\n")
    for key, value in ca_counts.items():
        out_stats.write(f"{key}:{value}\n")
    out_stats.close()
    f.close()
    out.close()
        

if __name__ == '__main__':
    main()