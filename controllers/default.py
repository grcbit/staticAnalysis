# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import os
import zipfile
import shutil
import axmlparserpy.axmlprinter as axmlprinter
import xml.dom.minidom
import xml.etree.ElementTree as ET
#import time
from datetime import datetime, date, time
import base64
demo = True

# ---- example index page ----
def index():
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))
    return dict()

def licencia():
    return dict()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires_login()
def aplicacion():
    db.applications.id.readable = False
    db.applications.appApkExtract.writable = False
    db.applications.appDex2Jar.writable = False
    db.applications.appDex2Smali.writable = False
    fields = (db.applications.appName, db.applications.appVersion, db.applications.appDesc, db.applications.appDate, db.applications.appFile, db.applications.codeFile)

    links = [lambda row: A('Decompile',_class='button btn btn-warning',_href=URL("default","decompile", args=[row.id, row.appFile, row.appName, row.appVersion, row.codeFile])), lambda row:A('Manifest XML', _class='button btn btn-success', _href=URL('default','manifestAnalyse', args=[row.id, row.appFile, row.appName, row.appVersion])), lambda row:A('JD GUI', _class='button btn btn-primary', _href=URL('default','jdiGui')), lambda row: A('Static Analysis',_class='button btn btn-info',_href=URL("default","staticAnalysis", args=[row.id, row.appFile, row.appName, row.appVersion, row.codeFile]))]

    if demo == False:
        if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
            form = SQLFORM.grid(db.applications, user_signature=False, searchable=True, create=True, editable=True, deletable=True, links=links, fields=fields, maxtextlength=500, paginate=10)
        else:
            form = SQLFORM.grid(db.applications, user_signature=False, searchable=True, create=False, editable=False, deletable=False, fields=fields, maxtextlength=500, paginate=10)
    elif demo == True:
        form = SQLFORM.grid(db.applications, user_signature=False, searchable=True, create=True, editable=True, deletable=True, links=links, fields=fields, maxtextlength=500, paginate=10)
    form = SQLFORM.grid(db.applications, user_signature=False, links=links, fields=fields, maxtextlength=500, paginate=10)
    return dict(form = form)

@auth.requires_login()
def decompile():
    #-------------
    #Descomprimir
    #-------------
    #request.args[2] --> appName
    #request.args[3] --> appVersion
    apk_path1 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])
    apk_path2 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/apkExtract/"
    apk_path3 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/zipExtract/"
    try:
        shutil.rmtree(apk_path1)
        shutil.rmtree(apk_path2)
        shutil.rmtree(apk_path3)
    except:
        pass
    os.mkdir(apk_path1)
    os.mkdir(apk_path2)
    os.mkdir(apk_path3)
    #---------------------------------------
    #Valida si existe un usuario APK y/o ZIP
    #---------------------------------------
    if len(request.args[1])>0 or len(request.args[4])>0:
        if len(request.args[1])>0:
            try:
                apk_file = zipfile.ZipFile( str(request.folder)+"/uploads/"+str(request.args[1]) )
                apk_file.extractall(apk_path2)
            except:
                t='alert alert-warning'
                msg = T('ERROR: APK decompress failed')
                redirect(URL('default', 'aplicacion', vars=dict(msg=msg, t=t)))
                pass
        if len(request.args[4])>0:
            try:
                apk_file = zipfile.ZipFile( str(request.folder)+"/uploads/"+str(request.args[4]) )
                apk_file.extractall(apk_path3)
            except:
                t='alert alert-warning'
                msg = T('ERROR: ZIP decompress failed')
                redirect(URL('default', 'aplicacion', vars=dict(msg=msg, t=t)))
                pass
    else:
            t='alert alert-warning'
            msg = T('ERROR: Not APK/ZIP file found')
            redirect(URL('default', 'aplicacion', vars=dict(msg=msg, t=t)))
            pass
    #----------
    #dex2jar
    #----------
    apk_path1 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/dex2jar/"
    try:
        shutil.rmtree(apk_path1)
    except:
        pass
    try:
        os.mkdir(apk_path1)
        dex_ex = str(request.folder)+"/static/appFiles/dex2jar-2.0/./d2j-dex2jar.sh --force --output "+str(apk_path1)+" "+str(apk_path2)+"classes.dex"
        os.system(dex_ex)
        db(db.applications.id==request.args[0]).update(appDex2Jar='T') 
    except:
        t='alert alert-warning'
        msg = T('dex2jar ERROR')
        redirect(URL('default', 'aplicacion', vars=dict(msg=msg, t=t)))
        pass
    #----------
    #dex2smali
    #----------
    num = db((db.applications.id==request.args[0]) & ( (db.applications.appApkExtract=='F') | (db.applications.appApkExtract==False))).count()
    if num == 1:
        t='alert alert-danger'
        msg = T('You must first run APK Extract')
        redirect(URL('default','applications', vars=dict(msg=msg, t=t)))
    apk_path1 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/dex2smali/"
    apk_path2 =  str(request.folder)+"/uploads/"+str(request.args[1])
    try:
        shutil.rmtree(apk_path1)
    except:
        pass
    try:
        os.mkdir(apk_path1)
        dex_ex = str(request.folder)+"/static/appFiles/dex2jar-2.0/./d2j-dex2smali.sh --force --output "+str(apk_path1)+" "+str(apk_path2)
        os.system(dex_ex)
        db(db.applications.id==request.args[0]).update(appDex2Smali='T') 
    except:
        t='alert alert-danger'
        msg = T('dex2smali ERROR')
        redirect(URL('default', 'aplicacion', vars=dict(msg=msg, t=t)))
        pass
    t = 'alert alert-success'
    msg = T('Decompile executed')
    redirect(URL('default', 'aplicacion', vars=dict(msg=msg, t=t)))

@auth.requires_login()
def staticAnalysis():
    #------------------------
    #Para analizar codigo APK
    #------------------------
    if len(request.args[1])>0:
        dex2jarCheck = db(db.applications.id==request.args[0]).select(db.applications.appDex2Jar).first().appDex2Jar
        dex2smaliCheck = db(db.applications.id==request.args[0]).select(db.applications.appDex2Smali).first().appDex2Smali
        apk_path2 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/staticAnalisys/"
        #-----------------------------
        #Para analizar el codigo JAVA
        #-----------------------------
        if dex2jarCheck == True:
            apk_path1 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/dex2jar/"
            html_file = "java"+str(request.args[2])+str(request.args[3])+str(base64.b64encode(str(datetime.now())))+".html"
            t = 'alert alert-success'
            msg = T('java Static analysis executed')
            tipo="java"
            db.staticAnalysis.insert(aplicationsId=request.args[0], staticAnalysisFileId=html_file, staticAnalysisDate=datetime.now(), staticAnalysisFileType=tipo)
            staticAnalysisRender(request.args[0], apk_path1, apk_path2, html_file, tipo)
        else:
            t='alert alert-danger'
            msg = T('Analysis was not done. You must first execute decompile')
        #-----------------------------
        #Para analizar el codigo SMALI
        #-----------------------------
        if dex2smaliCheck == True:
            apk_path1 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/dex2smali/"
            html_file = "smali_"+str(request.args[2])+str(request.args[3])+str(base64.b64encode(str(datetime.now())))+".html"
            t = 'alert alert-success'
            msg = T('smali Static analysis executed ') + " . " + msg
            tipo="smali"
            db.staticAnalysis.insert(aplicationsId=request.args[0], staticAnalysisFileId=html_file, staticAnalysisDate=datetime.now(), staticAnalysisFileType=tipo)
            staticAnalysisRender(request.args[0], apk_path1, apk_path2, html_file, tipo)
        else:
            t='alert alert-danger'
            msg = T('Analysis was not done. You must first execute decompile')
    #------------------------
    #Para analizar codigo ZIP
    #------------------------
    if len(request.args[4])>0:
        codigo = db(db.applications.id==request.args[0]).select(db.applications.codeFile).first().codeFile
        #if codigo:
        #apk_path1 = str(request.folder)+"/uploads/"+str(codigo)
        apk_path1 = str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/zipExtract/"
        #apk_path1 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/dex2jar/"
        #apk_path2 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])
        apk_path2 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/staticAnalisys/"
        #try:
        #    os.mkdir(apk_path2)
        #except:
        #    pass
        #apk_path2 =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/staticAnalisys/"
        try:
            os.mkdir(apk_path2)
        except:
            pass
        html_file = "codigo"+str(request.args[2])+str(request.args[3])+str(base64.b64encode(str(datetime.now())))+".html"
        t = 'alert alert-success'
        msg = T('code analysis executed ')
        tipo="source"
        db.staticAnalysis.insert(aplicationsId=request.args[0], staticAnalysisFileId=html_file, staticAnalysisDate=datetime.now(), staticAnalysisFileType=tipo)
        staticAnalysisRender(request.args[0], apk_path1, apk_path2, html_file, tipo)
    redirect(URL('default','aplicacion', vars=dict(msg=msg, t=t) ))

@auth.requires_login()
def staticAnalysisRender(appId, apk_path1, apk_path2, html_file, tipo):
    resultado = ''
    lista_palabras = []
    lista_palabras1 = db(db.applications.id==appId).select(db.applications.appWords)

    for i in lista_palabras1:
        for x in  str(str(i.appWords).replace(' ','')).split(','):
            lista_palabras.append(x)

    try:
        os.mkdir(apk_path2)
    except:
        pass

    apk_path2 =  apk_path2+str(html_file)

    result = open(apk_path2, 'w')
    numero_linea = 0

    if tipo=="java" or tipo=="smali":
        for root, dirs, files in os.walk(apk_path1):
            for name in files:
                files = os.path.join(root,name)
                f = open(files, 'r')
                for linea in f:
                    numero_linea = numero_linea + 1
                    for palabra in lista_palabras:
                        if (linea.lower()).find(palabra.lower())!=-1:
                            linea_completa = str(linea).replace('<','')
                            linea = linea[linea.lower().find(palabra):]
                            resultado = resultado+'<tr>'
                            resultado = resultado+'<td>'
                            resultado = resultado+str(palabra)
                            resultado = resultado+'</td>'
                            resultado = resultado+'<td>'
                            resultado = resultado+str(os.path.join(root,name))
                            resultado = resultado+'</td>'
                            resultado = resultado+'<td>'
                            resultado = resultado+str(numero_linea)
                            resultado = resultado+'</td>'
                            resultado = resultado+'<td>'
                            resultado = resultado+str(linea_completa).replace('>','')
                            resultado = resultado+'</td>'
                            resultado = resultado+'</tr>'
                f.close()

    if tipo=="source":
        #f = open(apk_path1, 'r')
        for root, dirs, files in os.walk(apk_path1):
            for name in files:
                files = os.path.join(root,name)
                f = open(files, 'r')
                for linea in f:
                    numero_linea = numero_linea + 1
                    for palabra in lista_palabras:
                        if (linea.lower()).find(palabra.lower())!=-1:
                            linea_completa = str(linea).replace('<','')
                            linea = linea[linea.lower().find(palabra):]
                            resultado = resultado+'<tr>'
                            resultado = resultado+'<td>'
                            resultado = resultado+str(palabra)
                            resultado = resultado+'</td>'
                            resultado = resultado+'<td>'
                            #resultado = resultado+str(apk_path1)
                            resultado = resultado+str(os.path.join(root,name))
                            resultado = resultado+'</td>'
                            resultado = resultado+'<td>'
                            resultado = resultado+str(numero_linea)
                            resultado = resultado+'</td>'
                            resultado = resultado+'<td>'
                            resultado = resultado+str(linea_completa).replace('>','')
                            resultado = resultado+'</td>'
                            resultado = resultado+'</tr>'
                f.close()

    result.write('<html>')
    result.write('<head>')
    
    result.write('<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css"> ')
    result.write('<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/1.6.2/css/buttons.dataTables.min.css"> ')
    result.write('<style type="text/css" class="init"></style> ')
    result.write('<script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script> ')
    result.write('<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>')
    result.write('<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/buttons/1.6.2/js/dataTables.buttons.min.js"></script> ')
    result.write('<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/buttons/1.6.2/js/buttons.flash.min.js"></script> ')
    result.write('<script type="text/javascript" language="javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js"></script>')
    result.write('<script type="text/javascript" language="javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js"></script> ')
    result.write('<script type="text/javascript" language="javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js"></script> ')
    result.write('<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/buttons/1.6.2/js/buttons.html5.min.js"></script> ')
    result.write('<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/buttons/1.6.2/js/buttons.print.min.js"></script> ')
    result.write('</head>')

    result.write('<body>')
    result.write(' <script> $(document).ready(function() {$("#example").DataTable( { lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]], scrollY: "500px", scrollX: true, scrollCollapse: true, columnDefs: [{ width: 70, targets: [1,3] }], dom: "Bfrtip", buttons: [ "copy","csv","excel","pdf","print"]  }); }); </script> ')
    result.write('<h3>')
    result.write('Application name: '+str(request.args[2]))
    result.write('</h3>')
    result.write('<h6>')
    result.write('<table id="example" class="display" style="width:100%; font-size:11">')

    result.write('<thead>')
    result.write('<tr> <td>Keyword</td> <td>File Path</td> <td>Line Number</td> <td>Code</td> </tr>')
    result.write('</thead>')
    result.write('<tbody>')
    result.write(str(resultado))
    result.write('</tbody>')

    result.write('</table>')
    result.write('</h6>')

    result.write('</body>')
    result.write('</html>')

    result.close()

    stream = open(apk_path2, 'rb')
    db( (db.staticAnalysis.aplicationsId==appId) & (db.staticAnalysis.staticAnalysisFileId==html_file)).update(staticAnalysisFile=stream, staticAnalysisKeyWords=lista_palabras)
    stream.close()

@auth.requires_login()
def staticAnalysisResults():
    apk_path =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/staticAnalisys/"

    f = {}
    i = 0
    for root, dirs, files in os.walk(apk_path):
        for name in files:
            path = str(apk_path)+str(name)
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
            f[i, 0]=str(name)
            f[i, 1]=time.ctime(ctime)
            i=i+1
    return dict(f=f, app=request.args[2], version=request.args[3], path=apk_path) 

@auth.requires_login()
def resultado():
    #file name
    db.staticAnalysis.staticAnalysisFileId.readable = False
    form = SQLFORM.grid(db.staticAnalysis, user_signature=True, create=False, deletable=True, editable=False, maxtextlength=500, paginate=10)
    return dict(form=form)

@auth.requires_login()
def jdiGui():
    #jdi = str(request.folder)+"/uploads/jre1.8.0_121/bin/java -jar "+str(request.folder)+"/uploads/jd-gui-1.6.5.jar"
    jdi = str(request.folder)+"/static/appFiles/jre1.8.0_121/bin/java -jar "+str(request.folder)+"/static/appFiles/jd-gui-1.6.5.jar"
    os.system(jdi)
    redirect(URL('default', 'aplicacion'))

@auth.requires_login()
def manifestAnalyse():
    try:
        apkFile =  str(request.folder)+"/uploads/"+str(request.args[2])+str(request.args[3])+"/apkExtract/AndroidManifest.xml"
        ap = axmlprinter.AXMLPrinter(open(apkFile,'rb').read())
        buff1 = xml.dom.minidom.parseString(ap.getBuff()).toxml()
        buff2 = xml.dom.minidom.parseString(ap.getBuff()).toprettyxml()
        root = ET.fromstring(str(buff1))
        return dict(buff=buff1, root=root)
    except:
        t='alert alert-danger'
        msg = T('You must first execute APK Extract')
        redirect(URL('default', 'aplicacion', vars=dict(msg=msg, t=t)))
