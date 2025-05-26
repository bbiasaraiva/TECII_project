import ROOT
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 8_momentum_dist_z_per_particle.py <AmberTarget_Run_*.root>")
    sys.exit(1)

file_path  = sys.argv[1]
file_num = sys.argv[2]

OUTPUT_DIR = "../output/8_momentum_dist_z_per_particle"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file = ROOT.TFile.Open(file_path)
trkData_tree= file.Get("tracksData")

particles = {
    "muons": [ 13, -13],
    "pions": [211, -211, 111]
}
colors = {"muons": ROOT.kBlue, "pions": ROOT.kRed}

nbins, xmin, xmax = 200, -10.0, 201

individual_hst = {}
for x, pdg in particles.items():
    hist = ROOT.TH1D(f"h_pZ_{x}",
        f"{x} momentum Z distribution; pZ (GeV); entries",
        nbins, xmin, xmax)
    hist.SetLineColor(colors[x])
    hist.SetLineWidth(2)

    pdg_cut = " || ".join(f"particlePDG=={p}" for p in pdg) #NÃO ESTÁ A FUNCIONAR!!!!! 
    sel = f"({pdg_cut} && pZ_GeV!=0)" #AAAAAAAAAAA QUERO DAR DROP DE TODAS AS ENTRADAS COM GeV<=0

    trkData_tree.Draw(f"pZ_GeV>>{hist.GetName()}", sel, "goff")

    canva_ind = ROOT.TCanvas(f"c_pZ_{x}", x, 800, 600)
    hist.Draw("HIST")
    canva_ind.SetLogy()
    canva_ind.SetGrid()
    canva_ind.Update()
    canva_ind.SaveAs(os.path.join(OUTPUT_DIR, f"momentum_z_{x}_{file_num}.root"))
    canva_ind.SaveAs(os.path.join(OUTPUT_DIR, f"momentum_z_{x}_{file_num}.png"))

    individual_hst[x] = hist

c_all = ROOT.TCanvas("c_pZ_overlay", "momentum Z: muons & pions", 800, 600)
ymax = max(h.GetMaximum() for h in individual_hst.values())
frame = c_all.DrawFrame(xmin, 0.1, xmax, ymax, "momentum Z distribution: muons & pions;pZ (GeV);entries")
# frame.GetYaxis().SetTitleOffset(1.3)

for j, hist in individual_hst.items():
    hist.Draw("HIST SAME")

leg = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
for name, hist in individual_hst.items():
    leg.AddEntry(hist, name, "l")
leg.Draw()

c_all.SetLogy()
c_all.SetGrid()
c_all.Update()
c_all.SaveAs(os.path.join(OUTPUT_DIR, f"momentum_z_both_{file_num}.png"))
c_all.SaveAs(os.path.join(OUTPUT_DIR, f"momentum_z_both_{file_num}.root"))

file.Close()
