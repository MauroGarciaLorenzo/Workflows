# -*- coding: utf-8 -*-

import numpy as np
import shutil
import pathlib
# path = pathlib.Path(__file__).parent.resolve()
import os

path = os.getcwd()
import sys

sys.path.append(path)

import time

import math
import trimesh
from pycompss.api.task import task
from pycompss.api.parameter import *


from PHASES.MESHER.permeability_mesher.WriteAlyaBou import writeAlyaBou
from PHASES.MESHER.permeability_mesher.WriteAlyaFix import writeAlyaFix
from PHASES.MESHER.permeability_mesher.WriteAlyaFie import writeAlyaFie
from PHASES.MESHER.permeability_mesher.WriteAlyaSet import writeAlyaSet
from PHASES.MESHER.permeability_mesher.WriteAlyaSet3 import writeAlyaSet3
from PHASES.MESHER.permeability_mesher.WriteAlyaSet4 import writeAlyaSet4
from PHASES.MESHER.permeability_mesher.WriteAlyaMat import writeAlyaMat
from PHASES.MESHER.permeability_mesher.FeatsFromMats import writeAlyaSetFtMats
from PHASES.MESHER.permeability_mesher.WriteAlyaNsi import writeAlyaNsi
from PHASES.MESHER.permeability_mesher.WriteAlyaDom import writeAlyaDom
from PHASES.MESHER.permeability_mesher.WriteAlyaDat import writeAlyaDat
from PHASES.MESHER.permeability_mesher.WriteAlyaKer import writeAlyaKer
from PHASES.MESHER.permeability_mesher.WriteAlyaPos import writeAlyaPos
from PHASES.MESHER.permeability_mesher.WriteJobLauncher import writeJobLauncher
from PHASES.MESHER.permeability_mesher.WriteAlyaGeo import writeAlyaGeo

from PHASES.MESHER.permeability_mesher.GenGeometry import generar_superficies_rectangulares
from PHASES.MESHER.permeability_mesher.GenGeometry import generar_superficies_puntos
from PHASES.MESHER.permeability_mesher.GenCases import NoFallos
from PHASES.MESHER.permeability_mesher.GenCases import Overlap
from PHASES.MESHER.permeability_mesher.GenCases import Gap
from PHASES.MESHER.permeability_mesher.FVF_variation_defects import FVF_variation
from PHASES.MESHER.permeability_mesher.GenerateMeshOris import Mesh_and_Oris

def permeability_from_doe(**kwargs):
    for item in kwargs['problem_mesher']:
        kwargs.update(item)
    values=kwargs.get("values")
    kwargs['angles_tows'] = [values[2], values[3], values[4], values[5], values[6], values[7]]
    kwargs['w_tow'] = float(values[0])
    kwargs['L_pro'] = values[1]
    del kwargs['problem_mesher']
    return RVEgen2Alya(**kwargs)

def permeability_mesher(**kwargs):
    for item in kwargs['problem_mesher']:
        kwargs.update(item)
    values=kwargs.get("values")
    kwargs['angles_tows'] = [values['angle_1'], values['angle_2'], values['angle_3'], values['angle_4'], values['angle_5'], values['angle_6']]

    del kwargs['problem_mesher']
    return RVEgen2Alya(**kwargs)


@task(returns=1)
def RVEgen2Alya(path, num_caso, Density, Viscosity, Gravity, FVF_component, Defect, factor_desplazamiento,
                w_tow, h_tow, L_pro, n_elements_gap, n_elementos_towsingap,
                n_elements_layer, n_layers, angles_tows, n_tows, Lset, Defect_Size, ajus_ol, Defect_Transition, ol_drch, AlyaSet, debug, consider_FVF_variation, Full_Periodicity):
    print("    Generating geometry ...")

    # Get the start time
    st = time.time()

    # --------------------------------------------
    #
    # Units
    #
    #   Variable  Description              SI (m)  SI (mm)
    #       nu    Viscosity                 Pa·s      MPa·s
    #       Kxx   Permeability in long.     m^2       mm^2
    #       Kyy   Permeability in tran.     m^2       mm^2
    #       P     Pressure                  Pa        MPa
    #       rho   Density                   kg/m^3    tonne/mm^3
    #       v     Velocity                  m/s       mm/s
    #
    # --------------------------------------------

    # --------------------------------------------
    #
    # Inputs
    # UNITS: SI
    # --------------------------------------------

    # Problem setup
    # 	debug = False
    #   Presion_de_inyeccion = 70000.0
    # 	Gravity = 10000.0
    TotalTimeSimulation = 1000.0
    MaxNumSteps = 1e6
    periodicityMethod = 'Automatic'
    fieldFlag = True

    simulaciones = ["x-flow", "y-flow", "z-flow"]

    # Nord3v2 Job setup
    # 	queue = 'debug'
    # 	numCPUs = 64

    # %%
    # --------------------------------------------
    #
    # Crear la geometria y malla
    #
    # --------------------------------------------

    inicio = time.time()
    ###################################################################
    ###################################################################
    ###################################################################
    ###################################################################
    # 	Defect = "O"
    # 	w_tow = 5.0
    # 	h_tow = 0.182			# Altura (espesor) de la capa.
    # 	L_pro = 0.2
    # 	n_elements_gap = 2     # Numero de elementos que queremos que haya en cada gap (colocado a 0 o 90).
    # 	# Hay que tener cuidado porque el numero de elementos del modelo crece muy rapido.
    # 	n_elementos_towsingap = 100 # Numero de elementos en cada tow en caso de que L_pro=0.0
    # 	n_elements_layer = 2    # Numero de elementos que queremos que haya en cada capa
    # 	n_layers = 3	# Numero de capas que se generan
    # 	angles_tows = [0, 0, 0, 135, 0] #Angulos correspondiente a cada capa
    # 	n_tows = 2
    # 	Lset = 1
    # 	# Variables a continuacion seran llamadas en caso de fallo (overlap/gap)
    # 	Defect_Size = 2.0
    # 	ajus_ol = 5/6
    # 	Defect_Transition = 0.6
    # 	ol_drch = 0.6
    ###################################################################
    ###################################################################
    ###################################################################
    ###################################################################

    if Defect == "N":
        caseName = "Caso_" + str(num_caso)
        datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array = NoFallos(w_tow, h_tow, L_pro,
                                                                                             angles_tows, n_layers,
                                                                                             n_tows, n_elements_gap,
                                                                                             n_elementos_towsingap,
                                                                                             n_elements_layer,
                                                                                             factor_desplazamiento)
    elif Defect == "O":
        caseName = "Caso_" + str(num_caso)
        datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array = Overlap(w_tow, h_tow, L_pro, Defect_Size,
                                                                                            ajus_ol, Defect_Transition, ol_drch,
                                                                                            angles_tows, n_layers,
                                                                                            n_tows, n_elements_gap,
                                                                                            n_elementos_towsingap,
                                                                                            n_elements_layer,
                                                                                            factor_desplazamiento)
    elif Defect == "G":
        caseName = "Caso_" + str(num_caso)
        datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array = Gap(w_tow, h_tow, L_pro, Defect_Size,
                                                                                        ajus_ol, Defect_Transition, ol_drch,
                                                                                        angles_tows, n_layers, n_tows,
                                                                                        n_elements_gap,
                                                                                        n_elementos_towsingap,
                                                                                        n_elements_layer,
                                                                                        factor_desplazamiento)

    # Job case
    # caseName = 'Caso_0_0_0_w2mm_lpro0p2mm_fine'

    # Set paths for directories
    basePath = f'{path}'
    outputPath = f'{basePath}/output/' + caseName
    if os.path.exists(outputPath):
        shutil.rmtree(f'{basePath}/output/' + caseName)
    os.makedirs(outputPath)
    outputMeshPath = f'{basePath}/output/' + caseName + '/msh/'
    os.makedirs(outputMeshPath)
    ##########################################
    ##########################################
    ##########################################
    ##########################################

    combined = []
    planos_Yarn = []
    centros_Yarn = []
    contarTow = 0
    for i in datos_input:
        contarTow += 1
        if int((len(i[0]) - 3) / 3) == 1:
            comb, plan, cent = generar_superficies_rectangulares(i)
        else:
            comb, plan, cent = generar_superficies_puntos(i)
        combined.append(comb)
        planos_Yarn.append(plan)
        centros_Yarn.append(cent)

        # Ruta del archivo de salida STL
        archivo_stl = outputPath + '/' + 'tow_{}.stl'.format(contarTow)

        # Guardar el objeto STL en un archivo
        combined[contarTow - 1].save(archivo_stl)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Geometry generation time: {round(tiempo_ej / 60, 2)} min")

    print(f"    The model will have {(n_nodos - 1) * (n_nodos - 1) * (n_espesor - 1)} elements")

    ##########################################

    ##########################################

    # %%

    # Mesh and orientation

    inicio = time.time()

    dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris, nodes = Mesh_and_Oris(Ldom, n_nodos,
                                                                                                         n_layers, h_tow,
                                                                                                         n_espesor,
                                                                                                         datos_input,
                                                                                                         outputPath,
                                                                                                         planos_Yarn,
                                                                                                         centros_Yarn)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Mesh and Oris generation time: {round(tiempo_ej / 60, 2)} min")

    # %%

    # --------------------------------------------
    #
    # Borrar variables que no se van a utilizar
    #
    # --------------------------------------------

    # 	del A, w_tow, angles_tows, archivo_stl, B, C, cent, centros_Yarn, comb
    # 	del combined, contarTow, D, delante_detras, delante_detras_anterior, delante_detras_menor, delante_detras_posterior
    # 	del dimCoord, direccion, direccion_unitaria, distance
    # 	del dot_product, fin, i, inicio, j, k, n, n_elements_layer, n_elements_gap
    # 	del normal_vector, p, P1, P2, p_plano, plan, planos_Yarn, point_to_check, posicion_posterior
    # 	del matriz_1dc_inout, menor_distancia, mesh_loaded, mesh_loaded_n, n_elementos_towsingap, n_espesor
    # 	del n_espesorc, n_nodos, n_tows, nc, node_tows, posicion_anterior, posicion_menor
    # 	del tiempo_ej, tow, tow_contains, tow_orientacion, v_plano_point
    # 	del vector_equidistante_X, vector_equidistante_Xc, vector_equidistante_Y, vector_equidistante_Yc
    # 	del vector_equidistante_Z, vector_equidistante_Zc, x0, x0c, x_plano
    # 	del xn, xnc, y0, y0c, y_plano, yn, ync, z0, z0c, z_plano, zn, znc

    # --------------------------------------------
    #
    # Alya files
    #
    # --------------------------------------------

    inicio = time.time()
    print('    Calculating FVF_tows ...')

    # Creamos una copia de la matriz que tiene la información de a qué tow pertenece cada elemento
    matriz_3dc_FVF = np.copy(matriz_3dc_inout)
    # Cálculo teórico del FVF de los tows para tener un FVF de componente dado
    FVF_component_tows = (FVF_component * (w_tow + L_pro)) / w_tow
    # Los elementos que pertenecen a tow los ponemos con FVF
    matriz_3dc_FVF[matriz_3dc_FVF != 0] = FVF_component_tows
    # Busca si hay overlap para cambiar la FVF
    if Defect == 'O' or Defect == 'G':
        if consider_FVF_variation == True:
            matriz_3dc_FVF = FVF_variation(matriz_3dc_inout, n_layers, matriz_3dc_FVF, ajus_ol)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        FVF generation time: {round(tiempo_ej / 60, 2)} min")

    # --------------------------------------------

    inicio = time.time()
    print('    Writting Alya files ...')
    print('    Writting Alya jobName.geo.dat ...')

    # Alya geo file
    Elementsetmaterials, numero_elemento, posicion_n_nodo, Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array = writeAlyaGeo(
        outputMeshPath, caseName, dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris,
        angles_tows, n_elements_layer, matriz_3dc_FVF)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Geo file generation time: {round(tiempo_ej / 60, 2)} min")

    # --------------------------------------------
    #
    # Alya .mat.dat
    # The number of materials is harcoded to be always 2: fibre and matrix
    # --------------------------------------------
    inicio = time.time()
    print('    Writting Alya jobName.mat.dat ...')
    nmate = writeAlyaMat(outputMeshPath, caseName, Elementsetmaterials)
    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Mat file generation time: {round(tiempo_ej / 60, 2)} min")
    # --------------------------------------------
    #
    # Alya .bou.dat and .fix.dat
    #
    # --------------------------------------------
    inicio = time.time()

    # 	print('Getting Alya boundaries ...')
    print('    Writting Alya jobName.bou.dat ...')

    # e1list = [int(numero_elemento[0][j][k]) for j in range(len(numero_elemento[0])) for k in range(len(numero_elemento[0][j]))]
    # e2list = [int(numero_elemento[-1][j][k]) for j in range(len(numero_elemento[-1])) for k in range(len(numero_elemento[-1][j]))]
    # e3list = [int(numero_elemento[i][0][k]) for i in range(len(numero_elemento)) for k in range(len(numero_elemento[i][0]))]
    # e4list = [int(numero_elemento[i][-1][k]) for i in range(len(numero_elemento)) for k in range(len(numero_elemento[i][-1]))]
    # e5list = [int(numero_elemento[i][j][0]) for i in range(len(numero_elemento)) for j in range(len(numero_elemento[i]))]
    # e6list = [int(numero_elemento[i][j][-1]) for i in range(len(numero_elemento)) for j in range(len(numero_elemento[i]))]
    # x0 = [int(posicion_n_nodo[0][j][k]) for j in range(len(posicion_n_nodo[0])) for k in range(len(posicion_n_nodo[0][j]))]
    # xl = [int(posicion_n_nodo[-1][j][k]) for j in range(len(posicion_n_nodo[-1])) for k in range(len(posicion_n_nodo[-1][j]))]
    # y0 = [int(posicion_n_nodo[i][0][k]) for i in range(len(posicion_n_nodo)) for k in range(len(posicion_n_nodo[i][0]))]
    # yl = [int(posicion_n_nodo[i][-1][k]) for i in range(len(posicion_n_nodo)) for k in range(len(posicion_n_nodo[i][-1]))]
    # z0 = [int(posicion_n_nodo[i][j][0]) for i in range(len(posicion_n_nodo)) for j in range(len(posicion_n_nodo[i]))]
    # zl = [int(posicion_n_nodo[i][j][-1]) for i in range(len(posicion_n_nodo)) for j in range(len(posicion_n_nodo[i]))]
    # blist = [[e1list,x0], [e2list,xl], [e3list,y0], [e4list,yl], [e5list,z0], [e6list,zl]]

    nboun = 0
    b_list1 = []
    for j in range(len(numero_elemento[0, :, 0])):
        for k in range(len(numero_elemento[0, 0, :])):
            b_list1.append([int(posicion_n_nodo[0, j, k]), int(posicion_n_nodo[0, j, k + 1]),
                            int(posicion_n_nodo[0, j + 1, k + 1]), int(posicion_n_nodo[0, j + 1, k]),
                            int(numero_elemento[0, j, k])])
            nboun += 1
    b_list2 = []
    for j in range(len(numero_elemento[-1, :, 0])):
        for k in range(len(numero_elemento[-1, 0, :])):
            b_list2.append([int(posicion_n_nodo[-1, j, k]), int(posicion_n_nodo[-1, j + 1, k]),
                            int(posicion_n_nodo[-1, j + 1, k + 1]), int(posicion_n_nodo[-1, j, k + 1]),
                            int(numero_elemento[-1, j, k])])
            nboun += 1
    b_list3 = []
    for i in range(len(numero_elemento[:, 0, 0])):
        for k in range(len(numero_elemento[0, 0, :])):
            b_list3.append([int(posicion_n_nodo[i, 0, k]), int(posicion_n_nodo[i + 1, 0, k]),
                            int(posicion_n_nodo[i + 1, 0, k + 1]), int(posicion_n_nodo[i, 0, k + 1]),
                            int(numero_elemento[i, 0, k])])
            nboun += 1
    b_list4 = []
    for i in range(len(numero_elemento[:, -1, 0])):
        for k in range(len(numero_elemento[-1, 0, :])):
            b_list4.append(
                [int(posicion_n_nodo[i + 1, -1, k]), int(posicion_n_nodo[i, -1, k]), int(posicion_n_nodo[i, -1, k + 1]),
                 int(posicion_n_nodo[i + 1, -1, k + 1]), int(numero_elemento[i, -1, k])])
            nboun += 1
    b_list5 = []
    for i in range(len(numero_elemento[:, 0, 0])):
        for j in range(len(numero_elemento[0, :, 0])):
            b_list5.append([int(posicion_n_nodo[i, j + 1, 0]), int(posicion_n_nodo[i + 1, j + 1, 0]),
                            int(posicion_n_nodo[i + 1, j, 0]), int(posicion_n_nodo[i, j, 0]),
                            int(numero_elemento[i, j, 0])])
            nboun += 1
    b_list6 = []
    for i in range(len(numero_elemento[:, -1, 0])):
        for j in range(len(numero_elemento[-1, :, 0])):
            b_list6.append([int(posicion_n_nodo[i, j, -1]), int(posicion_n_nodo[i + 1, j, -1]),
                            int(posicion_n_nodo[i + 1, j + 1, -1]), int(posicion_n_nodo[i, j + 1, -1]),
                            int(numero_elemento[i, j, -1])])
            nboun += 1

    b_list = [b_list1, b_list2, b_list3, b_list4, b_list5, b_list6]

    # Built RVE element boundaries for each boundary
    # b_list, nboun = getRVEboundaries(element_node_conectivity,blist)

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución getRVEboundaries: {tiempo_ej} segundos")
    # 	inicio = time.time()

    writeAlyaBou(outputMeshPath, caseName, b_list)
    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Bou file generation time: {round(tiempo_ej / 60, 2)} min")
    inicio = time.time()

    print('    Writting Alya jobName.fix.dat ...')
    writeAlyaFix(outputMeshPath, caseName, b_list)

    numerodenodos = int(len(posicion_n_nodo[:, 0, 0]) * len(posicion_n_nodo[0, :, 0]) * len(posicion_n_nodo[0, 0, :]))
    numerodeelementos = len(Elementsetmaterials[:, 0])
    numerodeboundelems = nboun

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Fix file generation time: {round(tiempo_ej / 60, 2)} min")
    # --------------------------------------------
    #
    # Alya .fie.dat (porosity tensor)
    #
    # --------------------------------------------
    # inicio = time.time()

    # print('Reading .ori file ...')

    # # importa el archivo .ori y se analiza la orientación de todos los elementos para luego asignar la permeabilidad

    # fin = time.time()
    # tiempo_ej = fin-inicio
    # print(f"Tiempo de ejecución crear variables de orientaciones: {tiempo_ej} segundos")
    inicio = time.time()

    print('    Writting Alya jobName.fie.dat ...')

    writeAlyaFie(outputMeshPath, caseName, Viscosity, FVF_component_tows, Elementsetmaterials, \
                 numerodeelementos, Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Fie file generation time: {round(round(tiempo_ej / 60, 2))} min")

    # --------------------------------------------
    #
    # from src.Escritura_inp import Escritura_inp
    # Escritura_inp(nombre_caso ,dimX, dimY, dimZ, matriz_4d, dimXc, dimYc, dimZc, datos_input, matriz_3dc_inout, matriz_3dc_oris,
    #                Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array)
    # #
    # --------------------------------------------

    # --------------------------------------------
    #
    # Alya Set - BSC (mesh) - estamos machacando el otro de momento
    #
    # --------------------------------------------
    #### AQUÍ ABRÍA QUE INCLUIR LA PARTE DE LOS SETS
    ####
    ####
    ####
    ####
    inicio = time.time()

    print('    Writting Alya jobName.set.dat ...')

    # Alya Set
    if AlyaSet == 'All':
        writeAlyaSet(outputMeshPath, caseName, numerodeelementos, numerodeboundelems)
    else:
        # 	    writeAlyaSetFtMats(outputMeshPath, caseName, matriz_3dc_inout, Lset, n_layers, nodes)
        # 		writeAlyaSet3(outputMeshPath, caseName, Lset, n_layers, nodes, L_pro, Ldom, mov_geometria_array, Defect_Size, Defect_Transition, ol_drch, desfase_array, angles_tows, w_tow, Defect)
        writeAlyaSet4(outputMeshPath, caseName, Lset, n_layers, nodes, L_pro, Ldom, mov_geometria_array, Defect_Size, Defect_Transition,
                      ol_drch, desfase_array, angles_tows, w_tow, Defect, matriz_3dc_FVF)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Set file generation time: {round(tiempo_ej / 60, 2)} min")

    # --------------------------------------------
    #
    # Alya periodicity file (NOT NEEDED)
    #
    # --------------------------------------------

    ### ESTA PARTE HABRÍA QUE REVISARLA PARA USARLA

    if periodicityMethod == 'Manual':
        print('NOT MANTAINED!!!!!!')
    # 		# Get nodes from vertices
    # 		n1, n2, n3, n4, n5, n6, n7, n8 = getRVEnodesFromVertices(lx,ly,lz,na,n)
    #
    # 		# Get nodes from edges
    # 		e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12 = getRVEnodesFromEdges(lx,ly,lz,n,na,n1,n2,n3,n4,n5,n6,n7,n8)
    #
    # 		bound_xl = e1  + e2  + e5  + e6  + [n1] + [n2] + [n3] + [n4]
    # 		bound_yl = e2  + e3  + e10 + e11 + [n2] + [n3] + [n6] + [n7]
    # 		bound_zl = e6  + e7  + e11 + e12 + [n3] + [n4] + [n7] + [n8]
    #
    # 		# Slave - master approach
    # 		lmast = []
    # 		print('Adding nodes from vertices ...')
    # 		lmast = addNodesFromVertices(n1,n2,n3,n4,n5,n6,n7,n8,lmast)
    #
    # 		print('Adding nodes from edges ...')
    # 		lmast = addNodesFromEdges(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,x,y,z,tol,lmast)
    #
    # 		print('Adding nodes from faces ...')
    # 		fileName = 'x'
    # 		lmast = addNodesFromFacesMeso('x',x,y,z,x0,y0,z0,xl,yl,zl,bound_xl,bound_yl,bound_zl,tol,lmast)
    # 		lmast.sort(key=lambda k: k[0])
    # 		print('Writting Alya jobName.per.dat ...')
    # 		writeAlyaPer(path, fileName, lmast)
    # 		if 'y' in simulaciones:
    # 			shutil.copy("x.per.dat","y.per.dat")
    # 		if 'z' in simulaciones:
    # 			fileName = 'z'
    # 			lmast = addNodesFromFacesMeso('z',x,y,z,x0,y0,z0,xl,yl,zl,bound_xl,bound_yl,bound_zl,tol,lmast)
    # 			lmast.sort(key=lambda k: k[0])
    # 			print('Writting Alya jobName.per.dat ...')
    # 			writeAlyaPer(path, fileName, lmast)
    else:
        print('    NOTE: Periodicity is imposed automatically by Alya ...')

    # --------------------------------------------
    #
    # End generating Alya mesh files
    #
    # --------------------------------------------

    # --------------------------------------------
    #
    # Alya configuration files for each flow direction
    #
    # --------------------------------------------
    inicio = time.time()

    print('    Writting Alya Configuration files ...')

    lx = Ldom  # Esto son mm
    ly = Ldom  # Esto son mm
    lz = n_layers * h_tow  # Esto son mm
    length = [lx * 1e-3, ly * 1e-3, lz * 1e-3]  # TODO: Acordar las unidades y quitar!
    for j in range(len(simulaciones)):
        path = outputPath + '/' + str(simulaciones[j]) + '/'
        os.makedirs(path)
        fileName = caseName
        icase = str(simulaciones[j])

        node = 1  # TODO: Coger un nodo que no este en la direccion del flow (solo en z)
        # Preliminary calculations
        #		Gravity = Presion_de_inyeccion/(Density*length[j])
        Presion_de_inyeccion = Gravity * (Density * length[j])

        # Alya Dom
        writeAlyaDom(path, fileName, icase, int(numerodenodos), numerodeelementos, numerodeboundelems, nmate,
                     periodicityMethod, fieldFlag, Full_Periodicity)
        # Alya Dat
        writeAlyaDat(debug, path, fileName, TotalTimeSimulation, MaxNumSteps)
        # Alya Ker
        writeAlyaKer(debug, path, fileName, nmate, Density, Viscosity)
        # Alya Nsi
        writeAlyaNsi(debug, path, fileName, icase, Presion_de_inyeccion, Gravity, lx, ly, lz, node, Full_Periodicity)
        # Alya Pos
        writeAlyaPos(path, fileName)

        # Job Launcher
        writeJobLauncher(path, fileName)

    # Get the end time
    et = time.time()

    # Get the execution time
    elapsed_time = et - st

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Configuration files generation time: {round(tiempo_ej / 60, 2)} min")
    print('  Total execution time:', round(elapsed_time / 60, 2), 'min')
    return