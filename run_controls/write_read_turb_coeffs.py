#-*- coding: utf-8 -*-

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


# Skrypt służy do modyfikacji w pliku "turbulenceProperties" wartości wybranych współczynników modelu turbulencji i ich sczytania

def write_read_turbulence_coefficients(case_number, case_i_dir, turb_coeffs, turb_coeffs_values, delta_turb_coeffs):

    if case_number == 1:

        turb = ParsedParameterFile(case_i_dir + "/constant/turbulenceProperties")

        for k in turb_coeffs:
            turb_coeffs_values[k].append(turb['RAS']['kOmegaSSTCoeffs'][k])

        print "\nTurbulence coefficients:"
        for l in turb_coeffs:
            print l + ": %.4f" % (turb_coeffs_values[l][0])

    else:

        turb = ParsedParameterFile(case_i_dir + "/constant/turbulenceProperties")

        for m in turb_coeffs:
            turb['RAS']['kOmegaSSTCoeffs'][m] += delta_turb_coeffs['delta_' + m]

        turb.writeFile()

        for n in turb_coeffs:
            turb_coeffs_values[n].append(turb['RAS']['kOmegaSSTCoeffs'][n])

        print "\nTurbulence coefficients:"
        for o in turb_coeffs:
            print o + ": %.4f" % (turb_coeffs_values[o][case_number-1])

    return turb_coeffs_values
