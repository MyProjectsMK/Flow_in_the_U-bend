#-*- coding: utf-8 -*-

import os
import shutil

 
# Skrypt służy do usunięcia zbędnych folderów i plików pozostałych po obliczeniach i działaniu skryptów

def hoover(case_name, run_directory, case_directory, case_number, cpu_number):
	folders = ["Decomposer.analyzed"]
	for fn in range(cpu_number):
		folders.append("processor" + str(fn))
	foam_file = case_name + "_" + str(case_number) + ".foam"
	files = ["Decomposer.logfile", "PyFoam.reconstructPar.logfile", "PyFoam.simpleFoam.logfile", "PyFoamHistory", "PyFoamServer.info", "PyFoamState.CurrentTime", "PyFoamState.LastOutputSeen", "PyFoamState.LogDir", "PyFoamState.StartedAt", "PyFoamState.TheState", foam_file]

	if os.path.isfile(run_directory + "/run_controls/remove_debris.pyc"):	
		os.remove(run_directory + "/run_controls/remove_debris.pyc")

	if os.path.isfile(run_directory + "/run_controls/write_read_turb_coeffs.pyc"):	
		os.remove(run_directory + "/run_controls/write_read_turb_coeffs.pyc")

	if os.path.isfile(run_directory + "/run_controls/detachment_point.pyc"):	
		os.remove(run_directory + "/run_controls/detachment_point.pyc")
	
	if os.path.isfile(run_directory + "/run_controls/PlyParser_FoamFileParser_parsetab.py"):	
		os.remove(run_directory + "/run_controls/PlyParser_FoamFileParser_parsetab.py")
	
	if os.path.isfile(run_directory + "/run_controls/PlyParser_FoamFileParser_parsetab.pyc"):
		os.remove(run_directory + "/run_controls/PlyParser_FoamFileParser_parsetab.pyc")

	for i in folders:
		shutil.rmtree(case_directory + "/" + i)

	for j in files:
		os.remove(case_directory + "/" + j)

