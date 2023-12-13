import subprocess
import sys
import tldextract

def extractns(dig_resp):
        ans = dig_resp.partition('ANSWER SECTION')[2]
        ans = ans.split('\n')
        ans = [a.split('NS\t',1)[1][:-1] for a in ans if 'NS' in a]
        return ans



def main():
    filename = sys.argv[1]
    output = sys.argv[2]

    # print("opening" + filename)

    f = open(filename, 'r')
    out = open(output,"w")

    for line in f:
        try:
            if 'local' in line:
                continue
            line = line.strip('\n').split()[1]
            dig = subprocess.check_output(['dig', line])
            dig = str(dig,"utf-8")
            if("NXDOMAIN" in dig):
                # print('nx')
                out.write((f"{line}:NXDOMAIN\n"))
            elif("SERVFAIL" in dig):
                # print ("sf")
                dig = subprocess.check_output(['dig', "@8.8.8.8",line])
                dig = str(dig,"utf-8")
                if("NXDOMAIN" in dig):
                    out.write((f"{line}:NXDOMAIN\n"))
                if("SERVFAIL" in dig):
                    out.write(f"{line}:SERVFAIL\n")
            else:
                # print('made it!')
                dig = subprocess.check_output(['dig', "ns","@8.8.8.8",line])
                dig = str(dig,"utf-8")

                if("ANSWER: 0" in dig):
                    tld = tldextract.extract(line)
                    domain = tld.domain + "." + tld.suffix
                    dig = subprocess.check_output(['dig', "ns","@8.8.8.8",domain])
                    dig = str(dig,"utf-8")
                    ans = extractns(dig)
                    ans = set(ans)
                    out.write(f"{line}:")
                    for val in ans:
                        out.write(f" {val}")
                    out.write("\n")

        except subprocess.CalledProcessError as e:
            pass

    


if __name__ == '__main__':
    main()