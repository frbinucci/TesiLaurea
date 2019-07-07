import importlib.util
import configparser
import re
import sys

path = flow_variables['context.workflow.absolute-path']+"/Libraries"
path_config_files = flow_variables['context.workflow.absolute-path']+"/ConfigurationFiles/config.cfg"
sys.path.insert(0,path)
from validation_functions import *

# Copy input to output
output_table = input_table.copy()

def key_checker(section,options,file,reg_expression):
	current_value = None
	for current_data in options:
		
		found_elements = re.findall(reg_expression,current_data)
		if len(found_elements)!=0:
			current_value = file.get(section,current_data)
	return current_value

def main():

	config_input = configparser.RawConfigParser()
	config_output = configparser.RawConfigParser()
	
	config_input.read(path_config_files)
	
	for interface_name in config_input.sections():
		problems = False
		data = config_input.options(interface_name)
		
		v6_configuration = key_checker(interface_name,data,config_input,'.*configuration.*|.*v6.*|.*ipv6.*|.*configurazione.*')
		dhcpv4 = key_checker(interface_name,data,config_input,'.*dhcpv4.*|dhcp4')
		dhcpv6 = key_checker(interface_name,data,config_input,'.*dhcpv6.*|dhcp6')
		ip_addresses = key_checker(interface_name,data,config_input,'.*indirizzi.*|.*ip.*|.*addresses.*|.*address.*|.*indirizzo.*')
		gateway = key_checker(interface_name,data,config_input,'.*gateway.*')
		dns_list = key_checker(interface_name,data,config_input,'.*dns.*')	

		'''
		print(interface_name+":\n")
		print("Voglio la config v6: "+v6_configuration)
		print("DHCP4: "+dhcpv4)
		print("DHCP6: "+dhcpv6)
		print("Indirizzi: "+ip_addresses)
		print("Gateway: "+gateway)
		print("DNS: "+dns_list)
'''
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
			print(ipv4_address)
			if validate_ipv4_address(ipv4_address.split("/")[0]) == False and dhcpv4 == "false":
				problems = True
			else:
				print("Tutto a posto..."+interface_name)
				if dhcpv4 == "false":
					if len(ipv4_address.split("/"))>1:
						if validate_prefix(ipv4_address.split("/")[1],1,32) == False:
							problems = True
							print("Attenzione! L'indirizzo IPv4 riporta un prefisso non ammissibile!")
					else:
						print("Attenzione! Non è stato specificato alcun prefisso per l'indirizzo IPv4")
						problems = True


			if len(address_block)>1 and v6_configuration=="true":
				ipv6_address = address_block[1]
				if validate_ipv6_address(ipv6_address.split("/")[0]) == False and dhcpv6 == "false":
					problems = True
					print("Attenzione! L'indirizzo IpV6 non è valido.")
				else:
					if dhcpv6 == "false":
						if len(ipv6_address.split("/"))>1:
							if validate_prefix(ipv6_address.split("/")[1],1,64) == False:
								problems = True
								print("Attenzione! L'indirizzo IPv6 riporta un prefisso non ammissibile!")
						else:
							print("Attenzione! Non è stato specificato alcun prefisso per l'indirizzo IPv6")
							problem_rilevator = True
			elif v6_configuration == "true" and dhcpv6 == "false":
					problems = True
					print("Attenzione! L'indirizzo Ipv6 non è valido.")

		elif dhcpv4=="false" or (dhcpv6=="false" and v6_configuration=="true"):
			problems = True
			print("Se si vuole una configurazione statica occorre specificare gli indirizzi IP.")

		if gateway == None and dhcpv4=="false":
			problems = True
			print("Se si vuole una configurazione statica occorre specificare il gateway!")
		elif dhcpv4 == "false" and validate_ipv4_address(gateway) == False:
			problems = True
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

		if problems == False:
			config_output.add_section(interface_name)
			config_output.set(interface_name,'valid','true')
			config_output.set(interface_name,'configurazionev6',v6_configuration)
		
			config_output.set(interface_name,'dhcp4',dhcpv4)
			config_output.set(interface_name,'dhcp6',dhcpv6)
			ip = ipv4_address+','+ipv6_address
			config_output.set(interface_name,'indirizzi',ip)
			config_output.set(interface_name,'gateway',str(gateway))
			config_output.set(interface_name,'dns',dns_list)
		else:
			config_output.add_section(interface_name)
			config_output.set(interface_name,'valid','false')
	with open(path_config_files,'w') as configfile:
	 	config_output.write(configfile)
				
main()

