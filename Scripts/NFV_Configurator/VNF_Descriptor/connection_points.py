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
	#IN THIS PART OF THE SCRIPT WE ARE LOOKING FOR ALL SECTION
	#DEFINED INSIDE THE CONFIGURATION FILE
	for section in config.dict():
		#--------------------------------------------
		#WRITING OF THE INFORMATION ABOUT THE CONNECTION POINTS
		connection_point = re.findall('.*points.*|.*connection.*',section.lower())
		if len(connection_point)!=0:
			f.write("        connection-point:"+"\n")
			for cp in config[section]:
				options = config[section][cp]
				print(options)
				name = key_checker(options,'.*name.*')
				short_name = key_checker(options,'.*short.*|.*alias.*')
				f.write("        -   id: "+cp+"\n") 
				if name!=None:
					f.write("            name: "+name+"\n")

				if short_name!=None:
					f.write("            short_name: "+short_name+"\n")  
	f.close()
main()
