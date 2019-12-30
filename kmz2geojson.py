# note: relies on kml2geojson (https://github.com/mrcagney/kml2geojson) being installed in active environment

import os

def kmz2geojson(full_kmz_path, output_directory):
	if full_kmz_path.endswith('.kmz'):
		try:
			main_file_name = full_kmz_path[(full_kmz_path.rfind('/')+1):-4]
			main_directory = full_kmz_path[0:(full_kmz_path.rfind('/'))]
			command_string = f'cp {full_kmz_path} kmz.zip'
			os.system(command_string)
			os.system('unzip kmz.zip')
			kml_file = f'{main_directory}/doc.kml'
			geojson_file = f'{main_directory}/{main_file_name}.geojson'
			command_string = f'k2g {kml_file} {geojson_file}'
			os.system(command_string)
		except Exception as e:
			message = e
			pass
	elif full_kmz_path.endswith('.kml'):
		try:
			main_file_name = full_kmz_path[(full_kmz_path.rfind('/')+1):-4]
			main_directory = full_kmz_path[0:(full_kmz_path.rfind('/'))]
			geojson_file = f'{main_directory}/{main_file_name}.geojson'
			command_string = f'k2g {full_kmz_path} {geojson_file}'
		except Exception as e:
			message = e
	else:
		message = "File is not kmz or kml."
	return message
