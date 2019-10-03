from pandas import DataFrame
from configobj import ConfigObj
import re
import sys
 
# Create empty table
output_table = DataFrame()
path_config_files = flow_variables['config_vnf']
path_output_files = flow_variables['vnf_descriptor']
path_lib = flow_variables['context.workflow.absolute-path']+"/Libraries"

sys.path.insert(0,path_lib)

from key_checker import *

def main():
	f = open(path_output_files,"w+")
	f.close()
	f = open(path_output_files,"a+")
	f.write('vnfd:vnfd-catalog:'+"\n")
	f.write('    vnfd:'+"\n")
	#READING OF THE CONFIGURATION FILE.
	config = ConfigObj(path_config_files)
	#______________________________________
	#IN THIS PART OF THE SCRIPT WE ARE LOOKING FOR ALL 
	#SECTIONS DEFINED INSIDE THE CONFIGURATION FILE
	for section in config.dict():
		#--------------------------------------------
		#WRITING OF THE GENERAL INFORMATION ABOUT THE VIRTUALIZED NETWORK FUNCTION
		general_section = re.findall('.*general.*',section.lower())
		if len(general_section)!=0:
			options = config[section]
			id = key_checker(options,'.*id.*')
			name = key_checker(options,'.*name.*')
			short_name = key_checker(options,'.*short.*|.*alias.*') 
			version = key_checker(options,'.*version.*') 
			logo = key_checker(options,'.*logo.*') 
			description = key_checker(options,'.*desc.*')
			if type(description)==list:
				description = ",".join(description)
			if id!=None:
				f.write("    -   id: "+id+"\n")
			if name!=None:
				f.write("        name: "+name+"\n")
			if short_name!=None:
				f.write("        short-name: "+short_name+"\n")
			if version!=None:
				f.write("        version: "+"'"+version+"'"+"\n")
			if logo!=None:
				f.write("        logo: "+logo+"\n")
			if description!=None:
				print(description)
				f.write("        description: "+description+"\n")				
	f.close()
main()
