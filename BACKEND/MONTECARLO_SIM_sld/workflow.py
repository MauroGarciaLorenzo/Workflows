from PHASES.SAMPLERS import PYDOE, sampler
from PHASES.SIMULATIONS import simulation as sim
# from PHASES.POSTSIMULATION import postSimulation
# from PHASES.BEFORESIMULATION import parserSimulation as parserSim
from PHASES.POSTSIMULATION import postSimulationtest as postSimulation
from PHASES.BEFORESIMULATION import parserSimulationTest as parserSim
from pycompss.api.api import compss_wait_on
import os
import yaml


def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(phases.get("sampler"), data.get("problem"), execution_folder, data.get("input"),
                           phases.get("sim"), data.get("outputs"), data_folder, )
    return


def workflow_execution(samplerData, problem, execution_folder, input, simType, outputs, data_folder):
    sample_set = sampler.sampler(samplerData.get("name"), problem)
    sample_set = compss_wait_on(sample_set)
    names = sampler.get_names(samplerData.get("name"), problem)
    mesh_folder=None
    templateDom_folder=None
    templateSld_folder=None
    mesh = input.get("mesh", [])
    mesh_folder = ""
    for item in mesh:
        if isinstance(item, dict) and 'folder' in item:
            mesh_folder = item['folder']
            break  # Exit the loop after finding the first 'folder'

    template_sld = input.get("template_sld", [])
    templateSld_folder = ""
    for item in template_sld:
        if isinstance(item, dict) and 'folder' in item:
            templateSld_folder = item['folder']
            break  # Exit the loop after finding the first 'folder'

    template_dom = input.get("template_dom", [])
    templateDom_folder = ""
    for item in template_dom:
        if isinstance(item, dict) and 'folder' in item:
            templateDom_folder = item['folder']
            break  # Exit the loop after finding the first 'folder'

    # Now use these folder paths as needed
    input_source = os.path.join(data_folder, mesh_folder) if mesh_folder else None
    templateSld = os.path.join(data_folder, templateSld_folder) if templateSld_folder else None
    templateDom = os.path.join(data_folder, templateDom_folder) if templateDom_folder else None


    print("input_source: "+input_source)
    print("templateSld: " + templateSld)
    print("templateDom: " + templateDom)
    parent_directory, original_name = os.path.split(input_source)
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    y = []
    type_sim = simType.get("type")

    for i in range(problem.get("n_samples")):
        values = sample_set[i, :]
        simulation_wdir = execution_folder + "/SIMULATIONS/" + original_name + "-s" + str(i) + "/"
        if not os.path.isdir(simulation_wdir):
            os.makedirs(simulation_wdir)
        nameSim = original_name + "-s" + str(i)
        variables_sld = sampler.vars_func(samplerData.get("name"), problem, values, problem.get("variables-fixed"),
                                          names)
        out1 = parserSim.prepare_data(type_sim, input_source, templateSld, simulation_wdir, original_name, nameSim,
                                      variables_sld)
        out3 = parserSim.prepare_dom_file(type_sim, templateDom, simulation_wdir, nameSim, out1)
        out = sim.run_sim(type_sim, simulation_wdir, nameSim, out3=out3)

        new_y = postSimulation.collect(type_sim, simulation_wdir, nameSim, out)
        y.append(new_y)

        """parserSim.prepare_data(type_sim, mesh, templateSld, simulation_wdir, original_name, nameSim, variables_sld)
        parserSim.prepare_dom_file(type_sim, templateDom, simulation_wdir, nameSim)
        sim.run_sim(type_sim, simulation_wdir, nameSim)
        new_y = postSimulation.collect(type_sim, simulation_wdir, nameSim)
        y.append(new_y)"""
    postSimulation.write_file(type_sim, results_folder, y, outputs=outputs)
    return
