import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 5_hits_distr_xy_per_detector.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path  = sys.argv[1]
OUTPUT_DIR = "../output/5_hits_distr_xy_per_detector"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file= ROOT.TFile.Open(file_path)
hits_tree = file.Get("Hits")

detectors = [0,1,2,3] 

# we're gonna use ±20 cm
nbins  = 200
xmin, xmax = -20.0, 20.0
ymin, ymax = -20.0, 20.0

for det in detectors:
    h2 = ROOT.TH2D(
        f"h2_det{det}", f"detector {det}: hits in X vs Y;X (cm);Y (cm)",
        nbins, xmin, xmax,
        nbins, ymin, ymax)
    
    hits_tree.Draw(
        f"hitPosY_cm:hitPosX_cm>>{h2.GetName()}",
        f"detectorID=={det}",
        "goff")

    h2.SetStats(False)
    c = ROOT.TCanvas(f"c_det{det}", f"det {det} hits XY", 800, 600)
    ROOT.gPad.SetRightMargin(0.15)
    h2.Draw("COLZ")     # linear color map

    c.Update()
    c.SaveAs(os.path.join(OUTPUT_DIR, f"hits_xy_det{det}.png"))

file.Close()
