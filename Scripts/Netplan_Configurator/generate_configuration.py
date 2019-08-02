import sys
import os
import configparser
from validation_functions import *

#_____________________________________________________________________________________________________________________________________________________
#FUNZIONE PRINCIPALE
#_____________________________________________________________________________________________________________________________________________________
def main():
	#Lo script riceve come parametro la locazione su cui memorizzazare il file di configurazione. Nell'ipotesi in cui essa sia errata, il file di configurazione sarà
	#generato della medesima directory in cui è contenuto lo script.
	file_path = ''
	if len(sys.argv)>1:
		if os.path.isdir(sys.argv[1]):
			file_path = sys.argv[1]+"/"
		else:
			print("<WARN>: Il percorso specificato non sembra essere corretto. Il file di configurazione sarà generato nella medesima directory dello script...\n")

	print("Benvenuti nello strumento di generazione automatica del file di configurazione!")
	print("Questo tool consente di generare automaticamente il file necessario alla configurazione delle diverse interfacce presenti sulla macchina.")
	print("\n")
	number_interfaces = int(input("Quante interfacce si vogliono configurare? "))
	print("\n")
	
	#Generazione dell'oggetto necessario alla gestione del file di configurazione
	out_config = configparser.RawConfigParser()
	
	for i in range(0,number_interfaces):
		
		eth_config_solo = ''
		cfgv6 = ''
		dhcp4 = ''
		dhcp6=''
		ipv4 = ''
		ipv6=''
		gateway4=''
		gateway6=''
		prefix=''

		print("Interfaccia n."+str(i+1)+"\n")
		interface_name = str(input("Inserire il nome dell'interfaccia: "))

		while(eth_config_solo!='y' and eth_config_solo!='n'):
			eth_config_solo = str(input("Si vuole configurare l'interfaccia come interfaccia di strato 2 (Y/N)?")).lower()

		if eth_config_solo!='y':

			while(cfgv6!='y' and cfgv6!='n'):
				cfgv6 = str(input("Si vuole procedere ad una configurazione basata su IPv6 (Y/N)? ")).lower()

			if cfgv6 == 'y':
				cfgv6 = 'true'
			else:
				cfgv6 = 'false'


			while(dhcp4!='s' and dhcp4!='d'):
				dhcp4 = str(input("Si vuol procedere ad una configurazione statica o dinamica per IPv4?(S/D)? ")).lower()

			if dhcp4 == 'd':
				dhcp4 = 'true'
			else:
				dhcp4 = 'false'



			if dhcp4 == 'false':

				ipv4 = str(input("Inserire indirizzo IPv4 dell'intefaccia: "))
				check_ip = validate_ipv4_address(ipv4)
				while check_ip==False:
					print("\nErrore! A quanto pare è stato inserito un indirizzo Ipv4 NON valido! Riprovare\n")
					ipv4 = str(input("Inserire indirizzo IPv4 dell'intefaccia:"))
					check_ip = validate_ipv4_address(ipv4)

				prefix = str(input("Specificare il numero di bit di prefisso (IPv4): "))
				check_prefix = validate_prefix(prefix,1,32)
				while check_prefix==False:
					print("\nErrore! A quanto pare è stato inserito un prefisso (IPv4) NON valido")
					print("Si ricorda che il prefisso deve essere un intero compreso tra 1 e 32\n")
					prefix = str(input("Specificare il numero di bit di prefisso (IPv4): "))
					check_prefix = validate_prefix(prefix,1,32)


				gateway4 = str(input("Inserire l'indirizzo IPv4 del gateway (premere invio se non si vuole specificare un gateway): "))
				
				if gateway4!="":
					check_ip = validate_ipv4_address(gateway4)

					while check_ip==False and gateway4!="":
						print("\nErrore! A quanto pare è stato inserito un indirizzo Ipv4 NON valido! Riprovare\n")
						gateway4 = str(input("Inserire l'indirizzo IPv4 del gateway (premere invio se non si vuole specificare un gateway): "))
						check_ip = validate_ipv4_address(gateway4)
				ipv4=ipv4+"/"+prefix


			if cfgv6 == 'true':
				while(dhcp6!='s' and dhcp6!='d'):
					dhcp6 = str(input("Si vuol procedere ad una configurazione statica o dinamica per IPv6?(S/D)? ")).lower()

				if dhcp6 == 'd':
					dhcp6 = 'true'
				else:
					dhcp6 = 'false'

				if dhcp6 == 'false':
					ipv6 = str(input("Inserire indirizzo IPv6 dell'intefaccia: "))
					check_ip = validate_ipv6_address(ipv6)
					while check_ip==False:
						print("\nErrore! A quanto pare è stato inserito un indirizzo Ipv6 NON valido! Riprovare\n")
						ipv6 = str(input("Inserire indirizzo IPv6 dell'intefaccia:"))
						check_ip = validate_ipv6_address(ipv6)

					prefix = str(input("Specificare il numero di bit di prefisso (IPv6): "))
					check_prefix = validate_prefix(prefix,1,64)
					while check_prefix==False:
						print("\nErrore! A quanto pare è stato inserito un prefisso (IPv6) NON valido")
						print("Si ricorda che il prefisso deve essere un intero compreso tra 1 e 64\n")
						prefix = str(input("Specificare il numero di bit di prefisso (IPv6): "))
						check_prefix = validate_prefix(prefix,1,64)
					ipv6=ipv6+"/"+prefix
			out_config.add_section(interface_name)
			out_config.set(interface_name,"valid","true")
			out_config.set(interface_name,"configurazionev6",cfgv6)
			out_config.set(interface_name,"dhcp4",dhcp4)
			out_config.set(interface_name,"dhcp6",dhcp6)
			out_config.set(interface_name,"indirizzi",ipv4+","+ipv6)
			out_config.set(interface_name,"gateway",gateway4)

			if (dhcp6=='false' or dhcp4=='false'):
				dns_check = ''
				dns_list = []
				while(dns_check!='y' and dns_check!='n'):
					dns_check = str(input("Si vuole specificare una lista di server dns? (Y/N): ")).lower()
				if dns_check=='y':
					dns_list = []
					current_server = ''
					while(current_server!='#'):
						current_server = str(input("Inserire l'indirizzo del prossimo server DNS ('#' per interrompere l'inserimento): "))
						if current_server!='#':
							dns_list.append(current_server)
				else:
					dns_list.append('8.8.8.8')

				out_config.set(interface_name,"dns",(','.join(dns_list)))
			print("\n")
		else:
			out_config.add_section(interface_name)
			
	with open(file_path+'config.cfg', 'w') as configfile:
    		out_config.write(configfile)
#__________________________________________________________________________________________________________________________________

if __name__=="__main__":
	main()
