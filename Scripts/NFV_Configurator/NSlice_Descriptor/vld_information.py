import re
import sys
from configobj import ConfigObj
# Copy input to output
output_table = input_table.copy()

path_config_files = flow_variables['nst_config']
path_output_files = flow_variables['nst_desc']
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
		#SCRITTURA DELLE INFORMAZIONI RELATIVE AI PUNTI DI CONNESSIONE
		vld_section = re.findall('.*vld.*',section.lower())
		if len(vld_section)!=0:
			f.write("     netslice-vld: "+"\n")
			for vld in config[section]:
				options = config[section][vld]
				print(options)
				id = vld
				name = key_checker(options,'.*name.*|.*nome.*')
				type = key_checker(options,'.*tipo.*|.*type.*')
				is_management = key_checker(options,'.*management.*')

				connection_points_subsection = None

				for current_subsection in config[section][vld]:
					connection_points = re.findall('.*connection.*|.*end.*|.*point.*|.*punti.*|.*connessione.*',current_subsection,re.IGNORECASE)

				if connection_points!=None:
 					connection_points_subsection = connection_points.pop()
 				
				f.write("     -   id: "+id+"\n")
				if name!=None:
					f.write("         name: "+name+"\n") 

				if type!=None:
					f.write("         type: "+type+"\n") 

				if is_management=="true":
					f.write("         mgmt-network: "+"'"+is_management+"'"+"\n") 
				
				if connection_points_subsection!=None:
					f.write("         nss-connection-point-ref:"+"\n")
					for current_point in config[section][vld][connection_points_subsection]:
						nss_ref = key_checker(config[section][vld][connection_points_subsection][current_point],'.*nss.*')
						connection_point = key_checker(config[section][vld][connection_points_subsection][current_point],'.*point.*|.*punto.*')
						if nss_ref!=None:
							f.write("         -   nss-ref: "+nss_ref+"\n") 

						if connection_point!=None:
							f.write("             nsd-connection-point-ref: "+connection_point+"\n")
			f.write("\n")


	

	f.close()

main()