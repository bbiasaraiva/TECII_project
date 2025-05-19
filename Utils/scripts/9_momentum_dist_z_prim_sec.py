import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 9_momentum_dist_z_prim_sec.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path  = sys.argv[1]
OUTPUT_DIR = "../output/9_momentum_dist_z_prim_sec"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file= ROOT.TFile.Open(file_path)
trkData_tree = file.Get("tracksData")

pion_pdgs = [211, -211, 111] #pgds code for pions
categories = {
    "primary":   "IsPrimary==1",
    "secondary": "IsPrimary!=1"}

nbins, xmin, xmax = 200, -10.0, 250.0

individual_hst = {}
for isPrim, isPrim_cut in categories.items():
    h = ROOT.TH1D(
        f"h_pZ_{isPrim}",
        f"{isPrim} Pions: pZ distribution; pZ (GeV); entries",
        nbins, xmin, xmax)
    h.SetLineWidth(2)
    h.SetLineColor(ROOT.kRed if isPrim=="primary" else ROOT.kBlue)

    pdg_cut = " || ".join(f"particlePDG=={p}" for p in pion_pdgs)
    sel     = f"({pdg_cut}) && {isPrim_cut}"
    trkData_tree.Draw(f"pZ_GeV>>{h.GetName()}", sel, "goff")

    canva_ind = ROOT.TCanvas(f"c_{isPrim}", isPrim, 800, 600)
    h.Draw("HIST")
    canva_ind.SetLogy()
    canva_ind.Update()
    canva_ind.SaveAs(os.path.join(OUTPUT_DIR, f"momentum_z_{isPrim}_pions.png"))

    individual_hst[isPrim] = h

c_both = ROOT.TCanvas("c_overlay", "Primary vs Secondary Pions pZ", 800, 600)
ymax = max(h.GetMaximum() for h in individual_hst.values()) * 1.2
frame = c_both.DrawFrame(
    xmin, 0.1, xmax, ymax,"pions pZ distribution; pZ (GeV); entries")

for h in individual_hst.values():
    h.Draw("HIST SAME")

leg = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
leg.AddEntry(individual_hst["primary"],   "Primary",   "l")
leg.AddEntry(individual_hst["secondary"], "Secondary", "l")
leg.Draw()

c_both.SetLogy()
c_both.Update()
c_both.SaveAs(os.path.join(OUTPUT_DIR, "momentum_z_both_prim_sec_pions.png"))

file.Close()
