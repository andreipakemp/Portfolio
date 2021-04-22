import inspect

def displayInConsole(objectsClass, staticMethod = False):
    frame = inspect.stack()[1]
    filename = frame.filename
    
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    methodName = calframe[1][3]
    
    if not staticMethod:
        className = objectsClass.__class__.__name__
    else:
        className = objectsClass
    print(filename.replace("home/andrei/share/workspace/Portfolio/",""))
    print(className + ' ' + methodName + '()')
    
def getSessionMsg(view):
    isMsg = False
    msg = ''
    
    if view.request.session.get('msg'):
        msg = view.request.session['msg']
        view.request.session['msg'] = None
        
    return isMsg, msg