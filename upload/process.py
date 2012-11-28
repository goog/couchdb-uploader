import couchdb
from  nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import nltk
from datetime import datetime
import subprocess
from topia.termextract import extract
#import tika
#tika.initVM()
#from tika import parser

def handler(file,meta):
## return the file url 
    couch = couchdb.Server('http://localhost:5984/')
    try:
        db=couch['test']
    except:
        db = couch.create('test')
    # file : InMemoryUploadedFile
    fw = open('tempfile','w')
    fw.write(file.read())
    fw.close()

    ##### to parse the file ######
    try:
        text = subprocess.check_output("java -jar tika-app-1.2.jar -t tempfile", shell=True)
    except:
        text = ''

    #metadata = subprocess.check_output("java -jar tika-app-1.2.jar -j tempfile", shell=True)

    dt = datetime.now()
    meta['created'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    # initialize the downloaded time 
    meta['cnt'] = 0
    
    if text:
	if len(text)<=400:
	    meta['begin']=text    
	else:
	    meta['begin']=text[:400]
        ## to do a better way
        extractor = extract.TermExtractor()
        if extractor(text):
            keywords=[];cnt=0
	    extractor(text).sort(key=lambda tup: tup[1],reverse=True)
	    for i in extractor(text):
                keywords.append(i[0])
		cnt+=1
		if cnt==5:
		    break
            print cnt,keywords
            meta['keyword'] =','.join(keywords)
    
    id = db.save(meta)[0]
    file.seek(0)
    db.put_attachment(meta,file)
    # the note and share url 
    #return "http://127.0.0.1:5984/test/"+id+"/"+file.name,id
    return id
    
# text analysis
def analysis(text):

    tokens=[]
    for t in sent_tokenize(text):
        tokens.extend(word_tokenize(t))
    text = nltk.Text(tokens)
    fdist = nltk.FreqDist(text)
    vocabulary = fdist.keys()
    return ' '.join(vocabulary[:50])

    

# del a document from couchdb
def del_doc(id):
    couch = couchdb.Server('http://localhost:5984/')
    try:
        db=couch['test']
    except:
        db = couch.create('test')
    del db[id]



#f= open('test.pdf')
#handler(f,'a','b')
