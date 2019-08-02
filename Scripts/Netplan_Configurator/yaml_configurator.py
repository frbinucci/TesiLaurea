import configparser

# Copy input to output
output_table = input_table.copy()

#Ottenimento del percorso assoluto del file di configurazione.
path_config_file = path_config_files = flow_variables['context.workflow.absolute-path']+"/ConfigurationFiles/config.cfg"

#Generazione dell'oggetto che rappresenza il file di configurazione.
config = configparser.RawConfigParser()
config.read(path_config_file)

#Apertura del file yaml contenente la configurazione delle interfacce di rete.
f = open("/etc/netplan/50-cloud-init.yaml","a+")

#__________________________________________________________
#CONFIGURAZIONE DELLE INTERFACCE
#Lo script assume che il file su cui si opera non contenga
#dati inconsistenti.
for interface in config.sections():
	#Verifica della validità della configurazione dell'interfaccia
	if config[interface]['valid'] == "true":

		only_eth_config = False
		interface_name = interface
		v6_config = config[interface]['configurazionev6']
		dhcp4 = config[interface]['dhcp4']
		dhcp6 = config[interface]['dhcp6']
		ip_addresses = config[interface]['indirizzi']
		gateway = config[interface]['gateway']
		dns = config[interface]['dns']

		#Scrittura del nome dell'interfaccia
		f.write("        "+interface_name+":\n")
		#______________________________________
		#Scrittura parametri inerenti gli indirizzi IP
		#_______________________________________
		if dhcp4!="true" or (v6_config=="true" and dhcp6!="true"):
			f.write("            "+"addresses: "+"\n")
    
		if dhcp4!="true":
		    ipv4 = ip_addresses.split(",")[0]
		    if ipv4=="" and v6_config=="false":
		    	f.write("            - "+ip_addresses.split(",")[1]+"\n")
		    	only_eth_config = True
		    elif ipv4!="":
		    	f.write("            - "+ipv4+"\n")    

		if v6_config == "true" and only_eth_config == False:
			if dhcp6!="true":
				if len(ip_addresses.split(","))>1:
					ipv6 = ip_addresses.split(",")[1]
					f.write("            - "+ipv6+"\n")
			f.write("            "+"dhcp6: "+dhcp6+"\n") 
		if only_eth_config == False:
			f.write("            "+"dhcp4: "+dhcp4+"\n") 
		#____________________________________________
		#Scrittura parametri inerenti il gateway
		#____________________________________________
		if dhcp4!='true' and only_eth_config== False and gateway!="":
		    f.write("            "+"gateway4: ")
		    f.write(gateway+"\n")
		#____________________________________________
		#Scrittura parametri inerenti il DNS
		#____________________________________________
		if (dhcp4!='true' or (dhcp6!='true' and v6_config=="true")) and only_eth_config== False:
		    dns_list = dns.split(",")
		    f.write("            "+"nameservers:"+"\n")
		    f.write("                 addresses: ")
		    f.write("\n")
		    
		    for dns_server in dns_list:
		        f.write("                 - "+dns_server+"\n")
		    
f.close()
		


