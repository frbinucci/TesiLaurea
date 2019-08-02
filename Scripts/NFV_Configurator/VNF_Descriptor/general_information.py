from pandas import DataFrame
from configobj import ConfigObj
import re
import sys
 
# Create empty table
output_table = DataFrame()
path_config_files = flow_variables['context.workflow.absolute-path']+"/ConfigurationFiles/VNFDescriptors.cfg"
path_output_files = flow_variables['context.workflow.absolute-path']+"/OutputFiles"
path_lib = flow_variables['context.workflow.absolute-path']+"/Libraries"

sys.path.insert(0,path_lib)

from key_checker import *

def main():


	f = open(path_output_files+'/descriptorTest.yaml',"w+")
	f.close()
	f = open(path_output_files+'/descriptorTest.yaml',"a+")
	f.write('vnfd:vnfd-catalog:'+"\n")
	f.write('    vnfd:'+"\n")
	
	#Lettura del file di configurazione.
	config = ConfigObj(path_config_files)
	#______________________________________
	#In questa parte dello script si passa in rassegna 
	#a tutte le sezioni presenti nell'apposito file
	for section in config.dict():
		#--------------------------------------------
		#SCRITTURA DELLE INFORMAZIONI GENERALI SUL SERVIZIO
		general_section = re.findall('.*general.*',section.lower())
		if len(general_section)!=0:
			options = config[section]
			id = key_checker(options,'.*id.*')
			name = key_checker(options,'.*name.*|.*nome.*')
			short_name = key_checker(options,'.*short.*|.*corto.*|.*alias.*') 
			version = key_checker(options,'.*version.*') 
			logo = key_checker(options,'.*logo.*') 
			description = ",".join(key_checker(options,'.*desc.*'))
			
			if id!=None:
				f.write("    -   id: "+id+"\n")
			if name!=None:
				f.write("        name: "+name+"\n")
			if short_name!=None:
				f.write("        short_name: "+short_name+"\n")
			if version!=None:
				f.write("        version: "+"'"+version+"'"+"\n")
			if logo!=None:
				f.write("        logo: "+logo+"\n")
			if description!=None:
				print(description)
				f.write("        description: "+description+"\n")			
			
	f.close()


main()