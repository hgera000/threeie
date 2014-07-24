from __future__ import print_function
from BeautifulSoup import BeautifulSoup
import os,pdb,re,io
from collections import defaultdict


source_folder = "/home/hgera000/threeie/html/"
studies = io.open('/home/hgera000/threeie/data/studies.txt','w',encoding='utf8')
authors = io.open('/home/hgera000/threeie/data/authors.txt','w',encoding='utf8')
sectors = io.open('/home/hgera000/threeie/data/sectors.txt','w',encoding='utf8')
subgroups = io.open('/home/hgera000/threeie/data/subgroups.txt','w',encoding='utf8')
designs = io.open('/home/hgera000/threeie/data/designs.txt','w',encoding='utf8')


for fname in sorted(os.listdir(source_folder)):
    d = defaultdict(list); #new data dictionary
    print ('Parsing file named %s' % fname)
    with open("%s%s" % (source_folder,fname),'r') as f:
        soup = BeautifulSoup(f.read())
        d['title'] = [soup.article.h1.text.strip(),]
        pdb.set_trace()
        d['source'] = soup.find('h2',text=re.compile('Publication Source')).findNext('p',text=re.compile('Available From:')).rstrip('Available From:').strip().split(', ')
        if len(d['source'])==2:
            d['source'] = d['source']+["NULL","NULL","NULL"]
        if len(d['source'])==3:
            d['source'] = d['source']+["NULL","NULL",]
        if len(d['source'])==4:
            d['source'] = d['source']+["NULL",]

        
        d['link'] = [soup.find('a',{'class':"button evidence_link"})['href'].strip(),]
        meta = soup.find('section', {'class': 'evidence_meta'})

        dt = meta.findAll('dt')
        dd = meta.findAll('dd')
        for i in range(0,len(dt)):
            if dt[i].text == 'Authors':
                d[dt[i].text.lower().strip()] = re.split(',| and ', dd[i].text.strip())
            else:
                d[dt[i].text.lower().strip()] = dd[i].text.strip().split(', ')

        details = soup.findAll('section',{'class': 'summary_item'})
        for det in details:
            d[det.h2.text.lower()] = det.nextSibling.text.strip()

        if 'methodology' not in d:
            d['methodology'] = "NULL"
        if 'main findings' not in d:
            d['main findings'] = "NULL"
        if 'about this impact evaluation' not in d:
            d['about this impact evaluation'] = "NULL"

        stdout1 = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s";

        print(stdout1 % (fname.strip('.html'),d['title'][0],d['status'][0],d['country'][0],d['region'][0],d['source'][0],d['source'][1],";".join(d['source'][2:]),d['link'][0],d['gender focus'][0], d['methodology'], d['main findings'], d['about this impact evaluation']),file=studies)

        stdout2 = "%s|%s";

        for l in d['authors']:
            print(stdout2 % (fname.strip('.html'),l),file=authors)

        for l in d['sector']:
            print(stdout2 % (fname.strip('.html'),l),file=sectors)

        for l in d['selected sub-groups']:
            print(stdout2 % (fname.strip('.html'),l),file=subgroups)

        for l in d['evaluation designs']:
            print(stdout2 % (fname.strip('.html'),l),file=designs)

authors.close()
sectors.close()
subgroups.close()
designs.close()
studies.close()


