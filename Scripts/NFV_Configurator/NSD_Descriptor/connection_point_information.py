import re
import sys
from configobj import ConfigObj
# Copy input to output
output_table = input_table.copy()

path_config_files = flow_variables['config_ns']
path_output_files = flow_variables['ns_descriptor']
path_lib = flow_variables['context.workflow.absolute-path']+"/Libraries"

sys.path.insert(0,path_lib)

from key_checker import *


def main():

	config = ConfigObj(path_config_files)
	f = open(path_output_files,"a+")
	#______________________________________
	#In questa parte dello script si passa in rassegna 
	#a tutte le sezioni presenti nell'apposito file
	for section in config.dict():
		#--------------------------------------------
		#SCRITTURA DELLE INFORMAZIONI RELATIVE AI DIVERSI PUNTI DI CONNESSIONE ESTERNI
		connection_point_section = re.findall('.*punti.*|.*connessione.*|.*esterni.*',section.lower())
		if len(connection_point_section)!=0:
			f.write("        connection-point:"+"\n")
			for vnfd in config[section]:
				options = config[section][vnfd]
				
				name_point = key_checker(options,'.*nome.*|.*name.*')
				vld_ref = key_checker(options,'.*riferimento.*|.*ref.*|.*vld.*')
				
				if name_point!=None:
					f.write("        -   name: "+name_point+"\n")
				if vld_ref!=None:
					f.write("            vld-id-ref: "+vld_ref+"\n") 

	f.close()

main()