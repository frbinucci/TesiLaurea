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
	#READING OF THE CONFIGURATION FILE
	config = ConfigObj(path_config_files)
	#______________________________________
	#IN THIS PART OF THE SCRIPT WE ARE LOOKING FOR ALL 
	#SECTIONS DEFINED INSIDE THE CONFIGURATION FILE
	for section in config.dict():
		#--------------------------------------------
		#WRITING OF THE INFORMATION ABOUT THE MANAGEMENT INTERFACES
		management_interface = re.findall('.*management.*',section.lower())
		if len(management_interface)!=0:
			management_interface = key_checker(config[section],".*id.*|.*int.*")
			f.write('        mgmt-interface:'+"\n")
			f.write('            cp: '+management_interface+"\n")
	f.close()
main()
