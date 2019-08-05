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
		#SCRITTURA DELLE INFORMAZIONI RELATIVE AI PUNTI DI CONNESSIONE
		vld_section = re.findall('.*vld.*',section.lower())
		if len(vld_section)!=0:
			f.write("        vld:"+"\n")
			for vld in config[section]:
				options = config[section][vld]
				print(options)
				id = vld
				name = key_checker(options,'.*name.*|.*nome.*')
				short_name = key_checker(options,'.*alias.*')
				type = key_checker(options,'.*tipo.*|.*type.*')
				is_management = key_checker(options,'.*management.*')
				vim_network_name = key_checker(options,'.*vim.*')

				connection_points_subsection = None

				for current_subsection in config[section][vld]:
					connection_points = re.findall('.*connection.*|.*end.*|.*point.*|.*punti.*|.*connessione.*',current_subsection,re.IGNORECASE)

				if connection_points!=None:
 					connection_points_subsection = connection_points.pop()
 				
				f.write("        -   id: "+id+"\n")
				if name!=None:
					f.write("            name: "+name+"\n") 

				if short_name!=None:
					f.write("            short-name: "+name+"\n") 

				if type!=None:
					f.write("            type: "+type+"\n") 

				if is_management=="true":
					f.write("            mgmt-network: "+"'"+is_management+"'"+"\n") 
					if vim_network_name!=None:
						f.write("            vim-network-name: "+"'"+vim_network_name+"'"+"\n") 
				
				if connection_points_subsection!=None:
					f.write("            vnfd-connection-point-ref:"+"\n")
					for current_point in config[section][vld][connection_points_subsection]:
						vnfd_ref = key_checker(config[section][vld][connection_points_subsection][current_point],'.*vnf.*')
						index = key_checker(config[section][vld][connection_points_subsection][current_point],'.*index.*|.*indice.*')
						ref = key_checker(config[section][vld][connection_points_subsection][current_point],'.*ref.*|.*rif.*')
						if vnfd_ref!=None:
							f.write("            -    vnfd-id-ref: "+vnfd_ref+"\n") 

						if index!=None:
							f.write("                 member-vnf-index-ref: "+"'"+index+"'"+"\n")

						if ref!=None:
							f.write("                 vnfd-connection-point-ref: "+"'"+ref+"'"+"\n")
							

	f.close()

main()