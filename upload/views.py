from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from upload.forms import UploadFileForm,RegisterForm,ProfileForm
from upload.process import handler,del_doc
from upload.activation import activate_user
from upload.models import UserProfile
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from couchdb import Server
from threading import Thread
from activation import send_activation
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required


# set up couchdb to display docs
SERVER = Server('http://127.0.0.1:5984')
if (len(SERVER) == 0):
    SERVER.create('test')
db = SERVER['test']

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/upload/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
	    user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
###activate the account
            user.is_active = False
            thread = Thread(target=send_activation,  args=[user])
            thread.setDaemon(True)
            thread.start()
	    user.save()
            userprofile = UserProfile(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'],favorite=form.cleaned_data['favorite'])
            userprofile.save()
            
            return render_to_response("to-activate.html",  {'username': form['username'],'email':form['email'], },context_instance=RequestContext(request))
	else:
	    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = RegisterForm()
 
    return render_to_response("register.html",  {'form': form},context_instance=RequestContext(request))

def activate(request):
    # use a GET method
    user = request.GET.get('user')
    code = request.GET.get('code')
 
    if activate_user(user,code):
        return render_to_response('index.html', {"activateMessage": "congratulations! you are activated now."},
			    context_instance=RequestContext(request))
    else:
        raise Http404

#####  uploader----------------------------------------------------------------------------
def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

##
def uploadfile(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            #print "post",request.POST
            f = request.FILES.get('file')   
	    meta = {}
            meta['desc'] = request.POST.get('desc','')
	    meta['tag'] = request.POST.get('tag','')
	    meta['pri'] = request.POST.get('pri','')
            meta['user'] = request.user.username
            id = handler(f,meta)  
            # Extend server-side upload handler to return a JSON response
            if f.name.endswith("pdf") or f.name.endswith("PDF"):
	        thumbnail_url = settings.MEDIA_URL + "img/" +"pdf.png"
	    else:
	        thumbnail_url = ''
             #data = [{'name': f.name, 'url': reverse('doc',args=[id]), 'thumbnail_url':thumbnail_url, 'delete_url': reverse('idel',args=[id]), 'delete_type': "DELETE"}]
	    data = [{'name': f.name, 'url': reverse('doc',args=[id]), 'thumbnail_url':thumbnail_url}]
            #print data
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response 
        else:
            #form = UploadFileForm()
            #return render_to_response('index.html', {'form': form}, context_instance=RequestContext(request))
	    return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        return render_to_response('preupload.html')
	
    
    
def deleteDoc(request,id):
    del_doc(id)
    print args
    if request.is_ajax():
           response = JSONResponse(True, {}, response_mimetype(self.request))
           response['Content-Disposition'] = 'inline; filename=files.json'
           return response
	

	    
# show singal document info . if pri is 1, public
def detail(request,id):
    try:
        doc = db[id]
    except:
        raise Http404
    if request.method == "POST":
        # relax to do multiple fields
	print request.POST
        for key in request.POST.keys():
            if key != "csrfmiddlewaretoken" and request.POST.get(key,''):
                doc[key] = request.POST.get(key)
        db[id] = doc
    setattr(doc, "attachment", doc['_attachments'].keys()[0])
    return render_to_response('detail.html',{'row':doc},
			context_instance=RequestContext(request))

def ShowProfile(request,username):
    data=model_to_dict(UserProfile.objects.get(user_id=User.objects.get(username=username).id))
    del data['id']
    object = ProfileForm(data)

    ######## view function ########
    '''map_fun =  'function(doc) {if(doc.user=="' + username + '") emit(doc.id,null);}' '''
    list = []
    for row in db.view('_design/example/_view/detail',key = username):
        list.append(row.id)
    ## TODO 
    ## show more infos 
    return render_to_response('profile.html', {'object': object , 'list': list },
		context_instance=RequestContext(request))


def goto(request,id,filename):
   return HttpResponseRedirect('http://127.0.0.1:5984/test/'+id+'/'+filename)
   



