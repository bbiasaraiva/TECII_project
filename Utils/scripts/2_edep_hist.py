import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 2_edep_hist.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path = sys.argv[1]
file_num = sys.argv[2]

OUTPUT_DIR = "../output/2_edep_hist"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file= ROOT.TFile.Open(file_path)
trkData_tree  = file.Get("tracksData")

particles = {
    "muons":  [13, -13],
    "pions":  [211, -211, 111],
    "others": None
}

detectors = [0,1,2,3]
det_colors = [ROOT.kGreen+2, ROOT.kBlue, ROOT.kMagenta, ROOT.kBlack]
part_colors = {
    "muons":   ROOT.kBlue,
    "pions":   ROOT.kRed,
    "others":  ROOT.kGreen+2 }


nbins, xmin, xmax = 200, 0, 8000

# stack per particle
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
        hist.SetLineColor(det_colors[i])
        hist.SetLineWidth(2)
        individual_hst.append(hist)

    stack = ROOT.THStack(f"stack_{x.lower()}", 
                         f"{x}: energy deposition (stacked);edep (keV);entries")
    for h in individual_hst:
        stack.Add(h)

    canva = ROOT.TCanvas(f"c_{x.lower()}", x, 800, 600)
    stack.Draw("nostack hist")
    canva.SetLogy()

    leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    for i, h in enumerate(individual_hst):
        leg.AddEntry(h, f"detector {detectors[i]}", "l")
    leg.Draw()

    canva.SetGridx()
    canva.SetGridy()
    canva.Update()
    canva.SaveAs(os.path.join(OUTPUT_DIR, f"stack_{x.lower()}_{file_num}.root"))
    canva.SaveAs(os.path.join(OUTPUT_DIR, f"stack_{x.lower()}_{file_num}.png"))

# stack per detector
for det in detectors:
    hist_part = {}
    for p, pdg_list in particles.items():
        h = ROOT.TH1D(f"h_{p}_det{det}",
                      f"{p} in det {det};edep (keV);entries",
                      nbins, xmin, xmax)
        if pdg_list is not None:
            cut= " || ".join(f"particlePDG=={p}" for p in pdg_list)
            sel =f"EdepDet{det}_keV>0 && ({cut})"
        else:
            reject = [13, -13, 211, -211, 111]
            rc = " && ".join(f"particlePDG!={p}" for p in reject)
            sel = f"EdepDet{det}_keV>0 && {rc}"

        trkData_tree.Draw(f"EdepDet{det}_keV>>{h.GetName()}", sel, "goff")
        h.SetLineColor(part_colors[p])
        h.SetLineWidth(2)
        hist_part[p] = h

    stack = ROOT.THStack(f"stack_det{det}", 
                         f"detector {det}: edep by particle;edep (keV);entries")
    for name in particles:
        stack.Add(hist_part[name])

    c = ROOT.TCanvas(f"c_det{det}_by_particle", f"detector {det}: edep by particle", 800, 600)
    stack.Draw("nostack hist")
    c.SetLogy()

    leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    for name in particles:
        leg.AddEntry(hist_part[name], name, "l")
    leg.Draw()

    c.SetGrid()
    c.Update()
    c.SaveAs(os.path.join(OUTPUT_DIR, f"stack_detector{det}_particles_{file_num}.root"))
    c.SaveAs(os.path.join(OUTPUT_DIR, f"stack_detector{det}_particles_{file_num}.png"))
file.Close()
