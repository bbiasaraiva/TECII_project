import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 task2_stack.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path = sys.argv[1]
OUTPUT_DIR = "../output/2_edep_hist_per_particle"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file= ROOT.TFile.Open(file_path)
trkData_tree  = file.Get("tracksData")

particles = {
    "muons":  [13, -13],
    "pions":  [211, -211, 111],
    "others": None
}

detectors = [0,1,2,3]
det_colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2]

nbins, xmin, xmax = 200, 0, 8000

for x, pdgs in particles.items():
    individual_hst = []
    for i, det in enumerate(detectors):
        hist = ROOT.TH1D(f"hist_{x.lower()}_det{det}",
                      f"{x} in det {det};edep (keV);entries",
                      nbins, xmin, xmax)
        if x != "others":
            cut = " || ".join(f"particlePDG=={p}" for p in pdgs)
            sel = f"(EdepDet{det}_keV>0) && ({cut})"
        else:
            others_reject = [13, -13, 211, -211, 111]
            rc = " && ".join(f"particlePDG!={p}" for p in others_reject)
            sel = f"EdepDet{det}_keV>0 && {rc}"

        trkData_tree.Draw(f"EdepDet{det}_keV>>{hist.GetName()}", sel, "goff")
        #h.SetFillColorAlpha(det_colors[i], 0.6)
        hist.SetLineColor(det_colors[i])
        hist.SetLineWidth(2)
        individual_hst.append(hist)

    stack = ROOT.THStack(f"stack_{x.lower()}", 
                         f"{x}: energy deposition (stacked);edep (keV);entries")
    for h in individual_hst:
        stack.Add(h)

    canva = ROOT.TCanvas(f"c_{x.lower()}", x, 800, 600)
    stack.Draw("hist")
    canva.SetLogy()

    leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    for i, h in enumerate(individual_hst):
        leg.AddEntry(h, f"detector {detectors[i]}", "l")
    leg.Draw()

    canva.Update()
    canva.SaveAs(os.path.join(OUTPUT_DIR, f"stack_{x.lower()}.png"))

file.Close()
