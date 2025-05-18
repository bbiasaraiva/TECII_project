import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 exercise4_vertex_z.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path  = sys.argv[1]
OUTPUT_DIR = "../output/4_hadronic_vertex_z"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file = ROOT.TFile.Open(file_path)
vertex_tree = file.Get("hadronicVertex")

isPrimary = {"primary": "IsPrimary==1", "secondary": "IsPrimary!=1"}
category_names = list(isPrimary.keys())
colors = [ROOT.kRed, ROOT.kBlue]

nbins = 300
zmin = vertex_tree.GetMinimum("vertexPosZ_cm")
zmax = vertex_tree.GetMaximum("vertexPosZ_cm")

#more focuesed -- analyse later
# zmin =-300
# zmax = -100

individual_hst = []
for x, name in enumerate(category_names):
    hist = ROOT.TH1D(
        f"h_vertex_{name}",
        f"{name} hadronic vertices; Z (cm); entries",
        nbins, zmin, zmax)
    vertex = f"vertexPosZ_cm>={zmin} && vertexPosZ_cm<={zmax} && {isPrimary[name]}"
    vertex_tree.Draw(f"vertexPosZ_cm>>{hist.GetName()}", vertex, "goff")
    hist.SetLineColor(colors[x])
    hist.SetLineWidth(2)
    individual_hst.append(hist)

    canva_ind = ROOT.TCanvas(f"c_vertex_{name}", f"{name} vertices", 800, 600)
    hist.Draw("hist")
    canva_ind.SetLogy()
    canva_ind.Update()
    canva_ind.SaveAs(os.path.join(OUTPUT_DIR, f"hadronic_vertex_z_{name}.png"))

canva_all = ROOT.TCanvas("c_vertex_z", "hadronic vertex", 800, 600)

stack = ROOT.THStack("h_vertex_stack", "hadronic vertices; Z (cm); entries")
for hist in individual_hst:
    stack.Add(hist)

stack.Draw("hist NOSTACK")
stack.SetMinimum(0.1)

legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
for j, hist in enumerate(individual_hst):
    legend.AddEntry(hist, category_names[j], "l")

legend.Draw()
canva_all.SetLogy()
canva_all.Update()
canva_all.SaveAs(os.path.join(OUTPUT_DIR, "hadronic_vertex_z_all.png"))

file.Close()