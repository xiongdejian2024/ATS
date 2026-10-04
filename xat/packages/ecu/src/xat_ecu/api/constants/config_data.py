#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 配置中心数据格式
gb_config_data = [
                    {
                        "proname":"tcam.rvs.gb32960.product.url",
                        "value":"jidu-gb32960.geely.com:18443"},
                    # {
                    #     "proname":"tcam.rvs.gb32960.staging.url",
                    #     "value":"evc-gb32960.test.geely.com:18443"},
                    {
                        "proname":"tcam.rvs.gb32960.staging.url",
                        "value":"120.48.11.173:18443"},
                    {
                        "proname":"tcam.rvs.gb32960.test.url",
                        "value":""},
                    {
                        "proname":"tcam.rvs.gb32960.url.test.select",
                        "value":""},
                    {
                        "proname":"tcam.rvs.gb32960.zl.address",
                        "value":"120.48.11.173:29476"},
                    {
                        "proname":"tcam.rvs.gb32960.zl.onoff",
                        "value":0},
                    {
                        "proname":"tcam.rvs.gb32960.config",
                        "value":[
                                    {
                                        "key":"rms.activate",
                                        "value":1,
                                        "comment":""},
                                    {
                                        "key":"realtime.period",
                                        "value":10,
                                        "comment":""},
                                    {
                                        "key":"supplement.period",
                                        "value":4,
                                        "comment":""},
                                    {
                                        "key":"rms.login.delay.time",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"rms.logout.delay.time",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"heartbeat",
                                        "value":15,
                                        "comment":""},
                                    {
                                        "key":"warning.period",
                                        "value":0,
                                        "comment":""}
                                ]
                    },
                    {
                        "proname":"tcam.rvs.gb32960.warning",
                        "value":[
                                    {
                                        "key":"warning.level.1",
                                        "value":0,
                                        "comment":""},
                                    {	
                                        "key":"warning.level.2",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.3",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.4",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.5",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.6",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.7",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.8",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.9",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.10",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.11",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.12",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.13",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.14",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.15",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.16",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.17",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.18",
                                        "value":0,
                                        "comment":""},
                                    {
                                        "key":"warning.level.19",
                                        "value":0,
                                        "comment":""}
                                ]
                    }
                ]

power_config_data = [
                        {
                            "proname": "tcam.power.ECUPowerParaCfg.soc",
                            "value":[
                                        {
                                            "key": "Lcfg_TimerMQTTHbInterval",
                                            "value": 20,
                                            "comment": ""},
                                        {
                                            "key": "Lcfg_ResetTboxTimeCount",
                                            "value": 32,
                                            "comment": "hours"},
                                        {
                                            "key": "Lcfg_ResetScoupStartTime",
                                            "value": 3,
                                            "comment": "hours"},
                                        {
                                            "key": "Lcfg_ResetScoupEndTime",
                                            "value": 5,
                                            "comment": "hours"}
                                    ]
                        },
                        {
                            "proname": "tcam.power.ECUPowerParaCfg.mcu",
                            "value":[
                                        {
                                            "key": "Lcfg_MaxTimePollCycle1",
                                            "value": 168,
                                            "comment": "hours"},
                                        {
                                            "key": "Lcfg_MaxTimePollCycle2",
                                            "value": 168,
                                            "comment": "hours"},
                                        {
                                            "key": "Lcfg_MaxTimeInStandby",
                                            "value": 1200,
                                            "comment": "hours"},
                                        {
                                            "key": __import__("os").environ['XAT_CREDENTIAL_SCAN_B43235FADBA1960E7647'],
                                            "value": 120,
                                            "comment": "minutes"},
                                        {
                                            "key": __import__("os").environ['XAT_CREDENTIAL_SCAN_06B32837E7A590BF7424'],
                                            "value": 240,
                                            "comment": "minutes"},
                                        {
                                            "key": "Lcfg_SleepPollingPollingTime",
                                            "value": 60,
                                            "comment": "second"},
                                        {
                                            "key": "Lcfg_TimerDoorOpenUsageMode",
                                            "value": 1000,
                                            "comment": "ms"},
                                        {
                                            "key": "Lcfg_TimerLowUsageModes",
                                            "value": 30,
                                            "comment": "second"},
                                        {
                                            "key": "Lcfg_TimerTimingWakeup",
                                            "value": 0,
                                            "comment": "minutes"},
                                        {
                                        "key": "Lcfg_CounterTimingWakeup",
                                        "value": 0,
                                        "comment": "times"}
                                    ]
                        },
                        {
                            "proname": "tcam.power.SleepLock",
                            "value":[
                                        {
                                            "key": "Lcfg_KeepAlive",
                                            "value": 100,
                                            "comment": "second"},
                                        {
                                            "key": "Lcfg_CountScope",
                                            "value": 30,
                                            "comment": "minutes"}
                                    ]
                        }
                    ]

log_config_data = [
                    {
                        "proname": "remoteLog.t2v.logcfg",
                        "value":{
                                    "ecuName": "TCAM",
                                    "ecuLogConfig": [
                                                        {
                                                            "vlog_type_id": 1,
                                                            "vlog_level": "Info",
                                                            "vlog_logfile_size": 20,
                                                            "vlog_upload_interval": 800,
                                                            "expired_time": 1716371734},
                                                        {
                                                            "vlog_type_id": 4,
                                                            "vlog_level": "Debug",
                                                            "vlog_logfile_size": 0,
                                                            "vlog_upload_interval": 100,
                                                            "expired_time": 1716371734},
                                                        {
                                                            "vlog_type_id": 100,
                                                            "vlog_level": "Debug",
                                                            "vlog_logfile_size": 0,
                                                            "vlog_upload_interval": 100,
                                                            "expired_time": 1716371734},
                                                        {
                                                            "vlog_type_id": 101,
                                                            "vlog_level": "Debug",
                                                            "vlog_logfile_size": 0,
                                                            "vlog_upload_interval": 100,
                                                            "expired_time": 1716371734},
                                                        {
                                                            "vlog_type_id": 102,
                                                            "vlog_level": "Debug",
                                                            "vlog_logfile_size": 0,
                                                            "vlog_upload_interval": 100,
                                                            "expired_time": 1716281734}
                                                    ],
                                    "localTriggerUploadConfig":[
                                                                    {
                                                                        "triggerType": 1,
                                                                        "isUploadLog": True,
                                                                        "logTimeScope": 0,
                                                                        "logType": []
                                                                    },
                                                                    {
                                                                        "triggerType": 2,
                                                                        "isUploadLog": True,
                                                                        "logTimeScope": 0,
                                                                        "logType": []
                                                                    },
                                                                    {
                                                                        "triggerType": 3,
                                                                        "isUploadLog": True,
                                                                        "logTimeScope": 0,
                                                                        "logType": []
                                                                    },
                                                                    {
                                                                        "triggerType": 4,
                                                                        "isUploadLog": True,
                                                                        "logTimeScope": 0,
                                                                        "logType": []
                                                                    }
                                                                ]
                                }
                    }
                ]

xcall_config_data = [
                        {
                            "proname":"tcam.ecall.callfunctiontype",
                            "value":1},
                        {
                            "proname":"tcam.ecall.calltype",
                            "value":1},
                        {
                            "proname":"tcam.ecall.callnumber",
                            "value":"02161897441"},
                        {
                            "proname":"tcam.bcall.callfunctiontype",
                            "value":2},
                        {
                            "proname":"tcam.bcall.calltype",
                            "value":1},
                        {
                            "proname":"tcam.bcall.callnumber",
                            "value":"02161897441"}
                    ]

v2trouter_config_data = [
                            {
                                "proname": "tcam.v2t.MQTT.dataCollect.interval",
                                "value": 300
                            },
                            {
                                "proname": "tcam.v2t.MQTT.connectOpts.minRetryInterval",
                                "value": 1
                            },
                            {
                                "proname": "tcam.v2t.MQTT.connectOpts.maxRetryInterval",
                                "value": 3
                            },
                            {
                                "proname": "tcam.v2t.MQTT.Newly.Opt",
                                "value": [
                                {
                                    "key": "MQTT_ACK_Timeout_interval",
                                    "value": 5,
                                    "comment": "s"
                                },
                                {
                                    "key": "MQTT_Connect_Timeout_interval",
                                    "value": 10,
                                    "comment": "s"
                                },
                                {
                                    "key": "MQTT_Downlink_Max_interval",
                                    "value": 50,
                                    "comment": "Hz"
                                },
                                {
                                    "key": "MQTT_Downlink_Timeout_interval",
                                    "value": 5,
                                    "comment": "s"
                                }
                                ]
                            }
                            ]
                    

rvc_config_data = [
                    {
                        "proname":"tcam.rvc.CockpitCtrlParaConfig",
                        "value":[
                            {
                                "key":"uClimateTempMaintainActvSOC",
                                "value":20,
                                "comment":"0 ~ 100%"
                                },
                            {
                                "key":"uClimateTempMaintainExitSOC",
                                "value":15,
                                "comment":"0 ~ 100%"
                                },
                            {
                                "key":"uClimaTempMaintainRunTime",
                                "value":30,
                                "comment":"0 ~ 59 min"
                                },
                            {
                                "key":"uRvcTspRspnTimeout",
                                "value":10,
                                "comment":"0 ~ 60 second"
                                },
                            {
                                "key":"uRemClimaHvTimeout",
                                "value":15,
                                "comment":"0 ~ 127 second"
                                },
                            {
                                "key":"uRemClimaCtrlTimeout",
                                "value":15,
                                "comment":"0 ~ 127 second"
                                },
                            {
                                "key":"uRemClimaRunTime",
                                "value":30,
                                "comment":"0 ~ 59 min"
                                },
                            {
                                "key":"uRemSeatHeatTimeout",
                                "value":15,
                                "comment":"0 ~ 127 second"
                                },
                            {
                                "key":"uRemSeatHeatRunTime",
                                "value":30,
                                "comment":"0 ~ 59 min"
                                },
                            {
                                "key":"uRemSteerWhlHeatTimeout",
                                "value":15,
                                "comment":"0 ~ 127 second"
                                },
                            {
                                "key":"uRemSteerWhlHeatRunTime",
                                "value":30,
                                "comment":"0 ~ 59 min"
                                },
                            {
                                "key":"uRemFrontDefrostRunTime",
                                "value":30,
                                "comment":"0 ~ 59 min"
                                },
                            {
                                "key":"uRemElecDefrostRunTime",
                                "value":15,
                                "comment":"0 ~ 30 min"},
                            {
                                "key":"uRemElecDefrostHvRunTime",
                                "value":16,
                                "comment":"0 ~ 30 min"
                                },
                            {
                                "key":"uRemFrontDefrostTimeout",
                                "value":15,
                                "comment":"0 ~ 60 second"
                                },
                            {
                                "key":"uRemSeatVentTimeout",
                                "value":15,
                                "comment":"0 ~ 60 second"
                                },
                            {
                                "key":"uRemSeatVentRunTime",
                                "value":30,
                                "comment":"0 ~ 59 min"
                                },
                            {
                                "key": "uRemMaxCoolingRunTime",
                                "value": 30,
                                "comment": "0 ~ 59 min"
                                },
                            {
                                "key": "uRemMaxHeatingRunTime",
                                "value": 30,
                                "comment": "0 ~ 59 min"
                                },
                                {
                                "key": "uRemHvBattPulseHeatgActive",
                                "value": 1,
                                "comment": "0/1"
                            }
                            ]
                     },
                    {
                        "proname":"tcam.rvc.CockpitBookParaConfig",
                        "value":
                            [
                            {
                                "key":"uRemBattHeatStartRunTime",
                                "value":60,
                                "comment":"0 ~ 120 min"
                                },
                            {
                                "key":"uRemCockpitReserveRunTime",
                                "value":30,
                                "comment":"0 ~ 60 min"
                                },
                            {
                                "key":"uRemCockpitReserveStartTime",
                                "value":15,
                                "comment":"0 ~ 60 min"
                                },
                            {
                                "key":"uRvcSubscribeCmdExecTimeOut",
                                "value":30,
                                "comment":"0 ~ 60 second"
                                },
                            {
                                "key":"uRvcRenewalCmdReqTime",
                                "value":825,
                                "comment":"0 ~ 900 second"
                                },
                            {
                                "key":"uRemClimaHvDelayTimeout",
                                "value":15,
                                "comment":"0 ~ 60 second"
                                },
                            {
                                "key":"uRvcRenewalCmdRspnTimeOut",
                                "value":30,
                                "comment":"0 ~ 60 second"
                                },
                            {
                                "key":"uRvcWaitTimeSyncFlag",
                                "value":15,
                                "comment":"0 ~ 60 second"
                                },
                            {
                                "key":"uRemOutRearViewFoldTimeout",
                                "value":10,
                                "comment":"0 ~ 127 second"
                                }
                            ]
                         }
                  ]

min_config_data = [
                    {
                        "proname":"soa.config",
                        "value":[
                                    {
                                        "version":"1715657295876",
                                        "globalConfig":
                                                        {
                                                            "enable":"1",
                                                            "uploadCycle":10000},
                                        "dataConfig":[
                                                        {
                                                            "service":"GNSSService",
                                                            "api":"NotifyGNSSInformation",
                                                            "dealayTime":700,
                                                            "applyRole":1},
                                                        {
                                                            "service":"NetStatService",
                                                            "api":"NetWorkSts",
                                                            "dealayTime":0,
                                                            "applyRole":1}
                                                    ]
                                    }
                                 ]
                    }
                   ]

nrm_config_data = [
                    {
                        "proname":"tcam.nrm.FunctionSwitch", # 功能开关
                        "value":1},
                    {
                        "proname": "tcam.nrm.NetResourceDetailFileConfig",
                        "value": [
                            {
                                "key": "FileCreatInterval", #上传单个日志文件的最大间隔
                                "value": 3600,
                                "comment": "file creat interval time(s)"
                            },
                            {
                                "key": "FileCount", # 日志文件的最大数量(超出将被覆盖)
                                "value": 60,
                                "comment": "file count"
                            },
                            {
                                "key": "FileCompression", # 是否压缩日志
                                "value": 1,
                                "comment": "Compression"
                            }
                            ]
                    }
                ]

nrm_config_data_v2_2 = [
                    {
                        "proname":"FunctionSwitch", # 功能开关
                        "value":1},
                    {
                        "proname": "NetResourceDetailFileConfig",
                        "value": [
                            {
                                "key": "FileCreatInterval", #上传单个日志文件的最大间隔
                                "value": 3600,
                                "comment": "file creat interval time(s)"
                            },
                            {
                                "key": "FileCount", # 日志文件的最大数量(超出将被覆盖)
                                "value": 60,
                                "comment": "file count"
                            },
                            {
                                "key": "FileCompression", # 是否压缩日志
                                "value": 1,
                                "comment": "Compression"
                            }
                            ]
                    }
                ]

cellnetmgr_config_data = [
                            {
                                "proname": "tcam.cellnetmgr.CFUNFailTimesThreshold",
                                "value": 5
                            },
                            {
                                "proname": "tcam.cellnetmgr.IntervalRecoveryTime",
                                "value": 600
                            },
                            {
                                "proname": "tcam.cellnetmgr.SIMStatusFailTimeThreshold",
                                "value": 60
                            },
                            {
                                "proname": "tcam.cellnetmgr.RSSIThreshold",
                                "value": -120
                            },
                            {
                                "proname": "tcam.cellnetmgr.RSSICheckTimeThreshold",
                                "value": 180
                            },
                            {
                                "proname": "tcam.cellnetmgr.REGCheckTimeThreshold",
                                "value": 180
                            },
                            {
                                "proname": "tcam.cellnetmgr.CfunTimeThreshold",
                                "value": 180
                            },
                            {
                                "proname": "tcam.cellnetmgr.SetApnTimeThreshold",
                                "value": 120
                            },
                            {
                                "proname": "tcam.cellnetmgr.DialUpFailTimesThreshold",
                                "value": 2
                            },
                            {
                                "proname": "tcam.cellnetmgr.DialUpCheckTimeThreshold",
                                "value": 30
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingEnableFlag",
                                "value": 1
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingURLStaging",
                                "value": "vehicle.jiduapp.cn"
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingURLProd",
                                "value": "vehicle.jiducar.com"
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingURL",
                                "value": "vehicle.jiduapp.cn"
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingIntervalStatisticsTime",
                                "value": 300
                            },
                            {
                                "proname": "tcam.cellnetmgr.ALLStatusCollectInterval",
                                "value": 15
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingCollectInterval",
                                "value": 5
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingFailTriggerEnableFlag",
                                "value": 1
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingFailTimesThreshold",
                                "value": 3
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingHighTimeTriggerEnableFlag",
                                "value": 0
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingHighTimeValueThreshold",
                                "value": 500
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingHIghTimeTimesThreshold",
                                "value": 60
                            },
                            {
                                "proname": "tcam.cellnetmgr.NetInfoLogUploadInterval",
                                "value": 300
                            },
                            {
                                "proname": "tcam.cellnetmgr.sync_netstatusStroeInterval",
                                "value": 15
                            },
                            {
                                "proname": "tcam.cellnetmgr.NetinfoLogCacheMax",
                                "value": 100
                            },
                            {
                                "proname": "tcam.cellnetmgr.RelControlRecoveryN1Threshold",
                                "value": 90
                            },
                            {
                                "proname": "tcam.cellnetmgr.RelControlRecoveryN2Timer",
                                "value": 1800
                            },
                            {
                                "proname": "tcam.cellnetmgr.DownRateTriggerRecoveryThreshold",
                                "value": 40
                            },
                            {
                                "proname": "tcam.cellnetmgr.UploadRateTriggerRecoveryThreshold",
                                "value": 0
                            },
                            {
                                "proname": "tcam.cellnetmgr.TotalDownRateTriggerRecoveryThreshold",
                                "value": 0
                            },
                            {
                                "proname": "tcam.cellnetmgr.TotalUploadRateTriggerRecoveryThreshold",
                                "value": 0
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingFailMaxTimesThreshold",
                                "value": 60
                            },
                            {
                                "proname": "tcam.cellnetmgr.IPAFailureRateThreshold",
                                "value": 102400
                            },
                            {
                                "proname": "tcam.cellnetmgr.PingDogRebootThreshold",
                                "value": 600
                            },
                            {
                                "proname": "tcam.cellnetmgr.DataRegDenyRecovery",
                                "value": [
                                {
                                    "key": "9",
                                    "value": 1,
                                    "comment": "UE ID can't be derived by network. 1 need wait in deregistered"
                                },
                                {
                                    "key": "10",
                                    "value": 1,
                                    "comment": "Implicitly de-registered. 1 need wait in deregistered"
                                },
                                {
                                    "key": "15",
                                    "value": 1,
                                    "comment": "No suitable cells in tracking area. 1 need wait in deregistered"
                                }
                                ]
                            },
                            {
                                "proname": "tcam.cellnetmgr.DataCallErrRecovery",
                                "value": [
                                {
                                    "key": "2_208",
                                    "value": 1,
                                    "comment": "IPV4_CALL_DISALLOWED. Need cfun"
                                },
                                {
                                    "key": "2_209",
                                    "value": 1,
                                    "comment": "IPV4_CALL_THROTTLED. Need cfun"
                                },
                                {
                                    "key": "2_210",
                                    "value": 1,
                                    "comment": "IPV6_CALL_DISALLOWED. Need cfun"
                                },
                                {
                                    "key": "2_211",
                                    "value": 1,
                                    "comment": "IPV6_CALL_THROTTLED. Need cfun"
                                },
                                {
                                    "key": "3_1140",
                                    "value": 1,
                                    "comment": "PDU_MAX_TIMEOUT. Need cfun"
                                }
                                ]
                            },
                            {
                                "proname": "tcam.cellnetmgr.ModemCrashTriggerRebootFlag",
                                "value": 1
                            },
                            {
                                "proname": "tcam.cellnetmgr.ModemCrashTriggerRebootThreshold",
                                "value": 8
                            },
                            {
                                "proname": "tcam.cellnetmgr.RsrpWeakThreshold",
                                "value": -95
                            },
                            {
                                "proname": "tcam.cellnetmgr.SnrWeakThreshold",
                                "value": 100
                            },
                            {
                                "proname": "tcam.cellnetmgr.N28BandEnableFlag",
                                "value": 1
                            },
                            {
                                "proname": "tcam.cellnetmgr.CellLogEnableFlag",
                                "value": 1
                            }
                    ]

