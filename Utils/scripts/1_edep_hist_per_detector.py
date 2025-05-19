import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 1_edep_hist_per_detector.py <path_ROOT_file>")
    sys.exit(1)

file_path = sys.argv[1]

OUTPUT_DIR = '../output/1_edep_hist_per_detector'
os.makedirs(OUTPUT_DIR, exist_ok=True)

file = ROOT.TFile.Open(file_path)

tree = file.Get("edep_Per_Event")

colors = [ROOT.kGreen+2, ROOT.kBlue, ROOT.kMagenta, ROOT.kBlack]
detectors = [0, 1, 2, 3]

nbins, xmin, xmax = 300, 0, 600000

individual_hst = []
for i in detectors:
    hist = ROOT.TH1D(f"hist_energy_dep_{i}", f"energy deposition: detector {i};energy (keV);counts", nbins, xmin, xmax)
    tree.Draw(f"detector{i}>>hist_energy_dep_{i}", f"detector{i}>0.0", "goff")
    individual_hst.append(hist)
    #save canvas 
    ind_canvas = ROOT.TCanvas(f"hist for detector {i}", f"Detector {i}", 800, 600)
    hist.SetLineColor(colors[i])
    hist.SetLineWidth(2)
    hist.Draw("HIST")
    ind_canvas.SetLogy()
    ind_canvas.Update()
    #c_ind.SaveAs(f"energy_deposition_detector_{det}.png")
    ind_canvas.SaveAs(f"{OUTPUT_DIR}/edep_per_detector{i}.png")


all_hist = ROOT.TCanvas("all_hist", "all detectors - edep", 1000, 800)
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

max_y = max([h.GetMaximum() for h in individual_hst])
frame = all_hist.DrawFrame(0, 0.1, 600000, max_y * 1.5, "energy deposition: all detectors;energy (keV);counts")

for det, h in zip(detectors, individual_hst):
    h.SetLineColor(colors[det])
    h.Draw("HIST SAME")  #to overlay and shos all together
    legend.AddEntry(h, f"Detector {det}", "l")

legend.Draw()
all_hist.SetGrid()
all_hist.SetLogy() 
all_hist.Update()
all_hist.SaveAs(f"{OUTPUT_DIR}/energy_deposition_all_detectors.png")

file.Close()
