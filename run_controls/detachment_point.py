#-*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import xlsxwriter
from pandas import DataFrame


# Skrypt służy do lokalizacji punktu oderwania przepływu w poszczególnych case'ach, zbadania jego położenia względem punktu oderwania przepływu wyznaczonego w trakcie badań eksperymentalnych, zapisania wyników do pliku oraz ich wizualizacji 

# Lokalizacja punktu oderwania przepływu w poszczególnych case'ach
def find_detachment_point(case_directory, case_number, cases_numbers, detachment_point_coordinates):

    print "Localizing the detachment point\n"

    with open(case_directory + "/postProcessing/swakExpression_findPoint_detachment1/0/findPoint_detachment1", 'rb') as file1:
        file1.seek(-100, 2)
        last = file1.readlines()[-1].decode()

    values = last.split()
    x1 = values[1]

    with open(case_directory + "/postProcessing/swakExpression_findPoint_detachment2/0/findPoint_detachment2", 'rb') as file2:
        file2.seek(-100, 2)
        last = file2.readlines()[-1].decode()

    values = last.split()
    x2 = values[1]

    r = 0.0195

    if x1 != "0":
        x = round(float(x1),4)
        y = round(-math.sqrt(pow(r, 2) - pow(x - 1.0, 2)), 4)

    else:
        x = round(float(x2),4)
        y = round(math.sqrt(pow(r, 2) - pow(x - 1.0, 2)), 4)

    cases_numbers.append(case_number)
    detachment_point_coordinates.append([x,y])

    print "Coordinates of the detachment point: x = %.4f, y = %.4f\n" % (x, y)

    return cases_numbers, detachment_point_coordinates


# Wyznaczenie odległości między punktem oderwania przepływu uzyskanym w poszczególnych case'ach a punktem oderwania wyznaczonym w trakcie badań
def dist_to_exp_detachment_point(x_exp, y_exp, cases_numbers, detachment_point_coordinates):

    print "Calculating the distance between the calculated and the experimental detachment point in the respective cases\n"

    dist_to_exp_detach_point = []
    best_cases_numbers = []
    shortest_distance = 10

    for i in cases_numbers:

        distance = round(math.sqrt(pow(detachment_point_coordinates[i-1][0]-x_exp, 2) + pow(detachment_point_coordinates[i-1][1]-y_exp, 2)), 4)
        dist_to_exp_detach_point.append(distance)

        if distance < shortest_distance:
            shortest_distance = distance
            del best_cases_numbers[:]
            best_cases_numbers.append(i)

        elif distance == shortest_distance:
            best_cases_numbers.append(i)

    if len(best_cases_numbers) == 1:
        best_case_number = best_cases_numbers[0]
        print "The shortest distance between the calculated and the experimental detachment point was achieved in Case %d." % (best_case_number)
        print "Distance between the calculated and the experimental detachment point: %.4f m" % (dist_to_exp_detach_point[best_case_number-1])
        print "Coordinates of the calculated detachment point: x = %.4f, y = %.4f" % (detachment_point_coordinates[best_case_number-1][0], detachment_point_coordinates[best_case_number-1][1])

    else:
        print "There are %d cases in which the same shortest distance between the calculated and the experimental detachment point was achieved." % (len(best_cases_numbers))
        print "Distance between the calculated and the experimental detachment point: %.4f m" % (dist_to_exp_detach_point[best_cases_numbers[0]-1])
        print "Coordinates of the detachment point calculated in the respective cases:"
        for j in best_cases_numbers:
            print "Case %d: x = %.4f, y = %.4f" % (j, detachment_point_coordinates[j-1][0], detachment_point_coordinates[j-1][1])

    return dist_to_exp_detach_point, best_cases_numbers


# Zapisanie do pliku parametrów punktu oderwania przepływu wyznaczonego w poszczególnych case'ach oraz wartości współczynników modelu turbulencji modyfikowanych w trakcie obliczeń
def write_results_to_file(cases_numbers, detachment_point_coordinates, dist_to_exp_detach_point, run_directory, turb_coeffs, turb_coeffs_values):

    print "\nWriting results to a file\n"

    x_coordinates = [detachment_point_coordinates[i][0] for i in range(len(detachment_point_coordinates))]
    y_coordinates = [detachment_point_coordinates[j][1] for j in range(len(detachment_point_coordinates))]

    arguments = {'Case number': cases_numbers, 'X-coordinate': x_coordinates, 'Y-coordinate': y_coordinates, 'Distance to experimental detachment point [m]': dist_to_exp_detach_point}
    col_names = ['Case number', 'X-coordinate', 'Y-coordinate', 'Distance to experimental detachment point [m]']

    for k in turb_coeffs:
        arguments[k] = turb_coeffs_values[k]
        col_names.append(k)

    workbook = xlsxwriter.Workbook(run_directory + '/detachment_point_parameters.xlsx')
    workbook.close()

    df = DataFrame(arguments)
    df.to_excel(run_directory + '/detachment_point_parameters.xlsx', sheet_name='Calc_results', index=False,
                columns=col_names)


# Wizualizacja punktu oderwania eksperymentalnego i punktu oderwania uzyskanego w poszczególnych seriach obliczeń
def plot_detachment_points(x_exp, y_exp, cases_numbers, detachment_point_coordinates, best_cases_numbers, run_directory):

    print "Saving to a file the figure of the position of the detachment point obtained in the respective cases\n"

    other_cases_numbers = []

    for i in cases_numbers:

        if i not in best_cases_numbers:
            other_cases_numbers.append(i)

    best_cases_x_coordinates = [detachment_point_coordinates[i - 1][0] for i in best_cases_numbers]
    best_cases_y_coordinates = [detachment_point_coordinates[j - 1][1] for j in best_cases_numbers]

    other_cases_x_coordinates = [detachment_point_coordinates[i - 1][0] for i in other_cases_numbers]
    other_cases_y_coordinates = [detachment_point_coordinates[j - 1][1] for j in other_cases_numbers]

    fig, ax = plt.subplots(figsize=(10,10), dpi=100)

    arc1 = mpatches.Arc([1, 0], 0.039, 0.039, angle=180, theta1=90, theta2=-90, lw=2)
    arc2 = mpatches.Arc([1, 0], 0.189, 0.189, angle=180, theta1=90, theta2=-90, lw=2)
    ax.add_patch(arc1)
    ax.add_patch(arc2)

    plt.plot([0, 1], [-0.0945, -0.0945], color='black', lw=2)
    plt.plot([0, 1], [-0.0195, -0.0195], color='black', lw=2)
    plt.plot([0, 1], [0.0195, 0.0195], color='black', lw=2)
    plt.plot([0, 1], [0.0945, 0.0945], color='black', lw=2)

    plt.xlabel('X', fontweight='bold')
    plt.ylabel('Y', fontweight='bold')
    ttl = plt.title('Position of the detachment point obtained in the respective cases', fontweight='bold')
    ttl.set_position([.5, 1.03])

    plt.xlim(0.96, 1.1)
    plt.ylim(-0.1, 0.1)

    plt.gca().set_aspect('equal', adjustable='box')

    plt.plot(x_exp, y_exp, marker='o', color='blue', label='Experiment', linestyle='None')
    ax.annotate('Exp detachment point', xy=(x_exp, y_exp), xytext=(x_exp+0.002, y_exp+0.001), fontsize=12)

    plt.plot(best_cases_x_coordinates, best_cases_y_coordinates, marker='o', color='y', label='The best case/cases', linestyle='None')

    i = 0
    for k in best_cases_numbers:
        ax.annotate('%d' % k, xy = (best_cases_x_coordinates[i], best_cases_y_coordinates[i]), xytext=(best_cases_x_coordinates[i]+0.001, best_cases_y_coordinates[i]+0.0015), fontsize=12)
        i += 1

    plt.plot(other_cases_x_coordinates, other_cases_y_coordinates, 'o', color='red', label='Other cases', linestyle='None')

    j = 0
    for l in other_cases_numbers:
        ax.annotate('%d' % l, xy = (other_cases_x_coordinates[j], other_cases_y_coordinates[j]), xytext=(other_cases_x_coordinates[j]+0.001, other_cases_y_coordinates[j]+0.0015), fontsize=12)
        j += 1
	
    plt.legend(numpoints=1, fontsize=12)
    plt.savefig(run_directory + '/detachment_point_position.png', bbox_inches='tight')

