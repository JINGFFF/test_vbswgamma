from WMCore.Configuration import Configuration
config = Configuration()
config.section_("General")
config.General.requestName   = 'jec_source_v2_full_run2_2018_PUJetID_TT_version1'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.maxMemoryMB = 4000
config.JobType.pluginName  = 'Analysis'
config.JobType.inputFiles = ['RegroupedV2_Autumn18_V19_MC_UncertaintySources_AK4PFchs.txt','Autumn18_V19_MC_L1FastJet_AK4PFchs.txt','Autumn18_V19_MC_L1FastJet_AK4PFPuppi.txt','Autumn18_V19_MC_L2L3Residual_AK4PFchs.txt','Autumn18_V19_MC_L2L3Residual_AK4PFPuppi.txt','Autumn18_V19_MC_L2Relative_AK4PFchs.txt','Autumn18_V19_MC_L2Relative_AK4PFPuppi.txt','Autumn18_V19_MC_L3Absolute_AK4PFchs.txt','Autumn18_V19_MC_L3Absolute_AK4PFPuppi.txt']
config.JobType.psetName    = 'analysis_mc.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
##config.Data.outputPrimaryDataset = 'VBS_WGAMMA_94X'
config.Data.inputDataset = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext3-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = -1
config.Data.publication = False
config.Data.outputDatasetTag = 'jec_source_v2_full_run2_2018_PUJetID_TT_version1'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
