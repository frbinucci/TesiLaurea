import re
from configobj import ConfigObj
# Copy input to output
output_table = input_table.copy()

path_config_files = flow_variables['context.workflow.absolute-path']+"/ConfigurationFiles/VNFDescriptors.cfg"
path_output_files = flow_variables['context.workflow.absolute-path']+"/OutputFiles"

def key_checker(options,reg_expression):
	current_value = None
	for current_data in options:
		
		found_elements = re.findall(reg_expression,current_data,re.IGNORECASE)
		if len(found_elements)!=0:
			current_value = options[current_data]
	return current_value


def main():

	config = ConfigObj(path_config_files)
	f = open(path_output_files+"/descriptorTest.yaml","a+")
	#______________________________________
	#In questa parte dello script si passa in rassegna 
	#a tutte le sezioni presenti nell'apposito file
	for section in config.dict():
		#--------------------------------------------
		#SCRITTURA DELLE INFORMAZIONI RELATIVE AI PUNTI DI CONNESSIONE
		vdu_information = re.findall('.*vdu.*',section.lower())
		if len(vdu_information)!=0:
			f.write("        vdu:"+"\n")
			for current_vdu in config[section]:

				
				hardware_features_subsection = None
				interfaces_subsection = None
				internal_connection_endpoints_subsection = None
				
				for current_subsection in config[section][current_vdu].dict():
					print("Sezione: "+current_subsection)
					hardware_features = re.findall('.*hardware.*|.*features.*|.*caratteristiche.*',current_subsection,re.IGNORECASE)
					interfaces = re.findall('.*interfacce.*|.*interfaces.*',current_subsection,re.IGNORECASE)		
					internal_connection_endpoints = re.findall('.*internal.*|.*connection.*|.*end.*|.*point.*|.*punti.*|.*connessione.*|.*interni.*',current_subsection,re.IGNORECASE)					

					
					if len(hardware_features)>0:
						hardware_features_subsection = hardware_features.pop()

					if len(interfaces)>0:
						interfaces_subsection = interfaces.pop()

					if len(internal_connection_endpoints)>0:
						internal_connection_endpoints_subsection = internal_connection_endpoints.pop()	
					
						
				#---------------------------------------------
				#QUI SONO SCRITTE LE INFORMAZIONI GENERALI
				general_options = config[section][current_vdu]
				print(general_options)				
				name = key_checker(config[section][current_vdu],'.*name.*|.*nome.*')
				image = key_checker(config[section][current_vdu],'.*sistema.*|.*operativo.*|.*immagine.*|.*image.*|.*operating.*|.*system.*')
				count = key_checker(config[section][current_vdu],'.*numero.*|.*progressivo.*|.*count.*|.*number.*|.*progressive.*')
				cloud_init_file = key_checker(config[section][current_vdu],'.*cloud.*|.*init.*|.*file.*|.*config.*')

				f.write("        -   id: "+current_vdu+"\n") 
				
				if name!=None:
					f.write("            name: "+name+"\n")

				if image!=None:
					f.write("            image: "+image+"\n")
				if cloud_init_file!=None:
					f.write("            cloud-init-file: "+cloud_init_file+"\n") 					 
				if count!=None:
					f.write("            count: "+"'"+count+"'"+"\n")
				#--------------------------------------------
				#QUI CI SI OCCUPA DI SCRIVERE LE INFORMAZIONI RELATIVE ALLE CARATTERISTICHE HARDWARE
				if hardware_features_subsection!=None:
					f.write("            vm-flavor: "+"\n")
					number_cpu = key_checker(config[section][current_vdu][hardware_features_subsection],'.*cpu.*|.*number.*|.*processori.*|.*numero.*')
					memory = key_checker(config[section][current_vdu][hardware_features_subsection],'.*ram.*|.*memory.*')
					storage = key_checker(config[section][current_vdu][hardware_features_subsection],'.*storage.*|.*capacita.*')
	
					f.write("               vcpu-count: "+"'"+number_cpu+"'"+"\n")
					f.write("               memory-mb: "+"'"+memory+"'"+"\n")
					f.write("               storage-gb: "+"'"+storage+"'"+"\n")
				#--------------------------------------------
				#QUI CI SI OCCUPA DI SCRIVERE LE INFORMAZIONI RELATIVE ALLE INTERFACCE DI RETE
				if interfaces_subsection!=None:
					f.write("            interface: "+"\n")

					for current_interface in config[section][current_vdu][interfaces_subsection]:
						interface_name = current_interface
						position = key_checker(config[section][current_vdu][interfaces_subsection][current_interface],'.*position.*|.*posizione.*')
						type =  key_checker(config[section][current_vdu][interfaces_subsection][current_interface],'.*tipo.*|.*type.*')
						connection_ref = key_checker(config[section][current_vdu][interfaces_subsection][current_interface],'.*connection.*|.*end.*|.*connessione.*|.*riferimento.*|.*ref.*')
						if type.lower()=="interna" or type.lower()=="interno" or type.lower()=="internal":
							type="INTERNAL"
						else:
							type="EXTERNAL"

						f.write("            -   name: "+interface_name+"\n")

						if position!=None:
							f.write("                position: "+"'"+position+"'"+"\n")
						f.write("                type: "+type+"\n")
						f.write("                virtual-interface: "+"\n")     
						f.write("                    type: PARAVIRT"+"\n")

						if type=="INTERNAL":
							f.write("                internal-connection-point-ref: "+connection_ref+"\n")
						else:
							f.write("                external-connection-point-ref: "+connection_ref+"\n")	
				#--------------------------------------------
				#QUI CI SI OCCUPA DI SCRIVERE LE INFORMAZIONI RELATIVE AI PUNTI DI CONNESSIONE INTERNI											
				if internal_connection_endpoints_subsection!=None:
					f.write("            internal-connection-point: "+"\n")	
					
					for current_endpoint in config[section][current_vdu][internal_connection_endpoints_subsection]:
						id = current_endpoint
						name = key_checker(config[section][current_vdu][internal_connection_endpoints_subsection][current_endpoint],'.*name.*|.*nome.*')
						short_name =  key_checker(config[section][current_vdu][internal_connection_endpoints_subsection][current_endpoint],'.*alias.*|.*short.*|.*corto.*')	
						
						f.write("            -   id: "+id+"\n")

						if name!=None:
							f.write("                name: "+name+"\n")
						if short_name!=None:
							f.write("                short-name: "+short_name+"\n")							
					
	f.close()			

main()