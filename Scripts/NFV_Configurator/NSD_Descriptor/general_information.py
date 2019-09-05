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


	f = open(path_output_files,"w+")
	f.close()
	f = open(path_output_files,"a+")
	f.write('nst:'+"\n")
	
	#Lettura del file di configurazione.
	config = ConfigObj(path_config_files)
	#______________________________________
	#In questa parte dello script si passa in rassegna 
	#a tutte le sezioni presenti nell'apposito file
	for section in config.dict():
		#--------------------------------------------
		#SCRITTURA DELLE INFORMAZIONI GENERALI SULLA NETWORK SLICE
		general_section = re.findall('.*general.*',section.lower())
		if len(general_section)!=0:
			options = config[section]
			id = key_checker(options,'.*id.*')
			name = key_checker(options,'.*name.*|.*nome.*')
			type = key_checker(options,'.*tipo.*|.*type.*') 
			qos = key_checker(options,'.*qos.*|.*qualita.*|.*quality.*|.*service.*|.*servizio.*') 
			
			if id!=None:
				f.write("-    id: "+id+"\n")
			if name!=None:
				f.write("     name: "+name+"\n")
			if type!=None:
				f.write("     SNSSAI-identifier:"+"\n")
				f.write("         slice-service-type: "+type+"\n")   
			if qos!=None:
				f.write("     quality-of-service: "+"\n")
				f.write("         id: "+qos)	

			f.write("\n\n")
					
			
	f.close()


main()
