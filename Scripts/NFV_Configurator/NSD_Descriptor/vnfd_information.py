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
		#SCRITTURA DELLE INFORMAZIONI RELATIVE ALLE VNF CHE COSTITUISCONO IL SERVIZIO
		vnf_section = re.findall('.*vnf.*',section.lower())
		if len(vnf_section)!=0:
			index_counter = 1
			f.write("        constituent-vnfd:"+"\n")
			for vnfd in config[section]:
				options = config[section][vnfd]
				print(options)
				id_descriptor = key_checker(options,'.*id.|.*desc.*')
 
				if id_descriptor!=None:
					f.write("        -   vnfd-id-ref: "+id_descriptor+"\n")
					f.write("            member-vnf-index: "+"'"+str(index_counter)+"'"+"\n") 
				index_counter=index_counter+1 

	f.close()

main()
