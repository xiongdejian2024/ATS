
/*****************************************************************************
 * (c) Copyright, JIDU Co,Ltd, Copyright 2023
 *
 * All rights reserved.
 *
 ****************************************************************************/

/**
  * @file       ConfigServerCommon.h

  * @author     hongbo.wu@jiduauto.com

  * @version    v1.0

  * @date       2023/12/01

  * @brief      description
*/

#ifndef _JIDU_SOA_JET_CONFIG_SERVER_LIB_COMMON_H_
#define _JIDU_SOA_JET_CONFIG_SERVER_LIB_COMMON_H_

#include <stdint.h>
#include <string.h>
#include <stdbool.h>
#include <vector>

namespace jet

{

namespace config

{

typedef enum{
  EN_RESULT_SUCCESS = 0, //接口调用成功
  EN_RESULT_FAIL = 1,  //接口调用失败
  EN_RESULT_NOT_INITED = 2, //库还未初始化
  EN_RESULT_CONFIG_NOT_EXIST = 3,//配置文件不存在
  EN_RESULT_CHECK_CONFIG_FAIL = 4, //配置文件校验失败
  EN_RESULT_FILE_SIZE_OVER_MAX = 5 //配置文件太大
}EnResult;

typedef enum{

 EN_CONFIG_UPDATED = 0,  //更新配置文件

 EN_CONFIG_DELETED = 1  //删除配置文件

} EnConfigUpdateCmd;



typedef enum{

 EN_USE_STATUS_CHECK_SUCCESS = 0,  //配置文件校验成功

 EN_USE_STATUS_CHECK_FAIL = 1,  //配置文件校验失败

 EN_USE_STATUS_APPLY = 2   //配置文件应用生效

} EnAppUseConfigStatus;



typedef enum{

 POWER_SLEEP = 0,  //休眠

 POWER_WAKEUP = 1  //唤醒

} PowerModeStatus;

typedef struct{

  std::string configFileName; //配置文件名称

  int64_t publishId;  //配置版本

  std::string filepath; //配置文件存储路径，包括文件名

} configAppInfo;


/*

*@fn ConfigUpdateNotify1

*@brief 配置变更通知回调，通知配置文件信息及本地存储路径，应用注册给共用库

*@param[in] appname(配置所属应用名称)

*@param[in] configname(配置文件名称)

*@param[in] publishid(配置版本)

*@param[in] cmd(变更操作)当前只有更新和删除两种指令

*@param[in] filepath(配置文件存储路径，包括文件名)

*@param[in] fileSize(配置文件大小,单位字节)

*@return N/A

*/

typedef std::function<void(const std::string &appname, const std::string &configname,const int64_t &publishid,const int64_t &fileSize, const EnConfigUpdateCmd &cmd, const std::string &filepath)> ConfigUpdateNotify1;


/*

*@fn ConfigUpdateNotify2

*@brief 配置变更通知回调，通知配置文件信息及内容数据，应用注册给共用库, 

*@param[in] appname(配置所属应用名称)

*@param[in] configname(配置文件名称)

*@param[in] publishid(配置版本)

*@param[in] cmd(变更操作) 当前只有更新和删除两种指令

*@param[in] data(配置文件数据) 删除指令，该数据为空；如果数据大小超过10M,该数据也为空，业务收到通知后需要自己读取文件进行解析

*@return N/A

*/

typedef std::function<void(const std::string &appname, const std::string &configname,const int64_t &publishid, const EnConfigUpdateCmd &cmd, const std::vector<uint8_t> &data)> ConfigUpdateNotify2;



/*

*@fn InitConfigServerCommon

*@brief 初始化配置共用库

*@param[in] domain(域名称，CDC ACU BGM TCAM )

*@param[in] storepath(存储路径,需要各域建好文件夹，给出路径，configServer直接写配置文件到该路径，不允许有其他业务的文件写入该路径。)

*@param[in] allFilesSizeMax(单位byte，如果设置为0，没有限制。落盘进行滚删，先删除旧文件, ACU预计10MB限制)

*@param[in] callback1(配置变更1通知回调)

*@param[in] callback2(配置变更2通知回调)

*@param[in] convert(是否需要准备OTA升级后的配置数据转换，只有CDC需要设置true，初始化之后，不管是否转换，都需要调用ConvertCompleted接口)

*@return 0 表示成功，非0表示失败，失败的errorCode之后定义  (当前只有EN_RESULT_SUCCESS)

*/

EnResult InitConfigServerCommon(const std::string& domain,const std::string& storepath,const uint64_t allFilesSizeMax, ConfigUpdateNotify1 callback1, ConfigUpdateNotify2 callback2, bool convert = false);


/*

*@fn DeinitConfigServerCommon

*@brief 反初始化配置共用库

*@return N/A （EN_RESULT_NOT_INITED  | EN_RESULT_SUCCESS）

*/

EnResult DeinitConfigServerCommon();



/*

*@fn GetConfigFileData

*@brief 配置文件读取解析并返回数据

*@param[in] appName(应用名称)

*@param[in] configname(配置文件名称)

*@param[out] publishid(配置版本)

*@param[out] configdata(配置文件数据) 如果数据大小超过10M,该数据为空，业务需要自己读取文件进行解析

*@return 0 表示成功，非0表示失败，(EN_RESULT_NOT_INITED | EN_RESULT_CONFIG_NOT_EXIST | EN_RESULT_CHECK_CONFIG_FAIL | EN_RESULT_FILE_SIZE_OVER_MAX | EN_RESULT_SUCCESS)

*/

EnResult GetConfigFileData(const std::string appName, const std::string configname, int64_t &publishId, std::vector<uint8_t> &configdata);



/*

*@fn GetConfigInfo

*@brief 回复云配置中心应用使用配置的状态 

*@param[in] appname(应用名称)

*@param[in] configname(配置文件名称)

*@param[out] publishid(配置版本)

*@param[out] filepath(配置文件存储路径，包括文件名)

*@return 最新配置文件的状态 （EN_RESULT_NOT_INITED | EN_RESULT_CONFIG_NOT_EXIST | EN_RESULT_SUCCESS）

*/

EnResult GetConfigInfo(const std::string &appname, const std::string & configname, int64_t & publishid, std::string & filepath);

/*

*@fn GetAppConfigInfo

*@brief 回复云配置中心应用使用配置的状态 

*@param[in] appname(应用名称)

*@param[out] info(配置文件名，配置文件路径，配置文件版本号)

*@return 最新配置文件的状态

*/

EnResult GetConfigAppInfo(const std::string &appname, std::vector<configAppInfo> & info);


/*

*@fn SetUseConfigStatus

*@brief 回复云配置中心应用使用配置的状态 

*@param[in] appname(应用名称)

*@param[in] appinstindex(应用实例编号)

*@param[in] configname(配置文件名称)

*@param[in] publishid(配置版本)

*@param[in] status(使用状态)

*@param[in] message(状态回复附加消息，应用自定义)

*@return N/A

*/

EnResult SetUseConfigStatus(const std::string & appname,const uint32_t &appinstindex, const std::string &configname,const int64_t &publishid,const EnAppUseConfigStatus &status, const std::string & message);



/*

*@fn IsConverted

*@brief 判断是否已经将旧版配置转存为新格式 

*@return 已转存返回true，否则false

*/

bool IsConverted();



/*

*@fn ConvertConfig

*@brief 将旧的配置文件转成新的 

*@param[in] appname(应用名称)

*@param[in] configname(配置文件名称)

*@param[out] publishid(配置版本)

*@param[out] configdata(配置文件数据)

*@return 

*/

EnResult ConvertConfig(const std::string &appname,const std::string & configname, const int64_t & publishid, const std::vector<uint8_t> &configdata);



/*

*@fn ConvertCompleted

*@brief 配置文件转换完成

*@return 
*/

void ConvertCompleted();

/*

*@fn PowerModeChange

*@brief 休眠/唤醒需要通知ConfigServerLib, 重启分发策略依赖唤醒消息，信息持久化依赖休眠消息

*@param[in] status(电源状态)

*@return 
*/

void PowerModeChange(PowerModeStatus status);

}

} //namespace jet

#endif

