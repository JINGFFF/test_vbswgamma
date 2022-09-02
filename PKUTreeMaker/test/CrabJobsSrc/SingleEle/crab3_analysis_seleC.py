from WMCore.Configuration import Configuration
config = Configuration()
config.section_("General")
config.General.requestName   = 'full_run2_2018_version2_seleC_v1'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.maxMemoryMB = 5000
config.JobType.pluginName  = 'Analysis'
config.JobType.inputFiles =['Autumn18_RunC_V19_DATA_L1FastJet_AK4PFchs.txt','Autumn18_RunC_V19_DATA_L1FastJet_AK4PFPuppi.txt','Autumn18_RunC_V19_DATA_L2L3Residual_AK4PFchs.txt','Autumn18_RunC_V19_DATA_L2L3Residual_AK4PFPuppi.txt','Autumn18_RunC_V19_DATA_L2Relative_AK4PFchs.txt','Autumn18_RunC_V19_DATA_L2Relative_AK4PFPuppi.txt','Autumn18_RunC_V19_DATA_L3Absolute_AK4PFchs.txt','Autumn18_RunC_V19_DATA_L3Absolute_AK4PFPuppi.txt']

config.JobType.psetName    = 'analysis_data_C.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
#config.Data.outputPrimaryDataset = 'VBS_WGAMMA_94X'
config.Data.inputDataset = '/EGamma/Run2018C-17Sep2018-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
config.Data.lumiMask = 'Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
config.Data.publication = False
config.Data.outputDatasetTag = 'full_run2_2018_version2_seleC_v1'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
