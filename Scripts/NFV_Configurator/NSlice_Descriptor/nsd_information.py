from pandas import DataFrame
from configobj import ConfigObj
import re
import sys
 
# Create empty table
output_table = DataFrame()
path_config_files = flow_variables['nst_config']
path_output_files = flow_variables['nst_desc']
path_lib = flow_variables['context.workflow.absolute-path']+"/Libraries"

sys.path.insert(0,path_lib)

from key_checker import *

def main():

	f = open(path_output_files,"a+")
	#Lettura del file di configurazione.
	config = ConfigObj(path_config_files)
	#______________________________________
	#In questa parte dello script si passa in rassegna 
	#a tutte le sezioni presenti nell'apposito file
	for section in config.dict():
		#--------------------------------------------
		#SCRITTURA DELLE INFORMAZIONI RELATIVE AI SINGOLI NS DELLA SLICE
		subnet_section = re.findall('.*subnet.*|.*nsd.*',section.lower())
		if len(subnet_section)!=0:
			f.write("     netslice-subnet: "+"\n")	
			
			for current_subnet in config[section]:
				options = config[section][current_subnet]
				subnet_id = current_subnet
				shared = key_checker(options,'.*condivisione.*|.*shared.*|.*sharing.*')
				description = key_checker(options,'.*desc.*')
				ref = key_checker(options,'.*riferimento.*|.*ref.*')
				if type(description)==list:
					description = ",".join(description)

				if subnet_id!=None:
					f.write("     -   id: "+subnet_id+"\n")
				if shared=='true':
					f.write("         is-shared-nss: "+"'"+shared+"'"+"\n")
				else:
					f.write("         is-shaered-nss: 'false'"+"\n")

				if description!=None:
					f.write("         description: "+description+"\n")

				if ref!=None:
					f.write("         nsd-ref: "+ref+"\n")	

			f.write("\n")
				
			
	f.close()


main()