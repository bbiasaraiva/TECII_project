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
    canva_ind.SetGrid()
    canva_ind.Update()
    canva_ind.SaveAs(os.path.join(OUTPUT_DIR, f"hits_time_det{det}.png"))

stack = ROOT.THStack("stack_time", "hit time distribution per detector;time (ns);hits")
for det, hist in h_time.items():
    hist.SetColors(colors[det])
    stack.Add(hist)

c_stacked = ROOT.TCanvas("c_time_stack", "stacked hit times", 800, 600)
stack.Draw("nostack hist")
c_stacked.SetLogy()

leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
for det, h in h_time.items():
    leg.AddEntry(h, f"detector {det}", "l")
leg.Draw()

c_stacked.SetGrid()
c_stacked.Update()
c_stacked.SaveAs(os.path.join(OUTPUT_DIR, "hits_time_stacked.png"))

#zoom a part of the stacked hists
nbins_zoom = 300
tmin_zoom = 0
tmax_zoom = 20         

h_time_zoom = {}
for det, col in zip(detectors, colors):
    h_zoom = ROOT.TH1D(f"h_time_alt_det{det}", f"detector {det} (alt): hit time; time (ns); hits",
        nbins_zoom, tmin_zoom, tmax_zoom)
    
    hits_tree.Draw(f"particleHitTime_ns>>{h_zoom.GetName()}", f"detectorID=={det}", "goff")
    
    h_zoom.SetLineColor(col)
    h_zoom.SetLineWidth(2)
    h_time_zoom[det] = h_zoom

# stack the alternative histograms
alt_stack = ROOT.THStack("stack_time_alt",
    "hit time distribution zoomed ; time (ns); hits"
)

for det in detectors:
    alt_stack.Add(h_time_zoom[det])

c_alt = ROOT.TCanvas("c_time_stack_zoomed", "stacked hit times zoomed", 800, 600)
alt_stack.Draw("nostack hist")
c_alt.SetLogy()
c_alt.SetGridx()
c_alt.SetGridy()

leg_alt = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
for det, hist in h_time_zoom.items():
    leg_alt.AddEntry(hist, f"detector {det}", "l")
leg_alt.Draw()

c_alt.Update()
c_alt.SaveAs(os.path.join(OUTPUT_DIR, "hits_time_stacked_zoomed.png"))   

file.Close()