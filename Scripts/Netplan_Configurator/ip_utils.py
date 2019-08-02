#Funzione atta alla restituzione degli indirizzi ipv6
def get_ipv6_address(ip_addresses):
	ipv6_address = None
	if ip_addresses!=None:
		address_block = ip_addresses.split(",")

		if(len(address_block)!=1):
			ipv6_address = address_block[1].split("/")[0]

	return ipv6_address
#Funzione atta alla restituzione del prefisso ipv6
def get_ipv6_prefix(ip_addresses):
	ipv6_prefix = None
	if ip_addresses!=None:
		address_block = ip_addresses.split(",")

		if(len(address_block)!=1):
			if(len(address_block[1].split("/"))!=1):	
				ipv6_prefix = address_block[1].split("/")[1]
	return ipv6_prefix
		

#Funzione atta alla restituzione degli indirizzi ipv4
def get_ipv4_address(ip_addresses):
	ipv4_address = None
	if ip_addresses!=None:
		address_block = ip_addresses.split(",")
		ipv4_address = address_block[0].split("/")[0]
	return ipv4_address

#Funzione atta alla restituzione del prefisso ipv4
def get_ipv4_prefix(ip_addresses):
	ipv4_prefix = None
	if ip_addresses!=None:
		address_block = ip_addresses.split(",")
		
		ipv4 = address_block[0].split("/")
		if len(ipv4)!=1:
			ipv4_prefix = ipv4[1]
	return ipv4_prefix
