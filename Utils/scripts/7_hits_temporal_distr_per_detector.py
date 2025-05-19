import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 7_hits_temporal_distr_per_detector.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path = sys.argv[1]
OUTPUT_DIR = "../output/7_hits_temporal_distr_per_detector"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file = ROOT.TFile.Open(file_path)
hits_tree = file.Get("Hits")

nbins = 200
tmin_raw = hits_tree.GetMinimum("particleHitTime_ns")
tmax = hits_tree.GetMaximum("particleHitTime_ns")
pad = 0.05 * (tmax - tmin_raw) #only to get bettr visualization
tmin = tmin_raw - pad
tmax    *= 1.05   # also for better visualization

detectors = [0,1,2,3]
colors = [ROOT.kGreen+2, ROOT.kBlue, ROOT.kMagenta, ROOT.kBlack]
h_time = {}

for det, col in zip(detectors, colors):
    h = ROOT.TH1D( f"h_time_det{det}", f"detector {det}: hit time distribution;time (ns);hits",
        nbins, tmin, tmax)
    
    hits_tree.Draw(
        f"particleHitTime_ns>>{h.GetName()}", f"detectorID=={det}","goff")
    h.SetLineColor(col)
    h.SetLineWidth(2)
    h_time[det] = h

    canva_ind = ROOT.TCanvas(f"c_time_det{det}", f"detector {det} hit times", 800, 600)
    h.Draw("HIST")
    canva_ind.SetLogy()
    canva_ind.Update()
    canva_ind.SaveAs(os.path.join(OUTPUT_DIR, f"hits_time_det{det}.png"))

stack = ROOT.THStack("stack_time", "hit time distribution per detector;time (ns);hits")
for det, hist in h_time.items():
    hist.SetColors(colors[det])
    stack.Add(hist)

c_stacked = ROOT.TCanvas("c_time_stack", "stacked hit times", 800, 600)
stack.Draw("hist")
c_stacked.SetLogy()

leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
for det, h in h_time.items():
    leg.AddEntry(h, f"detector {det}", "l")
leg.Draw()

c_stacked.Update()
c_stacked.SaveAs(os.path.join(OUTPUT_DIR, "hits_time_stacked.png"))

file.Close()