import requests,io,pdb

save_folder = "/home/hgerard/threeie/html/"
base_url = "http://www.3ieimpact.org/en/evidence/impact-evaluations/details/"

for pid in range(600,1001): 
    #pdb.set_trace()
    html = requests.get("%s%d" % (base_url,pid))
    with io.open("%s%d.html" % (save_folder,pid), 'w', encoding='utf8') as f:
        f.write(html.text)
