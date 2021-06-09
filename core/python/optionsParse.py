import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing


"""Functions to setup & handle command-line argument parsing"""


def setup_opts():
    """Setup a standard VarParsing object to handle command-line args"""
    options = VarParsing('analysis')
    options.register ('wantSummary',
                      0,
                      VarParsing.multiplicity.singleton,
                      VarParsing.varType.int,  # have to use int for a bool (!)
                      "Print module summary (# executions, time per module)")
    options.register ('eventContent',
                      'default',
                      VarParsing.multiplicity.singleton,
                      VarParsing.varType.string,
                      "Control which variables are stored. Possible values: 'default', 'min', max'")

    # setup defaults
    options.maxEvents = 100
    options.inputFiles = cms.untracked.vstring(['file:////nfs/dust/cms/user/jabuschh/NonResonantTTbar/ALPToTTbar_private_production/ALP_ttbar_interference_SM_like/output_step6_MiniAOD/B2G-RunIISummer20UL18MiniAOD-00455_0.root'])
    options.outputFile = "ALPtoTTbar_interference_colorflowSMlike_0test.root"

    # options.outputFile = "Ntuple.root"
    # options.maxEvents = 500

    return options


def set_event_content(process, eventContent):
    """Control event content

    Parameters
    ----------
    process : cms.Process
        Main process object to manipulate
    eventContent : string
        Options controlling the event content:
        if 'min' : minimal event content
        if 'max' : maximal event content
        else     : do nothing here, keep content as in process
    """
    if eventContent == 'min':
        process.MyNtuple.doL1TriggerObjects=cms.bool(False)
    if eventContent == 'max':
        process.MyNtuple.doL1TriggerObjects=cms.bool(True)


def parse_apply_opts(process, options):
    """Handle command-line args, and apply to the cms.Process object

    Parameters
    ----------
    process : cms.Process
        Main process object to manipulate
    options : VarParsing
        Options object to parse & apply to process
    """
    options.parseArguments()

    # Update process
    if options.inputFiles:
        process.source.fileNames = cms.untracked.vstring(options.inputFiles)
    process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(options.maxEvents))
    process.options.wantSummary = cms.untracked.bool(bool(options.wantSummary))
    # use this awkward __getattr__ as by default VarParsing changes options.outputFile
    # to xxx_numEventsYYY.root, which we don't necessarily want
    process.MyNtuple.fileName = cms.string(options.__getattr__('outputFile', noTags=True))
    set_event_content(process,options.eventContent)
