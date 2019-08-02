import re
import sys
from configobj import ConfigObj
# Copy input to output
output_table = input_table.copy()

path_config_files = flow_variables['context.workflow.absolute-path']+"/ConfigurationFiles/VNFDescriptors.cfg"
path_output_files = flow_variables['context.workflow.absolute-path']+"/OutputFiles"
path_lib = flow_variables['context.workflow.absolute-path']+"/Libraries"

sys.path.insert(0,path_lib)

from key_checker import *


def main():

	config = ConfigObj(path_config_files)
	f = open(path_output_files+"/descriptorTest.yaml","a+")
	#______________________________________
	#In questa parte dello script si passa in rassegna 
	#a tutte le sezioni presenti nell'apposito file
	for section in config.dict():
		#--------------------------------------------
		#SCRITTURA DELLE INFORMAZIONI RELATIVE AI PUNTI DI CONNESSIONE
		connection_point = re.findall('.*connessione.*|.*punti.*|.*points.*|.*connection.*',section.lower())
		if len(connection_point)!=0:
			f.write("        connection-point:"+"\n")
			for cp in config[section]:
				options = config[section][cp]
				print(options)
				name = key_checker(options,'.*name.*|.*nome.*')
				short_name = key_checker(options,'.*short.*|.*corto.*')
				f.write("        -   id: "+cp+"\n") 
				
				if name!=None:
					f.write("            name: "+name+"\n")

				if short_name!=None:
					f.write("            short_name: "+short_name+"\n")  

	f.close()

main()