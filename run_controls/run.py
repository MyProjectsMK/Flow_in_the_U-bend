#! /usr/bin/python
#-*- coding: utf-8 -*-

from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.Applications.Decomposer import Decomposer
from PyFoam.Applications.CaseReport import CaseReport
from PyFoam.Execution.ParallelExecution import LAMMachine
from write_read_turb_coeffs import write_read_turbulence_coefficients
from remove_debris import hoover
import detachment_point as dp


# Skrypy służy do zarządzania procesem obliczeń w programie OpenFOAM. Wymaga uprzedniego przygotowania case'u wraz z siatką obliczeniową.
# ***USER*** oznacza zmienną/zmienne, których wartość/wartości musi podać użytkownik

# Informacje o case'ie
case_name = "U-bend" # ***USER*** nazwa case'u
run_dir = "/home/maciek/OpenFOAM/maciek-4.1/run/U-bend" # ***USER*** ścieżka do folderu z case'em
case_dir = run_dir + "/" + case_name # ścieżka do folderu zawierającego pliki case'u
case_prev_dir = case_dir + "_0"

# Informacje o modyfikowanych w trakcie obliczeń współcznnikach modelu turbulencji
turb_coeffs = ['alphaK1', 'alphaOmega2', 'gamma1'] # ***USER*** nazwy modyfikowanych w trakcie obliczeń współczynników turbulencji
turb_coeffs_values = {'alphaK1': [], 'alphaOmega2': [], 'gamma1': []} # ***USER*** nazwy modyfikowanych w trakcie obliczeń współczynników turbulencji i ich wartości w poszczególnych seriach obliczeń (pola między nawiasami kwadratowymi zostawić puste)
delta_turb_coeffs = {'delta_alphaK1': 0.1, 'delta_alphaOmega2': -0.1, 'delta_gamma1': 0.075} # ***USER*** wartości, o jakie będą modyfikowane wybrane współczynniki turbulencji w kolejnych seriach obliczeń

# ***USER*** współrzędne punktu oderwania przepływu otrzymane w badaniach laboratoryjnych
x_exp = 1.00975
y_exp = 0.01689

# ***USER*** liczba serii obliczeń
iter_number = 1

# ***USER*** liczba wątków procesora/procesorów wykorzystywanych w obliczeniach 
cpu_number = 2

cases_numbers = []
detachment_point_coordinates = []

# Pętla obliczeń
for i in range(1,iter_number+1):

	print "\nCase " + str(i)
	print "======"
	
	# Utworzenie folderu case'u i-tej serii obliczeń i przekopiowanie do niego folderów "0", "constant" i "system" z case'u obliczanego w poprzedniej serii	
	case_i_dir = case_dir + "_" + str(i)
	orig=SolutionDirectory(case_prev_dir, archive=None, paraviewLink=False)	
	work=orig.cloneCase(case_i_dir)

	# Modyfikacja w pliku "turbulenceProperties" wartości wybranych współczynników modelu turbulencji i ich sczytanie 	
	turb_coeffs_values_updated = write_read_turbulence_coefficients(i, case_i_dir, turb_coeffs, turb_coeffs_values, delta_turb_coeffs)	
	turb_coeffs_values = turb_coeffs_values_updated

	# Dekompozycja case'u na potrzeby obliczeń równoległych	
	print "\nDecomposing case"
	Decomposer(args=["--progress", work.name, cpu_number])
	CaseReport(args=["--decomposition", work.name])
	machine=LAMMachine(nr=cpu_number)

	# Obliczenia	
	print "Running calculations\n"
	theRun=BasicRunner(argv=["simpleFoam", "-case", work.name], silent=True, lam=machine)
	theRun.start()
	print "Calculations finish\n"

	# Rekonstrukcja case'u po zakończeniu obliczeń	
	print "Reconstructing case\n"
	reconstruction=BasicRunner(argv=["reconstructPar", "-case", work.name], silent=True)
	reconstruction.start()

	# Lokalizacja punktu oderwania przepływu	
	cases_numbers_updated, detachment_point_coordinates_updated = dp.find_detachment_point(case_i_dir, i, cases_numbers, detachment_point_coordinates)
	cases_numbers = cases_numbers_updated
    	detachment_point_coordinates = detachment_point_coordinates_updated
	
	# Usunięcie zbędnych folderów i plików pozostałych po obliczeniach i działaniu skryptów	
	print "Removing debris\n"
	hoover(case_name, run_dir, case_i_dir, i, cpu_number)
	
	# Zakończenie i-tej serii obliczeń	
	print "Finish"
	print "======\n"

	if i < iter_number:
		case_prev_dir = case_i_dir

# Wyznaczenie odległości między punktem oderwania przepływu uzyskanym w poszczególnych case'ach a punktem oderwania wyznaczonym w trakcie badań
distance_to_experimental_detachment_point, best_cases_numbers = dp.dist_to_exp_detachment_point(x_exp, y_exp, cases_numbers, detachment_point_coordinates)

# Zapisanie do pliku parametrów punktu oderwania przepływu wyznaczonego w poszczególnych case'ach oraz wartości współczynników modelu turbulencji modyfikowanych w trakcie obliczeń
dp.write_results_to_file(cases_numbers, detachment_point_coordinates, distance_to_experimental_detachment_point, run_dir, turb_coeffs, turb_coeffs_values)
 
# Wizualizacja punktu oderwania eksperymentalnego i punktu oderwania uzyskanego w poszczególnych seriach obliczeń
dp.plot_detachment_points(x_exp, y_exp, cases_numbers, detachment_point_coordinates, best_cases_numbers, run_dir)

# Zakończenie działania skryptu
print "\nEND"
print "===\n"

