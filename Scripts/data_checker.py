import re
import random
from validation_functions import *
import sys
import os

def key_checker(data,reg_expression):
	current_value = None
	for current_data in data:
		key = current_data.split("=")[0].lower()
		value = current_data.split("=")[1]
		
		found_elements = re.findall(reg_expression,key)
		if len(found_elements)!=0:
			current_value = value
	return current_value

def main():
	if len (sys.argv)<3:
		sys.stderr.write("Attenzione! Alcuni parametri non sono stati specificati!")
		sys.exit(1)
	elif not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2]):
		sys.stderr.write("Attenzione! Uno o più percorsi indicati NON sono validi")
		sys.exit(2)


	file_path = sys.argv[1]
	output_path = sys.argv[2]
	f = open(file_path,"r+")

	file_data = f.read()
	f.close()

	f = open(output_path+'new_configuration.txt',"w+")
	f.write('')
	f.close()



	file_data = file_data.replace(" ","")
	file_data = re.sub(r'(?m)^ *#.*\n?','',file_data)
	file_data = re.sub(r'(?m)^ *\n?','',file_data)



	int_list = file_data.split('$')

	print(file_data)

	data_interface = []


	count_interface=1
	for interface in int_list:
		if count_interface!= len(int_list):
			problem_rilevator = False
			interface_parameters = interface.split(";")


			interface_name = key_checker(interface_parameters,'.*nome.*|.*name.*|.*interfaccia.*|.*interface.*|.*int.*')
			v6_configuration = key_checker(interface_parameters,'.*configuration.*|.*v6.*|.*ipv6.*|.*configurazione.*')
			dhcpv4 = key_checker(interface_parameters,'.*dhcpv4.*|dhcp4')
			dhcpv6 = key_checker(interface_parameters,'.*dhcpv6.*|dhcp6')
			ip_addresses = key_checker(interface_parameters,'.*indirizzi.*|.*ip.*|.*addresses.*|.*address.*|.*indirizzo.*')
			gateway = key_checker(interface_parameters,'.*gateway.*')
			dns_list = key_checker(interface_parameters,'.*dns.*')

			if interface_name == None:
				interface_name = "interface"+str(random.randint(1,len(int_list)*100))

			if v6_configuration == None:
				v6_configuration = "false"

			if dhcpv4 == None or (dhcpv4!="true" and dhcpv4!="false"):
				dhcpv4 = "false"

			if dhcpv6 == None or (dhcpv6!="true" and dhcpv6!="false"):
				dhcpv6 = "false"

			ipv4_address=''
			ipv6_address=''


			#In questa fase gestisco il caso in cui l'utente abbia richiesto una configurazione statica senza specificare gli indirizzi IP
			if ip_addresses != None:
				address_block = ip_addresses.split(",")
				ipv4_address = address_block[0]
				if validate_ipv4_address(ipv4_address.split("/")[0]) == False and dhcpv4 == "false":
					problem_rilevator = True
					print("Attenzione! L'indirizzo IpV4 non è valido.")
				else:
					if dhcpv4 == "false":
						if len(ipv4_address.split("/"))>1:
							if validate_prefix(ipv4_address.split("/")[1],1,32) == False:
								problem_rilevator = True
								print("Attenzione! L'indirizzo IPv4 riporta un prefisso non ammissibile!")
						else:
							print("Attenzione! Non è stato specificato alcun prefisso per l'indirizzo IPv4")
							problem_rilevator = True


				if len(address_block)>1 and v6_configuration=="true":
					ipv6_address = address_block[1]
					if validate_ipv6_address(ipv6_address.split("/")[0]) == False and dhcpv6 == "false":
						problem_rilevator = True
						print("Attenzione! L'indirizzo IpV6 non è valido.")
					else:
						if dhcpv6 == "false":
							if len(ipv6_address.split("/"))>1:
								if validate_prefix(ipv6_address.split("/")[1],1,64) == False:
									problem_rilevator = True
									print("Attenzione! L'indirizzo IPv6 riporta un prefisso non ammissibile!")
							else:
								print("Attenzione! Non è stato specificato alcun prefisso per l'indirizzo IPv6")
								problem_rilevator = True
				elif v6_configuration == "true" and dhcpv6 == "false":
						problem_rilevator = True
						print("Attenzione! L'indirizzo Ipv6 non è valido.")

			elif dhcpv4=="false" or (dhcpv6=="false" and v6_configuration=="true"):
				problem_rilevator = True
				print("Se si vuole una configurazione statica occorre specificare gli indirizzi IP.")

			if gateway == None and dhcpv4=="false":
				problem_rilevator = True
				print("Se si vuole una configurazione statica occorre specificare il gateway!")
			elif dhcpv4 == "false" and validate_ipv4_address(gateway) == False:
				problem_rilevator = True
				print("Attenzione! È stato specificato un indirizzo di gateway non valido!")

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

			if problem_rilevator == False:
				f = open(output_path+'/new_configuration.txt', 'a+')

				f.write('nome_interfaccia='+interface_name+';\n')
				f.write('configurazionev6='+v6_configuration+';\n')
				f.write('dhcp4='+dhcpv4+';\n')
				f.write('dhcp6='+dhcpv6+';\n')
				f.write('indirizzi='+ipv4_address+','+ipv6_address+';\n')
				f.write('gateway='+str(gateway)+';\n')
				f.write('dns='+dns_list+'$\n')
				f.close()

		count_interface+=1

if __name__=="__main__":
	main()
