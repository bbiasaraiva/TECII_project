import multiprocessing
import sys
import os

global WORKING_DIRECTORY
WORKING_DIRECTORY = os.getcwd()


def work(n, script):
    fname = WORKING_DIRECTORY + "/AmberTarget_Run_" + str(n) + ".root" 
    os.system("python3 scripts/" + script + " " + fname + " " + str(n))

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
        print("\t3. Exit")
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
                    exitConditiom = True
                    break
                try:
                    scriptChoice = int(scriptChoice)
                    if scriptChoice in scripts:
                        toRunNow.append(scriptChoice)
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        elif choice == "3":
            exitConditiom = True
        else:
            print("Invalid choice. Please try again.")

    print("Scripts to run:", toRunNow)
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