import couchdb
from  nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import nltk
from datetime import datetime
import subprocess
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
        text = subprocess.check_output("java -jar tika-app-1.2.2.jar -t tempfile", shell=True)
    except:
        text = ''

    #metadata = subprocess.check_output("java -jar tika-app-1.2.2.jar -j tempfile", shell=True)

    dt = datetime.now()
    meta['created'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    if text:
        meta['fre'] = analysis(text)
    
    id = db.save(meta)[0]
    file.seek(0)
    db.put_attachment(meta,file)
    # the note and share url 
    #return "http://127.0.0.1:5984/test/"+id+"/"+file.name,id
    return id
    
# text analysis
def analysis(text):
    #TODO  add some meta data
    tokens=[]
    for t in sent_tokenize(text):
        tokens.extend(word_tokenize(t))
    text = nltk.Text(tokens)
    fdist = nltk.FreqDist(text)
    vocabulary = fdist.keys()
    return ''.join(vocabulary[:50])

    

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
