########
#License	GNU/GPL 
#Author Beto Alves
#######

import os
import sys
import wx
from xml.dom import minidom

Path_main =  sys.path[0]
###################################################
global grouplist 
global xmldoc 
xmldoc = minidom.parse(Path_main+'/upaupa.xml')
grouplist = xmldoc.getElementsByTagName('group')
###################################################


###################################################
total_groups = 0
for groups in grouplist:
	group = groups.getAttribute("name")
	total_groups += 1
###################################################

###################################################
def getUserPass(hostname):
	for groups in grouplist:
		pcs = groups.getElementsByTagName("server")
		for pc in  pcs:
			nome = pc.getAttribute("name")
			if hostname == nome:
				ip = pc.getAttribute("host")
				user = pc.getAttribute("user")
				passwd = pc.getAttribute("password")
				return user,passwd,ip
###################################################

#######################################################
def newEterm(hostname):
    user,passw,ip = getUserPass(hostname)
    #execute =" konsole -e sshpass -p %s ssh -l %s %s &" %(passw,user,ip)
    execute =" Eterm -e sshpass -p %s ssh -l %s %s &" %(passw,user,ip)
    os.system(execute)
#######################################################

#######################################################
class Frame(wx.Frame):
	def __init__(self, *args, **kwargs):
		self.aux = 0
		wx.Frame.__init__(self, *args, **kwargs)
		self.p1 = wx.Panel(self)

	def text_return(self, event):
		hostname = event.GetString()
		newEterm(hostname)
		self.st.Destroy()
		app.add()

	def addCombo(self,lst,names):
		try:
			aux = self.st.GetSize()
			inte = int(aux[0])
			inte += self.aux
		except:
			inte = 0
		self.aux = inte
        	self.st = wx.ComboBox(self.p1, -1,value=names,name=names,size=(130,-1),pos=(inte, 0), choices = lst, style=wx.CB_DROPDOWN)
        	self.st.Bind(wx.EVT_COMBOBOX, self.text_return)

#######################################################

#######################################################
class Window(wx.App):
    def OnInit(self):
        mysize = 130*int(total_groups)
        self.frame = Frame(None, -1, 'UPA UPA',size = (mysize,23))
        self.SetTopWindow(self.frame)
        self.frame.Center()
        self.frame.Show()
        self.frame.SetAutoLayout(True)
        return 1

    def add(self):

		for groups in grouplist:
			array = []
			group = groups.getAttribute("name")
			pcs = groups.getElementsByTagName("server")
			for pc in  pcs:
				nome = pc.getAttribute("name")
				array.append(nome)
			self.frame.addCombo(array,group)
#######################################################


#####################################################
if __name__ == "__main__":
    app = Window(0)
    app.add()
    app.MainLoop()
####################################################
