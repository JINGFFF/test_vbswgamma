cmsrel CMSSW_10_2_18

cd CMSSW_10_2_18/src

cmsenv

git cms-init

git cms-merge-topic cms-egamma:EgammaPostRecoTools

git cms-addpkg RecoMET/METFilters

git clone -b 18_tight_for_analysis https://github.com/JINGFFF/VBSWG_Ntuple.git VAJets
