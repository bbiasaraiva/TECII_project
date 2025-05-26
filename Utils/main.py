import multiprocessing
import os

global WORKING_DIRECTORY
WORKING_DIRECTORY = os.getcwd()



def work(n, script):
    file_num = n 

    
    scriptNum = int(script.split("_")[0])  # Extract the script number from the filename
    possibleNames = {
    1: [f"edep_per_detector*_{file_num}.root", f"energy_deposition_all_detectors_{file_num}.root"],
    2: [f"stack_*_{file_num}.root",f"stack_detector*_particles_{file_num}.root"],
    3: [f"totaledep_*_{file_num}.root",f"totaledep_stacked_per_particle_{file_num}.root"],
    4: [f"hadronic_vertex_z_*_{file_num}.root",f"hadronic_vertex_z_all_{file_num}.root"],
    5: [f"hits_xy_all_detectors_{file_num}.root"],
    6: [f"hits_xy_charged_allDetec_{file_num}.root",f"hits_xy_neutral_allDetec_{file_num}.root"],
    7: [f"hits_time_det*_{file_num}.root",f"hits_time_stacked_{file_num}.png",f"hits_time_stacked_zoomed_{file_num}.root"],
    8: [f"momentum_z_*_{file_num}.root",f"momentum_z_both_{file_num}.root"],
    9: [f"momentum_z_*_pions_{file_num}.root",f"momentum_z_both_prim_sec_pions_{file_num}.root"]
    }
    
    outDir = {
        1: '../output/1_edep_hist_per_detector',
        2: '../output/2_edep_hist',
        3: '../output/3_totaledep_hist_per_particle',
        4: '../output/4_hadronic_vertex_z',
        5: '../output/5_hits_distr_xy_per_detector',
        6: '../output/6_hits_distr_xy_per_particle',
        7: '../output/7_hits_temporal_distr_per_detector',
        8: '../output/8_momentum_dist_z_per_particle',
        9: '../output/9_momentum_dist_z_prim_sec'
    }


    names = [f"{outDir[scriptNum]}/{x}" for x in possibleNames[scriptNum]]
    strang = str(names).replace("'", "").replace("[", "").replace("]", "").replace(",","")

    print(strang)
    fname = WORKING_DIRECTORY + "/AmberTarget_Run_" + str(n) + ".root" 
    os.system("python3 scripts/" + script + " " + fname + " " + str(n))
    #print(f"hadd -f {outDir[scriptNum]}/AmberTargetDone_{n}" + )
    os.system(f"hadd -f {outDir[scriptNum]}/AmberTargetDone_{n}.root {strang}" )


def main():
    toRunNow = []
    scripts = {
            1: "1_edep_hist_per_detector.py",
            2: "2_edep_hist.py",
            3: "3_totaledep_hist_per_particle.py",
            4: "4_hadronic_vertex_z.py",
            5: "5_hits_distr_xy_per_detector.py",
            6: "6_hits_distr_xy_per_particle.py",
            7: "7_hits_temporal_distr_per_detector.py",
            8: "8_momentum_dist_z_per_particle.py",
            9: "9_momentum_dist_z_prim_sec.py",
            }

    print("Running main.py script...")
    exitConditiom = False
    exitAdding = False
    
    while not exitConditiom:
        print("Options:")    
        print("\t1. Run all scripts")        
        print("\t2. Choose a script to run")  
        print(f"\t0. Run scripts{toRunNow} or empty to exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            toRunNow = list(scripts.keys())
            exitConditiom = True

        elif choice == "2":
            print("Available scripts:")
            for key, value in scripts.items():
                print(f"{key}. {value}")
            
            while not exitAdding:
                print("Scripts to run:")
                toRunNow.sort()
                print(toRunNow)

                scriptChoice = input("Enter the number of the script you want to run (0 to exit):")
                if scriptChoice == "0":
                    exitAdding = True
                    break
                try:
                    scriptChoice = int(scriptChoice)
                    if scriptChoice in scripts and scriptChoice not in toRunNow :
                        toRunNow.append(scriptChoice)
                    elif scriptChoice in scripts:
                        toRunNow.remove(scriptChoice)
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == "0":
            exitConditiom = True
        else:
            print("Invalid choice. Please try again.")

    for i in toRunNow:
        print (f"Running script {i}: {scripts[i]}")
        cpus = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpus)
        tasks = range(0,4)
        location = scripts[i]
        tasks = [(n, location) for n in range(4)]  # List of (n, script) tuples
        pool.starmap_async(work, tasks)

        pool.close()
        pool.join()


main()