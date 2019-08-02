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
	f = open(path_output_files+'/descriptorTest.yaml',"a+")
		
	#Lettura del file di configurazione.
	config = ConfigObj(path_config_files)
	#______________________________________
	#In questa parte dello script si passa in rassegna 
	#a tutte le sezioni presenti nell'apposito file
	for section in config.dict():
		#--------------------------------------------
		#SCRITTURA DELLE INFORMAZIONI GENERALI SUL SERVIZIO
		management_interface = re.findall('.*management.*',section.lower())
		if len(management_interface)!=0:
			management_interface = key_checker(config[section],".*id.*|.*int.*")
			f.write('        mgmt-interface:'+"\n")
			f.write('            cp: '+management_interface+"\n")
	f.close()


main()