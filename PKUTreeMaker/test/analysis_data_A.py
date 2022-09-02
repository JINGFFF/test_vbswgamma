import FWCore.ParameterSet.Config as cms

process = cms.Process( "TEST" )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
				     SkipEvent = cms.untracked.vstring('ProductNotFound'))
corrJetsOnTheFly = True
runOnMC = False
chsorpuppi = True  # AK4Chs or AK4Puppi
#****************************************************************************************************#
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("RecoTracker.CkfPattern.CkfTrackCandidates_cff")
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")

from Configuration.AlCa.GlobalTag import GlobalTag
if runOnMC:
   process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v21'
elif not(runOnMC):
   process.GlobalTag.globaltag = '102X_dataRun2_v13'

##########			                                                             
hltFiltersProcessName = 'RECO'
if runOnMC:
   hltFiltersProcessName = 'PAT' #'RECO'
reducedConversionsName = 'RECO'
if runOnMC:
   reducedConversionsName= 'PAT' #'RECO'

process.load("VAJets.PKUCommon.goodMuons_cff")
process.load("VAJets.PKUCommon.goodElectrons_cff")
process.load("VAJets.PKUCommon.goodPhotons_cff")
process.load("VAJets.PKUCommon.leptonicW_cff")
process.load("VAJets.PKUCommon.goodJets_cff")

#for egamma smearing
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       era="2018-Prompt",
		       runEnergyCorrections=False#True: do egamma_modification
		      )
# If Update
process.goodMuons.src = "slimmedMuons"
process.goodElectrons.src = "slimmedElectrons"
process.goodPhotons.src = "slimmedPhotons"
process.Wtoenu.MET  = "slimmedMETs"
process.Wtomunu.MET = "slimmedMETs"

# jerc uncer 2017/5/7
if chsorpuppi:
        jLabel = "slimmedJets"
        jetAlgo    = 'AK4PFchs'
else:
      jLabel = "slimmedJetsPuppi"
      jetAlgo    = 'AK4PFPuppi'

jer_era = "Autumn18_V19_MC"
#jer_era = "Fall17_17Nov2017_V32_MC"
triggerResultsLabel      = "TriggerResults"
triggerSummaryLabel      = "hltTriggerSummaryAOD"
hltProcess = "HLT"
if runOnMC:
   jecLevelsAK4chs = [
          'Autumn18_V19_MC_L1FastJet_AK4PFchs.txt',
          'Autumn18_V19_MC_L2Relative_AK4PFchs.txt',
          'Autumn18_V19_MC_L3Absolute_AK4PFchs.txt'
    ]
   jecLevelsAK4puppi = [
          'Autumn18_V19_MC_L1FastJet_AK4PFPuppi.txt',
          'Autumn18_V19_MC_L2Relative_AK4PFPuppi.txt',
          'Autumn18_V19_MC_L3Absolute_AK4PFPuppi.txt'
    ]
else:
   jecLevelsAK4chs = [
          'Autumn18_RunA_V19_DATA_L1FastJet_AK4PFchs.txt',
          'Autumn18_RunA_V19_DATA_L2Relative_AK4PFchs.txt',
          'Autumn18_RunA_V19_DATA_L3Absolute_AK4PFchs.txt',
          'Autumn18_RunA_V19_DATA_L2L3Residual_AK4PFchs.txt'
    ]
   jecLevelsAK4puppi = [
          'Autumn18_RunA_V19_DATA_L1FastJet_AK4PFPuppi.txt',
          'Autumn18_RunA_V19_DATA_L2Relative_AK4PFPuppi.txt',
          'Autumn18_RunA_V19_DATA_L3Absolute_AK4PFPuppi.txt',
          'Autumn18_RunA_V19_DATA_L2L3Residual_AK4PFPuppi.txt'
    ]


process.JetUserData = cms.EDProducer(
   'JetUserData',
   jetLabel          = cms.InputTag(jLabel),
   rho               = cms.InputTag("fixedGridRhoFastjetAll"),
   coneSize          = cms.double(0.4),
   getJERFromTxt     = cms.bool(False),
   jetCorrLabel      = cms.string(jetAlgo),
   jerLabel          = cms.string(jetAlgo),
   resolutionsFile   = cms.string(jer_era+'_PtResolution_'+jetAlgo+'.txt'),
   scaleFactorsFile  = cms.string(jer_era+'_SF_'+jetAlgo+'.txt'),
   ### TTRIGGER ###
   triggerResults = cms.InputTag(triggerResultsLabel,"",hltProcess),
   triggerSummary = cms.InputTag(triggerSummaryLabel,"",hltProcess),
   hltJetFilter       = cms.InputTag("hltPFHT"),
   hltPath            = cms.string("HLT_PFHT800"),
   hlt2reco_deltaRmax = cms.double(0.2),
   candSVTagInfos         = cms.string("pfInclusiveSecondaryVertexFinder"), 
   jecAK4chsPayloadNames_jetUserdata = cms.vstring( jecLevelsAK4chs ),
   vertex_jetUserdata = cms.InputTag("offlineSlimmedPrimaryVertices"),
   )
#jerc uncer Meng
process.load("VAJets.PKUCommon.goodJets_cff") 
if chsorpuppi:
      #process.goodAK4Jets.src = "slimmedJets"
      process.goodAK4Jets.src = "JetUserData"
else:
      process.goodAK4Jets.src = "slimmedJetsPuppi"
 
#process.goodOfflinePrimaryVertex = cms.EDFilter("VertexSelector",
#                                       src = cms.InputTag("offlineSlimmedPrimaryVertices"),
#                                       cut = cms.string("chi2!=0 && ndof >= 4.0 && abs(z) <= 24.0 && abs(position.Rho) <= 2.0"),
#                                       filter = cms.bool(False)
#                                       )

WBOSONCUT = "pt > 0.0"

process.leptonicVSelector = cms.EDFilter("CandViewSelector",
                                       src = cms.InputTag("leptonicV"),
                                       cut = cms.string( WBOSONCUT ), 
                                       filter = cms.bool(False)
                                       )

process.leptonicVFilter = cms.EDFilter("CandViewCountFilter",
                                       src = cms.InputTag("leptonicV"),
                                       minNumber = cms.uint32(0),
                                       #filter = cms.bool(False)
                                       )


process.leptonSequence = cms.Sequence(process.muSequence +
#		                      process.egammaPostRecoSeq*process.slimmedElectrons*process.slimmedPhotons+
                                      process.eleSequence +
                                      process.leptonicVSequence +
                                      process.leptonicVSelector +
                                      process.leptonicVFilter )

process.jetSequence = cms.Sequence(process.NJetsSequence)


process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.load("RecoMET.METFilters.BadChargedCandidateFilter_cfi")
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.metfilterSequence = cms.Sequence(process.BadPFMuonFilter+process.BadChargedCandidateFilter)

if chsorpuppi:
      ak4jecsrc = jecLevelsAK4chs
else:
      ak4jecsrc = jecLevelsAK4puppi

process.load("RecoEgamma/PhotonIdentification/photonIDValueMapProducer_cff")
#from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD 
## Example 1: If you only want to re-correct MET and get the proper uncertainties [e.g. when updating JEC]
#runMetCorAndUncFromMiniAOD(process,
#                           isData=False,
#                           )
   
# EcalBadCalibFiler
process.load('RecoMET.METFilters.ecalBadCalibFilter_cfi')

baddetEcallist = cms.vuint32(
    [872439604,872422825,872420274,872423218,
     872423215,872416066,872435036,872439336,
     872420273,872436907,872420147,872439731,
     872436657,872420397,872439732,872439339,
     872439603,872422436,872439861,872437051,
     872437052,872420649,872422436,872421950,
     872437185,872422564,872421566,872421695,
     872421955,872421567,872437184,872421951,
     872421694,872437056,872437057,872437313])


process.ecalBadCalibReducedMINIAODFilter = cms.EDFilter(
    "EcalBadCalibFilter",
    EcalRecHitSource = cms.InputTag("reducedEgamma:reducedEERecHits"),
    ecalMinEt        = cms.double(50.),
    baddetEcal    = baddetEcallist, 
    taggingMode = cms.bool(True),
    debug = cms.bool(False)
    )

process.treeDumper = cms.EDAnalyzer("PKUTreeMaker",
                                    originalNEvents = cms.int32(1),
                                    crossSectionPb = cms.double(1),
                                    targetLumiInvPb = cms.double(1.0),
                                    PKUChannel = cms.string("VW_CHANNEL"),
                                    isGen = cms.bool(False),
				    				RunOnMC = cms.bool(runOnMC), 
                                    generator =  cms.InputTag("generator"),
                                    genJet =  cms.InputTag("slimmedGenJets"),
                                    lhe =  cms.InputTag("externalLHEProducer"),  #for multiple weight
                                    pileup  =   cms.InputTag("slimmedAddPileupInfo"),  
                                    leptonicVSrc = cms.InputTag("leptonicV"),
                                    rho = cms.InputTag("fixedGridRhoFastjetAll"),   
                                    ak4jetsSrc = cms.InputTag("cleanAK4Jets"),      
									#photonSrc = cms.InputTag("goodPhotons"),
                                    photonSrc = cms.InputTag("slimmedPhotons"),
                                    genSrc =  cms.InputTag("prunedGenParticles"),  
                                    jecAK4chsPayloadNames = cms.vstring( jecLevelsAK4chs ),
                                    jecAK4PayloadNames = cms.vstring( ak4jecsrc ),
                                    metSrc = cms.InputTag("slimmedMETs"),
                                    vertex = cms.InputTag("offlineSlimmedPrimaryVertices"),  
                                    t1jetSrc_user = cms.InputTag("JetUserData"),
                                    t1jetSrc = cms.InputTag("slimmedJets"),      
                                    t1muSrc = cms.InputTag("slimmedMuons"),       
                                    looseelectronSrc = cms.InputTag("vetoElectrons"),
                                    electrons = cms.InputTag("slimmedElectrons"),
                                    conversions = cms.InputTag("reducedEgamma","reducedConversions",reducedConversionsName),
                                    beamSpot = cms.InputTag("offlineBeamSpot","","RECO"),
                                    loosemuonSrc = cms.InputTag("looseMuons"),

				    				goodmuonSrc = cms.InputTag("goodMuons"),
                                    goodeleSrc = cms.InputTag("goodElectrons"),

                                    hltToken    = cms.InputTag("TriggerResults","","HLT"),
                                    elPaths1     = cms.vstring("HLT_Ele23_WPTight_Gsf_v*"),
                                    elPaths2     = cms.vstring("HLT_Ele32_WPTight_Gsf_v*"),
                                    muPaths1     = cms.vstring("HLT_IsoMu20_v*","HLT_IsoTkMu20_v*"),
									#muPaths2     = cms.vstring("HLT_IsoMu22_v*","HLT_IsoTkMu22_v*"),
                                    muPaths2     = cms.vstring("HLT_IsoMu24_v*"),
                                    muPaths3     = cms.vstring("HLT_IsoMu27_v*","HLT_IsoTkMu27_v*"),
				    				noiseFilter = cms.InputTag('TriggerResults','', hltFiltersProcessName),
				    				noiseFilterSelection_HBHENoiseFilter = cms.string('Flag_HBHENoiseFilter'),
                                    noiseFilterSelection_HBHENoiseIsoFilter = cms.string("Flag_HBHENoiseIsoFilter"),
				    				noiseFilterSelection_globalTightHaloFilter = cms.string('Flag_globalTightHalo2016Filter'),
                                    noiseFilterSelection_EcalDeadCellTriggerPrimitiveFilter = cms.string('Flag_EcalDeadCellTriggerPrimitiveFilter'),
				    				noiseFilterSelection_goodVertices = cms.string('Flag_goodVertices'),
				    				noiseFilterSelection_eeBadScFilter = cms.string('Flag_eeBadScFilter'),
                                    noiseFilterSelection_badMuon = cms.InputTag('BadPFMuonFilter'),
                                    noiseFilterSelection_badChargedHadron = cms.InputTag('BadChargedCandidateFilter'),
                                    full5x5SigmaIEtaIEtaMap   = cms.InputTag("photonIDValueMapProducer:phoFull5x5SigmaIEtaIEta"),
                                    phoChargedIsolation = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
                                    phoNeutralHadronIsolation = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
                                    phoPhotonIsolation = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
                                    effAreaChHadFile = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfChargedHadrons_90percentBased_V2.txt"),
                                    effAreaNeuHadFile= cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfNeutralHadrons_90percentBased.txt"),
                                    effAreaPhoFile   = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfPhotons_90percentBased.txt")
                                    )

process.analysis = cms.Path(
			    			process.JetUserData +
                            process.leptonSequence +
                            process.jetSequence +
                            process.metfilterSequence + #*process.treeDumper)
                            process.ecalBadCalibReducedMINIAODFilter*
                            process.treeDumper)

### Source
process.load("VAJets.PKUCommon.data.RSGravitonToWW_kMpl01_M_1000_Tune4C_13TeV_pythia8")
process.source.fileNames = [
#"root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/E6440217-0405-E811-8404-A0369F7F8E80.root "
#"/store/mc/RunIISummer16MiniAODv2/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/40000/A0C1C471-E704-E811-A1F2-008CFAF292B0.root"   #root://cms-xrd-global.cern.ch/
#"/store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v2/00000/EC2D608D-622A-E711-A658-002590D9D984.root"
#"/store/mc/RunIISummer16MiniAODv2/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/F205A9E7-0BCE-E611-8617-008CFA5D275C.root"
#"/store/mc/RunIISummer16MiniAODv3/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_102X_upgrade2018_realistic_v21-v1/70000/FADCF3F9-6247-E911-A86D-EC0D9A80980A.root"
#"/store/data/Run2018A/SingleMuon/MINIAOD/17Sep2018-v2/90000/6FEE6A9B-E03C-A14F-AD01-914C76D0A721.root"
#"/store/data/Run2018A/EGamma/MINIAOD/17Sep2018-v2/120000/5248C2A0-4A01-8E44-AFD3-C87ED5EB123B.root"
"/store/data/Run2018D/EGamma/MINIAOD/PromptReco-v2/000/325/172/00000/A3B29E9C-A761-0D41-95EB-EA34C20978C0.root"
]

process.maxEvents.input = -1  #-1
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.cerr.FwkReport.limit = 99999999

process.TFileService = cms.Service("TFileService",
                                    fileName = cms.string("treePKU.root")
                                   )
