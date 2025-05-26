import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 6_hits_distr_xy_per_particle.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path = sys.argv[1]
file_num = sys.argv[2]

OUTPUT_DIR = "../output/6_hits_distr_xy_per_particle"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file = ROOT.TFile.Open(file_path)
hits_tree = file.Get("Hits")

detectors = [0,1,2,3]

nbins = 200
xmin, xmax = -20.0, 20.0
ymin, ymax = -20.0, 20.0

h_charged = {}
h_neutral = {}

for det in detectors:
    # charged
    name_charged = f"h2_charged_det{det}"
    h2_ch = ROOT.TH2D(name_charged, f"det {det} charged hits;X (cm);Y (cm)",
        nbins, xmin, xmax,
        nbins, ymin, ymax)
    cut_ch = f"detectorID=={det} && particleCharge!=0"
    hits_tree.Draw(f"hitPosY_cm:hitPosX_cm>>{name_charged}", cut_ch, "goff")
    h2_ch.SetStats(False)
    h_charged[det] = h2_ch

    # neutral
    name_neutral  = f"h2_neutral_det{det}"
    h2_neutral    = ROOT.TH2D(name_neutral, f"det {det} neutral hits;X (cm);Y (cm)",
        nbins, xmin, xmax,
        nbins, ymin, ymax)
    cut_neutral   = f"detectorID=={det} && particleCharge==0"
    hits_tree.Draw(f"hitPosY_cm:hitPosX_cm>>{name_neutral}", cut_neutral, "goff")
    h2_neutral.SetStats(False)
    h_neutral[det] = h2_neutral

#CHARGED hits
c_charged = ROOT.TCanvas("c_charged", "charged hits XY per detector", 1200, 1200)
c_charged.Divide(2,2)
for x, det in enumerate(detectors):
    c_charged.cd(x+1)
    ROOT.gPad.SetRightMargin(0.15)
    h_charged[det].Draw("COLZ")
c_charged.Update()
c_charged.SaveAs(os.path.join(OUTPUT_DIR, f"hits_xy_charged_allDetec_{file_num}.root"))
c_charged.SaveAs(os.path.join(OUTPUT_DIR, f"hits_xy_charged_allDetec_{file_num}.png"))

#NEUTRAL hits
c_neutral = ROOT.TCanvas("c_neutral", "neutral hits XY per detector", 1200, 1200)
c_neutral.Divide(2,2)
for idx, det in enumerate(detectors):
    c_neutral.cd(idx+1)
    ROOT.gPad.SetRightMargin(0.15)
    h_neutral[det].Draw("COLZ")
c_neutral.Update()
c_neutral.SaveAs(os.path.join(OUTPUT_DIR, f"hits_xy_neutral_allDetec_{file_num}.root"))
c_neutral.SaveAs(os.path.join(OUTPUT_DIR, f"hits_xy_neutral_allDetec_{file_num}.png"))
file.Close()
