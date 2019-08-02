import ipaddress

'''Questo insieme di funzioni serve a verificare che l'utente abbia inserito indirizzi ip validi.'''

#Funzione utile a verificare la correttezza di un generico indirizzo ip, sia esso IPv4 sia esso IPv6
def validate_generic_address(address):
	valid_address=False
	try:
		ipaddress.ip_address(address)
		valid_address=True
	except ValueError:
		valid_address=False

	return valid_address

#Funzione utile a verificare la correttezza di un indirizzo IPv4
def validate_ipv4_address(address):
	valid_address=False
	try:
		ipaddress.IPv4Address(address)
		valid_address=True
	except ValueError:
		valid_address=False

	return valid_address

#Funzione utile a verificare la correttezza di un indirizzo IPv6
def validate_ipv6_address(address):
	valid_address=False
	try:
		ipaddress.IPv6Address(address)
		valid_address=True
	except ValueError:
		valid_address=False

	return valid_address

#Funzione utile a verificare la correttezza di un generico prefisso. La funzione riceve come parametri gli estremi 
#del range ammissibile per il prefisso.
def validate_prefix(prefix,start_range,end_range):
	valid_prefix=False
	try:
		prefix_length=int(prefix)
		if prefix_length<=end_range and prefix_length>=start_range:
			valid_prefix = True
	except ValueError:
		valid_prefix = False

	return valid_prefix
