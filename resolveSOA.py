import sys
import subprocess

def extractSOA(dig):
    if 'AUTHORITY SECTION' in dig:
        ans = dig.partition('AUTHORITY SECTION')[2]
    elif 'ANSWER SECTION' in dig:    
        ans = dig.partition('ANSWER SECTION')[2]
    else:
        return None
    ans = ans.split('\n')
    ans = [a.split('SOA\t')[1] for a in ans if "SOA" in a]
    return ans

def getSOA(url):
    dig = subprocess.check_output(['dig', 'SOA', url])
    dig = str(dig, 'utf-8')
    extracted = extractSOA(dig)
    return extracted


def main():
    line1 = 'calendar.google.com'
    line2 = 'ns2.google.com'
    print(getSOA(line1))
    print(getSOA(line2))

if __name__ == '__main__':
    main()