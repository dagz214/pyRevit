"""Wrapper module for pyRevitLabs functionality"""
import logging
#pylint: disable=W0703,C0302,C0103,W0614,E0401,W0611,C0413
#pylint: disable=superfluous-parens
from pyrevit import HOST_APP, EXEC_PARAMS, HOME_DIR
from pyrevit.framework import clr
import pyrevit.compat as compat

# try loading pyrevitlabs
clr.AddReference('Nett')
clr.AddReference('MadMilkman.Ini')
clr.AddReference('OpenMcdf')
clr.AddReference('YamlDotNet')
clr.AddReference('pyRevitLabs.NLog')
clr.AddReference('pyRevitLabs.MahAppsMetro')
clr.AddReference('pyRevitLabs.Common')
clr.AddReference('pyRevitLabs.CommonCLI')
clr.AddReference('pyRevitLabs.CommonWPF')
clr.AddReference('pyRevitLabs.Language')
clr.AddReference('pyRevitLabs.DeffrelDB')
clr.AddReference('pyRevitLabs.TargetApps.Revit')
clr.AddReference('pyRevitLabs.PyRevit')
clr.AddReference('PythonStubsBuilder64')
import Nett
import pyRevitLabs.NLog as NLog
import MadMilkman.Ini
import OpenMcdf
import YamlDotNet as libyaml
import pyRevitLabs.MahAppsMetro
from pyRevitLabs import Common
from pyRevitLabs import CommonCLI
from pyRevitLabs import CommonWPF
from pyRevitLabs import Language
from pyRevitLabs import DeffrelDB
from pyRevitLabs import TargetApps
from pyRevitLabs import PyRevit
from PythonStubs import PythonStubsBuilder

from pyrevit import coreutils
from pyrevit.coreutils import logger


mlogger = logger.get_logger(__name__)


# setup logger
class PyRevitOutputTarget(NLog.Targets.TargetWithLayout):
    """NLog target to direct log messages to pyRevit output window."""
    def Write(self, asyncLogEvent):
        """Write event handler."""
        try:
            event = asyncLogEvent.LogEvent
            level = self.convert_level(event.Level)
            if mlogger.is_enabled_for(level):
                print(self.Layout.Render(event))    #pylint: disable=E1101
        except Exception as e:
            print(e)

    def convert_level(self, nlog_level):
        """Convert Nlog levels to pything logging levels."""
        if nlog_level == NLog.LogLevel.Fatal:
            return logging.CRITICAL
        elif nlog_level == NLog.LogLevel.Error:
            return logging.ERROR
        elif nlog_level == NLog.LogLevel.Info:
            return logging.INFO
        elif nlog_level == NLog.LogLevel.Debug:
            return logging.DEBUG
        elif nlog_level == NLog.LogLevel.Off:
            return logging.DEBUG
        elif nlog_level == NLog.LogLevel.Trace:
            return logging.DEBUG
        elif nlog_level == NLog.LogLevel.Warn:
            return logging.WARNING


# activate binding resolver
if not EXEC_PARAMS.doc_mode:
    if HOST_APP.is_older_than(2019):
        PyRevit.PyRevitBindings.ActivateResolver()

    # configure NLog
    #pylint: disable=W0201
    if compat.PY2:
        config = NLog.Config.LoggingConfiguration()
        target = PyRevitOutputTarget()
        target.Name = __name__
        target.Layout = "${level:uppercase=true} [${logger}] ${message}"
        config.AddTarget(__name__, target)
        config.AddRuleForAllLevels(target)
        NLog.LogManager.Configuration = config

        for rule in NLog.LogManager.Configuration.LoggingRules:
            rule.EnableLoggingForLevel(NLog.LogLevel.Info)
            rule.EnableLoggingForLevel(NLog.LogLevel.Debug)

        nlog_mlogger = NLog.LogManager.GetLogger(__name__)
