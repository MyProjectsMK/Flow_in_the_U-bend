# Flow in the U-bend
The repository contains an OpenFOAM case (U-bend_0) dedicated to perform CFD simulations of air flow in a U-shaped ventilation duct and scripts written in Python 2.7 (run_calculations) supposed to automate calculations and investigate the point of flow separation from an inner wall of the U-bend.
<br><br>

## Structure of the repository
![Figure 1](https://github.com/MyProjectsMK/Flow_in_the_U-bend/blob/master/README_pictures/case_structure.jpg)

The repository consists of two main folders: *run_controls* and *U-bend_3D_fineMesh_0*. The first one contains scripts written in Python which are responsible for automation of CFD simulations and extracting some significant data from the results of the calculations. The second one contains files of an OpenFOAM case of flow in the U-bend.

The *run_controls* folder contains the following files:
* *detachment_point.py*
* *remove_debris.py*
* *run.py*
* *write_read_turb_coeffs.py*

The *U-bend_3D_fineMesh_0* folder contains the following folders:
* *0*
* *constant*
* *system*

## Geometry and BCs
![Figure 2](https://github.com/MyProjectsMK/Flow_in_the_U-bend/blob/master/README_pictures/3D_model.jpg)

![Figure 3](https://github.com/MyProjectsMK/Flow_in_the_U-bend/blob/master/README_pictures/3D_model_BCs.jpg)

## Mesh
![Figure 4](https://github.com/MyProjectsMK/Flow_in_the_U-bend/blob/master/README_pictures/mesh.png)

## Results
![Figure 5](https://github.com/MyProjectsMK/Flow_in_the_U-bend/blob/master/README_pictures/results_velocity.png)

![Figure 6](https://github.com/MyProjectsMK/Flow_in_the_U-bend/blob/master/README_pictures/detachment_point_position.png)
