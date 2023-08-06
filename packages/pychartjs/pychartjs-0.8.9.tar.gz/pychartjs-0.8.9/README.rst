A smartClient wrapper
=====================

to use (with caution), suppose that you are using bottle and beaker::

from smartClient import SessionManager


@app.route('/')
def root():
    # get the client session
    clientSession = request.environ.get('beaker.session')

    # get the session manager
    sm = SessionManager(clientSession, clientInfo=clientInfo)

    # get the HTML page
    page = sm.getPage()

    # clear session
    page.clearSession()

    # build the page
    page.addComponent(getLoginPage(page))

    # build the response body
    response.body = page.getMainPage()

    # update the client sesssion
    page.updateSession()
    clientSession.save()

    return response



from smartClient import VerticalLayout, HorizontalLayout, KeyboardManager, ReplyClick, ActionUrl, Validator
from smartClient import Label, DateField, EditField, CheckBox, RadioGroup, SelectField, PasswordField, Button, Link
from smartClient import TextArea, Header, Spacer, RichEditor, ListGrid, DataSource, FileUpload, Window, ViewLoader
from smartClient import SectionStack, MainMenu, MenuLink, HTMLPane, Canvas


def getLoginPage(page):
    login = Label()
    login.setProperty('contents','login')
    login.setProperty('height',40)

    user = EditField()
    user.setProperty('title','user','fields')
    user.setProperty('value','','fields')
    user.setProperty('autoFocus','true')
    user.setProperty('autoFocus','true','fields')
    user.transformValue = 'function(form, item, value, oldValue) {return value.toUpperCase()}'

    password = PasswordField()
    password.setProperty('title','password','fields')
    password.setProperty('value','','fields')

    v = Validator()
    v.setCondition("return value == 'xxx';")
    password.addValidator(v)

    spacer = Spacer()
    spacer.setProperty('width', '*')
    spacer0 = Spacer()
    spacer0.setProperty('width', '*')
    spacer1 = Spacer()
    spacer1.setProperty('width', '5%')
    spacer2 = Spacer()
    spacer2.setProperty('height', '5%')

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('verifyPassword')
    strObj = '{"object":"User"}'
    actionURL.setObject(strObj)
    actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    check = Button(actionUrl=actionURL)
    check.setProperty('title', 'login')
    check.setProperty('width', 100)
    check.setProperty('height', 40)
    #check.setProperty('saveOnEnter', 'true')
    keyboardManager = page.keyboardManager
    keyboardManager.addEventList2Component(check, ['%s.setFocus(true);', '%s.click();'])


    v1 = VerticalLayout()
    h0 = HorizontalLayout()
    h1 = HorizontalLayout()
    v1.setProperty('width', 400)
    v1.setProperty('membersMargin', 5)
    v1.setProperty('layoutMargin', 20)


    v1.addComponent(spacer2)
    v1.addComponent(login)
    v1.addComponent(user)
    v1.addComponent(password)
    #v1.addComponent(spacer2)
    v1.addComponent(h1)

    h1.addComponent(spacer)
    h1.addComponent(check)

    h0.addComponent(spacer0)
    h0.addComponent(v1)
    h0.addComponent(spacer1)

    return h0



