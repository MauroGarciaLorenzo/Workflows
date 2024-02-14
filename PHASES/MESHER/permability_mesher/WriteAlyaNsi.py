
def writeAlyaNsi(debug, path, fileName, icase, pressure, gravity, lx, ly, lz, node):
    """ Alya caseName.nsi.dat file
    """
    
    stream = open(path+fileName+'.nsi.dat', 'w', newline='\n')

    stream.write('$-------------------------------------------------------------------\n')
    stream.write('$\n')
    stream.write(f'$ {fileName:s}\n')
    stream.write('$\n')
    stream.write('$ Dimensions:\n')
    stream.write(f'$   lx= {lx:1.5f}\n')
    stream.write(f'$   ly= {ly:1.5f}\n')
    stream.write(f'$   lz= {lz:1.5f}\n')
    stream.write('$\n')
    stream.write('$ Boundary conditions:\n')
    stream.write('$\n')
    stream.write('$   D            C\n') 
    stream.write('$    o----------o          o----------o\n')        
    stream.write('$    |\         |\         |\         |\ \n')      
    stream.write('$    | \        | \        | \    4   | \ \n')   
    stream.write('$    |  \ H     |  \ G     |  \  5    |  \ \n')
    stream.write('$    |   o------+---o      |   o------+---o\n')
    stream.write('$    |   |      |   |      | 1 |      | 2 |\n')
    stream.write('$    o---+------o   |      o---+------o   |\n')
    stream.write('$   A \  |     B \  |       \  |    6  \  |\n')
    stream.write('$      \ |        \ |        \ |   3    \ |\n')
    stream.write('$       \|         \|         \|         \|\n')
    stream.write('$        o----------o          o----------o\n')
    stream.write('$       E            F\n')
    stream.write('$   ^ y\n')
    stream.write('$   |\n')
    stream.write('$   |      x\n')
    stream.write('$   o----->\n')
    stream.write('$    \ \n')
    stream.write('$    _\/ z\n')
    stream.write('$\n')
    stream.write('$   CODE 1: LEFT,  X= 0\n')
    stream.write('$   CODE 2: RIGHT, X= lx\n')
    stream.write('$   CODE 3: BOT,   Y= 0\n')
    stream.write('$   CODE 4: TOP,   Y= ly\n')
    stream.write('$   CODE 5: BACK,  Z= 0\n')
    stream.write('$   CODE 6: FRONT, Z= lz\n')
    stream.write('$\n')
    stream.write('$   Periodicity is shown for X- and Y-flow directions:\n')
    stream.write('$\n')
    stream.write('$      Faces           Edges         Vertices\n')
    stream.write('$   ------------------------------------------------\n')
    stream.write('$   Slave Master    Slave Master    Slave Master\n')
    stream.write('$    BCGF  ADHE      EF    AB         E     A\n')
    stream.write('$                    FG    BC         F     B\n')
    stream.write('$                    GH    CD         G     C\n')  
    stream.write('$    DHGC  AEFB      HE    DA         H     D\n')
    if icase == 'z-flow':
        stream.write('$    EFGH  ABCD      BC    AD         G     A\n')
        stream.write('$                    EH    AD\n')        
        stream.write('$                    FG    AD\n')
    stream.write('$\n')
    if icase == 'x-flow':
        stream.write('$   Flow:         x-direction\n')
        stream.write('$   Wall no-slip: AEFB and DHGC, vz= 0.0\n')
        stream.write(f'$   Pressure:     {pressure:1.5e}\n')
        stream.write('$   Periodicity:  BCGF with ADHE and DHGC with AEFB\n')
    elif icase == 'y-flow':
        stream.write('$   Flow:         y-direction\n')
        stream.write('$   Wall no-slip: AEFB and DHGC, vz= 0.0\n')
        stream.write(f'$   Pressure:     {pressure:1.5e}\n')
        stream.write('$   Periodicity:  BCGF with ADHE and DHGC with AEFB\n')
    elif icase == 'z-flow':
        stream.write('$   Flow:         z-direction\n')
        stream.write('$   Wall no-slip: -\n')
        stream.write(f'$   Pressure:     {pressure:1.5e}\n')
        stream.write('$   Periodicity:  All\n')
    stream.write('$\n')
    stream.write('$ Units:     SI\n')
    stream.write('$\n')
    stream.write('$ Reference: CAELESTIS\n')
    stream.write('$\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PHYSICAL_PROBLEM\n')
    stream.write('  PROBLEM_DEFINITION\n')
    stream.write('    TEMPORAL_DERIVATIVES: ON\n')
    stream.write('    CONVECTIVE_TERM:      ON\n')
    stream.write('    VISCOUS_TERM:         LAPLACIAN\n')
    if icase == 'x-flow':
        stream.write(f'    GRAVITY:              NORM= {gravity:1.5e}, GX= 1.0, GY= 0.0, GZ= 0.0\n')
    elif icase == 'y-flow':
        stream.write(f'    GRAVITY:              NORM= {gravity:1.5e}, GX= 0.0, GY= 1.0, GZ= 0.0\n')
    elif icase == 'z-flow':
        stream.write(f'    GRAVITY:              NORM= {gravity:1.5e}, GX= 0.0, GY= 0.0, GZ= 1.0\n')
    stream.write('  END_PROBLEM_DEFINITION\n')
    stream.write('END_PHYSICAL_PROBLEM\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('NUMERICAL_TREATMENT\n')
    stream.write('  ELEMENT_LENGTH:         Minimum\n')
    stream.write('  STABILIZATION:          ASGS, NOTA1\n')
    stream.write('  TIME_INTEGRATION:       Trapezoidal, ORDER: 1\n')
    stream.write('  SAFETY_FACTOR=          2000.0\n')
    stream.write('  STEADY_STATE_TOLER=     1e-5\n')
    stream.write('  VECTORIZED_ASSEMBLY:    ON\n')
    stream.write('  NORM_OF_CONVERGENCE:    LAGGED_ALGEBRAIC_RESIDUAL\n')
    stream.write('  MAXIMUM_NUMBER_OF_IT=   1\n')
    stream.write('  CONVERGENCE_TOLERANCE=  1e-6\n')
    stream.write('  ALGORITHM:              SCHUR\n')
    stream.write('    SOLVER:               ORTHOMIN, MOMENTUM_PRESERVING\n')
    stream.write('    PRECONDITIONER:       TAU\n')
    stream.write('    ELEMENT_LENGTH:       Minimum\n')
    stream.write('    TAU_STRATEGY:         Codina\n')
    stream.write('  END_ALGORITHM\n')
    stream.write('  MOMENTUM\n')
    stream.write('    ALGEBRAIC_SOLVER\n')     
    stream.write('      SOLVER:             BICGSTAB\n')
    stream.write('      CONVERGENCE:        ITERATIONS= 1000, TOLERANCE= 1.0e-10, ADAPTIVE, RATIO= 1.0e-3\n')
    stream.write('      OUTPUT:             CONVERGENCE\n')
    stream.write('      PRECONDITIONER:     DIAGONAL\n')
    stream.write('    END_ALGEBRAIC_SOLVER\n')     
    stream.write('  END_MOMENTUM\n')
    stream.write('  CONTINUITY \n')
    stream.write('    ALGEBRAIC_SOLVER\n')
    stream.write('       SOLVER:            DEFLATED_CG, COARSE: SPARSE\n')
    stream.write('       CONVERGENCE:       ITERATIONS= 1000, TOLERANCE= 1.0e-10, ADAPTIVE, RATIO= 1.0e-3\n')
    stream.write('       OUTPUT:            CONVERGENCE\n')
    stream.write('       PRECONDITIONER:    DIAGONAL\n')
    stream.write('    END_ALGEBRAIC_SOLVER\n')     
    stream.write('  END_CONTINUITY\n')
    stream.write('  DIRICHLET: MATRIX\n')
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS\n')
    if debug:
        stream.write('  START_POSTPROCESS_AT: STEP= 0\n')
        stream.write('  POSTPROCESS FIXNO\n')
        stream.write('  POSTPROCESS VELOC\n')
        stream.write('  POSTPROCESS PRESS\n')
    stream.write('  ELEMENT_SET\n')
    stream.write('    MEANP\n')
    stream.write('    VELOX\n')
    stream.write('    VELOY\n')
    stream.write('    VELOZ\n')
    stream.write('  END_ELEMENT_SET\n')
    stream.write('  BOUNDARY_SET\n')
    stream.write('    MASS\n')
    stream.write('    MEANP\n')
    stream.write('  END_BOUNDARY_SET\n')
    stream.write('END_OUTPUT_&_POST_PROCESS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('BOUNDARY_CONDITIONS\n')
    stream.write('  PARAMETERS\n')
    stream.write('    INITIAL_CONDITIONS: CONSTANT, VALUE= 0.0, 0.0, 0.0\n')
    if icase == 'x-flow' or icase == 'y-flow':
        stream.write('    FIX_PRESSURE: AUTOMATIC\n')
    else:
        stream.write(f'    FIX_PRESSURE: WEAK, ON_NODE= {node}, VALUE= 0.0, MULTIPLICATIVE= 1.1\n')
    #stream.write(f'    PRESSURE: DARCY\n')
    stream.write('  END_PARAMETERS\n')
    stream.write('  CODES, NODES\n')
    if icase == 'x-flow' or icase == 'y-flow':
        # Flow in x-direction
        stream.write('    1 & 5      001 0.0 0.0 0.0\n')
        stream.write('    1 & 6      001 0.0 0.0 0.0\n')
        stream.write('    3 & 5      001 0.0 0.0 0.0\n')
        stream.write('    4 & 5      001 0.0 0.0 0.0\n')
        stream.write('    3 & 6      001 0.0 0.0 0.0\n')
        stream.write('    4 & 6      001 0.0 0.0 0.0\n')
        stream.write('    5          001 0.0 0.0 0.0\n')
        stream.write('    6          001 0.0 0.0 0.0\n')
        stream.write('    2 & 6      001 0.0 0.0 0.0\n')
        stream.write('    2 & 5      001 0.0 0.0 0.0\n')
        stream.write('    1 & 3 & 5  001 0.0 0.0 0.0\n')
        stream.write('    2 & 4 & 5  001 0.0 0.0 0.0\n')
        stream.write('    1 & 4 & 5  001 0.0 0.0 0.0\n')
        stream.write('    2 & 3 & 5  001 0.0 0.0 0.0\n')
        stream.write('    2 & 4 & 6  001 0.0 0.0 0.0\n')
        stream.write('    1 & 3 & 6  001 0.0 0.0 0.0\n')
        stream.write('    1 & 4 & 6  001 0.0 0.0 0.0\n')
        stream.write('    2 & 3 & 6  001 0.0 0.0 0.0\n')
    elif icase == 'z-flow':
        # Flow in z-direction
        stream.write('    1 & 5      000 0.0 0.0 0.0\n')
        stream.write('    1 & 6      000 0.0 0.0 0.0\n')
        stream.write('    3 & 5      000 0.0 0.0 0.0\n')
        stream.write('    4 & 5      000 0.0 0.0 0.0\n')
        stream.write('    3 & 6      000 0.0 0.0 0.0\n')
        stream.write('    2 & 3      000 0.0 0.0 0.0\n')
        stream.write('    4 & 6      000 0.0 0.0 0.0\n')
        stream.write('    2          000 0.0 0.0 0.0\n')
        stream.write('    5          000 0.0 0.0 0.0\n')
        stream.write('    1 & 3      000 0.0 0.0 0.0\n')
        stream.write('    3          000 0.0 0.0 0.0\n')
        stream.write('    4          000 0.0 0.0 0.0\n')
        stream.write('    1 & 4      000 0.0 0.0 0.0\n')
        stream.write('    2 & 4      000 0.0 0.0 0.0\n')
        stream.write('    6          000 0.0 0.0 0.0\n')
        stream.write('    2 & 6      000 0.0 0.0 0.0\n')
        stream.write('    1          000 0.0 0.0 0.0\n')
        stream.write('    2 & 5      000 0.0 0.0 0.0\n')
        stream.write('    1 & 3 & 5  000 0.0 0.0 0.0\n')
        stream.write('    2 & 4 & 5  000 0.0 0.0 0.0\n')
        stream.write('    1 & 4 & 5  000 0.0 0.0 0.0\n')
        stream.write('    2 & 3 & 5  000 0.0 0.0 0.0\n')
        stream.write('    2 & 4 & 6  000 0.0 0.0 0.0\n')
        stream.write('    1 & 3 & 6  000 0.0 0.0 0.0\n')
        stream.write('    1 & 4 & 6  000 0.0 0.0 0.0\n')
        stream.write('    2 & 3 & 6  000 0.0 0.0 0.0\n')
    stream.write('  END_CODES\n')
    #stream.write('  CODES, BOUNDARIES\n')
    #if icase == 'x-flow':
        # Flow in x-direction
        #stream.write(f'    1 2 {pressure:1.5e}\n')
        #stream.write('    2 2 0.0\n')
    #elif icase == 'y-flow':
        # Flow in y-direction
        #stream.write(f'    3 2 {pressure:1.5e}\n')
        #stream.write('    4 2 0.0\n')
    #elif icase == 'z-flow':
        # Flow in z-direction
        #stream.write(f'    5 2 {pressure:1.5e}\n')
        #stream.write('    6 2 0.0\n')
    #stream.write('  END_CODES\n')
    stream.write('END_BOUNDARY_CONDITIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    
    stream.close()

    
