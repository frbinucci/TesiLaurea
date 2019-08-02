import importlib.util
import configparser
import re
import sys
import random

#___________________________________________________________________________
'''In questa sezione dello script ci si occupa di recuperare le informazioni
necessarie per ottenere il percorso assoluto di tutti i files utilizzati dallo script
per operare.
'''
path = flow_variables['context.workflow.absolute-path']+"/Libraries"
path_config_files = flow_variables['context.workflow.absolute-path']+"/ConfigurationFiles/config.cfg"
sys.path.insert(0,path)
from validation_functions import *
from ip_utils import *
#___________________________________________________________________________

# Copy input to output
output_table = input_table.copy()
#___________________________________________________________________________
'''Questa funzione consente di determinare se i parametri necessari alla
configurazione dell'interfaccia sono stati definiti dall'utente. Essa riceve
tre parametri:

section => Contiene la sezione del file di configurazione, ossia l'interfaccia
per la quale si ricercano i parametri.
option => Rappresenta lo specifico parametro dell'interfaccia
reg_expression => Rappresenta una espressione regolare necessaria alla
ricerca del suddetto parametro. L'utilizzo delle espressioni regolari si
giustifica in quanto contente una maggior flessibilità sulle modalità che
l'utente può utilizzare per nominare i differenti parametri.'''
def key_checker(section,options,file,reg_expression):
	current_value = None
	for current_data in options:
		
		found_elements = re.findall(reg_expression,current_data)
		if len(found_elements)!=0:
			current_value = file.get(section,current_data)
	return current_value
#___________________________________________________________________________
def main():

	#Creazione degli oggetti necessari alla gestione dei file di configurazione.
	#Il primo oggetto rappresenta il file da leggere.
	config_input = configparser.RawConfigParser()
	#Il secondo oggetto serve a definire il file di configurazione "sanificato".
	config_output = configparser.RawConfigParser()

	#Lettura dei parametri dal file.
	config_input.read(path_config_files)

	#Ciascuna sezione del file, delimitata da parentesi quadre, rappresenta
	#una interfaccia. Le operazioni di sanificazione sono ripetute per tutte
	#le interfacce la cui configurazione è definita all'interno dell'apposito file.
	for interface_name in config_input.sections():

		#Variabili atte a rivelare la presenza di una configurazione errata
		#rispettivamente per ipv4 e ipv6.
		problems_v6_config = False
		problems_v4_config = False
		
		is_eth_config = False
		#Ottenimento dei parametri inerenti la interfaccia considerata.
		data = config_input.options(interface_name)

		#Ricerca dei valori assegnati ai parametri mediante la funzione
		#"key_checker()", precedentemente descritta.
		v6_configuration = key_checker(interface_name,data,config_input,'.*configuration.*|.*v6.*|.*ipv6.*|.*configurazione.*')
		dhcpv4 = key_checker(interface_name,data,config_input,'.*dhcpv4.*|dhcp4')
		dhcpv6 = key_checker(interface_name,data,config_input,'.*dhcpv6.*|dhcp6')
		ip_addresses = key_checker(interface_name,data,config_input,'.*indirizzi.*|.*ip.*|.*addresses.*|.*address.*|.*indirizzo.*')
		gateway = key_checker(interface_name,data,config_input,'.*gateway.*')
		dns_list = key_checker(interface_name,data,config_input,'.*dns.*')	

		#__________________________________________________________________________________
		'''In questa sezione sono gestiti i parametri "facoltativi". Nella fattispecie,
		se l'utente non manifesta la volontà esplicita di configurare un indirizzo ipv6
		e di non fornire una configurazione dinamica, tali parametri verranno automaticamente
		assunti come disabilitati. Pertanto, non sarà fornita una configurazione basata su ipv6
		e l'assegnazione degli indirizzi ipv4 avverrà staticamente.'''
		if v6_configuration == None:
			v6_configuration = "false"
	
		if dhcpv4 == None or (dhcpv4!="true" and dhcpv4!="false"):
			dhcpv4 = "false"
	
		if dhcpv6 == None or (dhcpv6!="true" and dhcpv6!="false"):
			dhcpv6 = "false"
		#_______________________________________________________________________________

		#Sanificazione dei parametri inerenti la configurazione degli indirizzi ip
		ipv4_address=''
		ipv6_address=''

		'''In questa sezione di codice si verifica che l'utente abbia inserito
		un indirizzio ipv6 con un prefisso valido nell'ipotesi in cui abbia
		fatto esplicita richiesta di una configurazione basata su ipv6.'''

		#Per controllare la validità dei dati immessi ci si avvale delle funzioni
		#messe a disposizione dalla libreria validation_functions.
		if v6_configuration == "true":
			if dhcpv6 == "false":
				ipv6_address = get_ipv6_address(ip_addresses)
				if validate_ipv6_address(ipv6_address) == False:
					problems_v6_config = True
					print("Attenzione! L'indirizzo IpV6 non è valido.")
				else:
					ipv6_prefix = get_ipv6_prefix(ip_addresses)
					if validate_prefix(ipv6_prefix,1,64) == False:
							problems_v6_config = True
							print("Attenzione! L'indirizzo IPv6 riporta un prefisso non ammissibile!")
					else:
						ipv6_address=ipv6_address+"/"+ipv6_prefix
						print("Ho ottenuto il seguente indirizzo ipv6: "+ipv6_address)
		
		#La medesima procedura è ripetuta per quanto riguarda ipv4.
		if dhcpv4 == "false":
			ipv4_address = get_ipv4_address(ip_addresses)
			ipv4_prefix =  get_ipv4_prefix(ip_addresses)
			print("Nome: "+interface_name+" "+v6_configuration)
			'''Se l'utente ha configurato il file in modo da:
			1)Non configurare indirizzi ipv6.
			2)Non configurare indirizzi ipv4.
			Si assume che l'interfaccia debba essere configurata come 
			interfaccia ethernet. Per ottenere tale configurazione si assegna
			ad essa un indirizzio ipv6 della classe link local, generato casualmente.'''
			if (ipv4_address==None or ipv4_address == "") and v6_configuration=="false":
				is_eth_config = True
				ipv4_address=""
				ipv6_address="FE80::"+str(random.randint(1,10))+"/10"
				print("Configurazione di strato 2..."+interface_name)
			elif validate_ipv4_address(ipv4_address)==False:
				problems_v4_config = True
				ipv4_address=""
				print("Attenzione! L'indirizzo Ipv4 non è valido!")
			else:
				if validate_prefix(ipv4_prefix,1,32)==False:
					problems_v4_config = True
					ipv4_prefix=""
					print("Attenzione! L'Indirizzo IPv4 riporta un prefisso non ammissibile!")
				else:
					ipv4_address=ipv4_address+"/"+ipv4_prefix
					print("Ho ottenuto il seguente indirizzo ipv6: "+ipv6_address)
			
			#Verifica della correttezza dell'eventuale gateway.
			if gateway!=None and gateway!="":
				print("Il gateway è: "+gateway+" Interfaccia "+interface_name)
				if validate_ipv4_address(gateway) == False:
					problems_v4_config = True
					print("Attenzione! È stato specificato un indirizzo di gateway non valido!")
			#Verifica della correttezza dei dati relativi ad eventuali DNS		
			if is_eth_config == False:
				if dns_list == None:
					dns_list = "8.8.8.8"
				else:
					dns_error = False
					dns_rows = dns_list.split(",")
					for current_server in dns_rows:
						if validate_generic_address(current_server)==False:
							dns_error = True
							print("Attenzione! è stato inserito un server DNS errato")
		
					if dns_error == True:
						dns_list="8.8.8.8"
		'''Se alcuni parametri dovessero presentare delle problematiche, essi
		sarranno sostituiti da stringhe vuote, in modo da essere ignorati 
		dal successivo script di generazione del file YAML.'''
		if gateway == None:
			gateway = ""
		
		if problems_v6_config == True:
			v6_configuration = "false"
			ipv6_address=""
			dhcpv6="false"

		if problems_v4_config == True:
			ipv4_address=""
			dhcpv4="false"

		'''Se una delle configurazioni (ipv4 o ipv6) è corretta i parametri
		ad essa relativi saranno copiati nel file di configurazione sanificato.
		In caso contrario la configurazione sarà marcata come "invalida", e lo script successivo
		provvederà ad ignorarla.'''
		
		if (problems_v6_config == False and v6_configuration=="true") or problems_v4_config == False:
			config_output.add_section(interface_name)
			config_output.set(interface_name,'valid','true')
			config_output.set(interface_name,'configurazionev6',v6_configuration)
			config_output.set(interface_name,'dhcp4',dhcpv4)
			config_output.set(interface_name,'dhcp6',dhcpv6)
			if ipv4_address==None:
				ipv4_address = ""
			if ipv6_address==None:
				ipv6_address = ""
			ip = str(ipv4_address)+','+str(ipv6_address)
			config_output.set(interface_name,'indirizzi',ip)
			config_output.set(interface_name,'gateway',gateway)
			config_output.set(interface_name,'dns',dns_list)
		else:
			config_output.add_section(interface_name)
			config_output.set(interface_name,'valid','false')
	with open(path_config_files,'w') as configfile:
		 config_output.write(configfile)
			
main()

