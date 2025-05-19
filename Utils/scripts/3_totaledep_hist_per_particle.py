import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 3_totaledep_hist_per_particle.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path  = sys.argv[1]
OUTPUT_DIR = "../output/3_totaledep_hist_per_particle"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file= ROOT.TFile.Open(file_path)
trkData_tree = file.Get("tracksData")

particles = {
    "muons":  [ 13, -13],
    "pions":  [211, -211, 111],
    "others": None
}
particle_name = list(particles.keys())
colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2]

detectors = [0,1,2,3]
sum_detect  = " + ".join(f"EdepDet{d}_keV" for d in detectors) # sums the 4 detec

nbins, xmin, xmax = 300, 0, 80000 #200000 VER ESCALA!!!!!

individual_hst = []
for x, name in enumerate(particle_name):
    pdg = particles[name]
    hist = ROOT.TH1D(f"h_total_{name}",
                     f"total tdep for {name};edep (keV);entries",
                     nbins, xmin, xmax)
    hist.SetLineColor(colors[x])
    hist.SetLineWidth(2)

    if pdg is not None:
        cut = " || ".join(f"particlePDG=={p}" for p in pdg)
        sel = f"({sum_detect})>0 && ({cut})"
    else:
        others_reject = [13, -13, 211, -211, 111]
        rej_cut = " && ".join(f"particlePDG!={p}" for p in others_reject)
        sel = f"({sum_detect})>0 && ({rej_cut})"

    trkData_tree.Draw(f"({sum_detect})>>{hist.GetName()}", sel, "goff")

    canva_ind = ROOT.TCanvas(f"c_{name}", name, 800, 600)
    hist.Draw("HIST")
    canva_ind.SetLogy()
    canva_ind.Update()
    canva_ind.SaveAs(os.path.join(OUTPUT_DIR, f"totaledep_{name}.png"))

    individual_hst.append(hist)

stack = ROOT.THStack("stack_total", "total edep per particle;edep (keV);entries")
for j, hist in enumerate(individual_hst):
    hist.SetColors(colors[j])
    stack.Add(hist)

canva_stack = ROOT.TCanvas("c_stack_total", "Stacked Total Edep", 800, 600)
stack.Draw("hist")
canva_stack.SetLogy()

leg = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
for k, name in enumerate(particle_name):
    leg.AddEntry(individual_hst[k], name, "l")
leg.Draw()

canva_stack.Update()
canva_stack.SaveAs(os.path.join(OUTPUT_DIR, "totaledep_stacked_per_particle.png"))

file.Close()
