from saci_db.cpvs import *

CPVS = [
    MavlinkSiKCPV(),
    GPSSpoofingMoveCPV(),
    WiFiDeauthDosCPV(),
    WiFiICMPFloodingCPV(),
    ObjectTrackCPV(),
    SerialRollOverCPV(),
    CompassPermanentSpoofingCPV(),
    WifiWebCrashCPV(),
    GPSSpoofingStaticCPV(),
    SerialThrottleCPV(),
    WifiWebMoveCPV(),
    GPSSpoofingLoopCPV(),
    SerialArduinoControlCPV(),
    WifiWebStopCPV(),
    SerialRedirectCPV(),
    CompassTemporarySpoofingCPV(),
    SMBusBatteryShutdownCPV(),
    DebugESCFlashCPV(),
    SerialESCBootloaderCPV(),
    SerialESCResetCPV(),
    SerialESCDischargeCPV(),
    SerialESCOverflowCPV(),
    SerialESCExeccmdCPV(),
    SerialOverheatingCPV(),
    AcousticSpoofingAccelerometerCPV(),
    AcousticSpoofingGyroscopeCPV(),
    AcousticSpoofingMagnetometerCPV(),
    BarometricSensorSpoofingCPV(),
    ProjectorOpticalFlowCPV(),
    DepthCameraDoSCPV(),
    EMIMotorBlockCPV(),
    WiFiDeauthQuadDosCPV(),
    MavlinkDisarmCPV(),
    EMIMotorFullControlCPV(),
    EMIMotorBlockRotateCPV(),
    ARDiscoveryDoSCPV(),
    ARDiscoveryBufferOverflowCPV(),
    ARDiscoveryMitM(),
    FTPTelnetHijackCPV(),
    BeaconFrameFloodingCPV(),
    RFJammingCPV(),
    EMISpoofingMagnetometerCPV(),
    GyroscopeEMIChannelDisruptionCPV(),
    AccelerometerEMIChannelDisruptionCPV(),
    MagnetometerEMIChannelDisruptionCPV(),
    DirectionalManipulationCPV(),
    FailSafeAvoidanceCPV(),
    PathManipulationCPV(),
    PatchEmergencyStopFailureCPV(),
    PatchPivotTurnMalfunctionCPV(),
    PatchUnstableAttitudeControlCPV(),
    PatchMissionFailureCPV(),
    PatchObstacleAvoidanceErrorCPV(),
    GNSSFlightModeSpoofingCPV(),
    GNSSLoiterModeSpoofingCPV(),
    DSMxJammingHijackCPV(),
    PayloadCrashCommandCPV(),
    PayloadDisableSafetyCPV(),
    PayloadSpoofDroneIDCPV()
]
