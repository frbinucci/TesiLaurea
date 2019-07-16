import importlib.util
import configparser
import re
import sys

path = flow_variables['context.workflow.absolute-path']+"/Libraries"
path_config_files = flow_variables['context.workflow.absolute-path']+"/ConfigurationFiles/config.cfg"
sys.path.insert(0,path)
from validation_functions import *
from ip_utils import *

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
		problems_v6_config = False
		is_eth_config = False
		data = config_input.options(interface_name)
			
		v6_configuration = key_checker(interface_name,data,config_input,'.*configuration.*|.*v6.*|.*ipv6.*|.*configurazione.*')
		dhcpv4 = key_checker(interface_name,data,config_input,'.*dhcpv4.*|dhcp4')
		dhcpv6 = key_checker(interface_name,data,config_input,'.*dhcpv6.*|dhcp6')
		ip_addresses = key_checker(interface_name,data,config_input,'.*indirizzi.*|.*ip.*|.*addresses.*|.*address.*|.*indirizzo.*')
		gateway = key_checker(interface_name,data,config_input,'.*gateway.*')
		dns_list = key_checker(interface_name,data,config_input,'.*dns.*')	
	
		if v6_configuration == None:
			v6_configuration = "false"
	
		if dhcpv4 == None or (dhcpv4!="true" and dhcpv4!="false"):
			dhcpv4 = "false"
	
		if dhcpv6 == None or (dhcpv6!="true" and dhcpv6!="false"):
			dhcpv6 = "false"
	
		ipv4_address=''
		ipv6_address=''
	
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

		problems_v4_config = False

		if dhcpv4 == "false":
			ipv4_address = get_ipv4_address(ip_addresses)
			ipv4_prefix =  get_ipv4_prefix(ip_addresses)
			print("Nome: "+interface_name+" "+v6_configuration)
			if (ipv4_address==None or ipv4_address == "") and v6_configuration=="false":
				is_eth_config = True
				ipv4_address=""
				ipv6_address="FE80::1/10"
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

			if gateway!=None and gateway!="":
				print("Il gateway è: "+gateway+" Interfaccia "+interface_name)
				if validate_ipv4_address(gateway) == False:
					problems_v4_config = True
					print("Attenzione! È stato specificato un indirizzo di gateway non valido!")
					
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
	
		if gateway == None:
			gateway = ""

		if problems_v6_config == True:
				v6_configuration = "false"

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

