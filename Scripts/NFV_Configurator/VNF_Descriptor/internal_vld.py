import re
from configobj import ConfigObj
import sys
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
	#IN THIS PART OF THE SCRIPT WE ARE LOOKING FOR ALL 
	#SECTIONS DEFINED INSIDE THE CONFIGURATION FILE
	for section in config.dict():
		#--------------------------------------------
		#WRITING OF THE INFORMATION ABOUT THE INTERNAL VIRTUAL LINKS
		internal_vld_information = re.findall('.*internal.*|.*vld.*',section.lower())
		if len(internal_vld_information)!=0:
			f.write("        internal-vld:"+"\n")
			for current_link in config[section]:
				options = config[section][current_link]
				name = key_checker(options,'.*name.*|.*nome.*')
				short_name = key_checker(options,'.*short.*|.*alias.*')
				type = key_checker(options,'.*type.*')
				connection_points = key_checker(options,'.*points.*')
				f.write("        -   id: "+current_link+"\n") 
				
				if name!=None:
					f.write("            name: "+name+"\n")

				if short_name!=None:
					f.write("            short_name: "+short_name+"\n")  

				if type!=None:
					f.write("            type: "+type+"\n")

				if connection_points!=None:
					f.write("            internal-connection-point:"+"\n")
					for current_point in connection_points:
						f.write("            -  id-ref: "+current_point+"\n") 

	f.close()
main()
