# Automotive SDK

通用车企 ECU 模拟与诊断测试 SDK。这是一个现代化、模块化、解耦的 Python 库，用于替代原有的强耦合 `ecu_simulator` 项目。

## 特性

*   **五层解耦架构**: HAL (硬件) -> Transport (传输) -> Protocol (协议) -> Service (业务服务) -> Facade (SDK API)
*   **硬件无关**: 通过 `IHardwareAdapter` 支持多种底层硬件（SocketCAN, Tosun, Toomoss, PCAN），业务代码无需修改。
*   **配置隔离**: 通过 `ConfigManager` 和 `VehicleRegistry` 动态加载车型拓扑和数据配置，彻底消除代码中的车型（如 mars1/venus）硬编码。
*   **安全凭证管理**: 凭证（密码/Token）不再明文硬编码，由 `CredentialProvider` 通过环境变量或外部配置统一注入。
*   **插件化第三方集成**: 飞书、Jira、云端 BOS 存储等不再是核心强依赖，可通过 `@plugin` 装饰器注册。

## 安装

```bash
# 基本安装
pip install -e .

# 包含不同硬件支持的安装
pip install -e ".[tosun]"
pip install -e ".[pcan]"

# 安装全部测试及第三方插件依赖
pip install -e ".[full]"
```

## 快速使用

新的入口点是 `automotive_sdk.VehicleSDK`，它采用 Lazy 初始化，并且支持 Context Manager：

```python
from automotive_sdk import VehicleSDK
from automotive_sdk.core.types import DiagMode

# 1. 初始化 SDK (指定车型、版本，以及使用的底层硬件)
with VehicleSDK(vehicle_type="mars1", version="v_3_0_0", hardware="socketcan") as sdk:

    # 2. 诊断服务 (连接 BGM 并读取 DID)
    sdk.diagnostic.connect(ecu="BGM", mode=DiagMode.DOIP)
    resp = sdk.diagnostic.read_did(0xF190)
    print(f"BGM VIN: {resp.data}")
    sdk.diagnostic.disconnect()

    # 3. 总线服务 (发送单帧消息)
    sdk.bus.send_single(bus_name="bodycan", msg_id=0x123, data=b"\x11\x22")

    # 4. 信号服务 (通过解析加载数据修改具体信号)
    sdk.signal.set_signal_in_message(msg_name="BGM_Status", signal_name="DoorOpen", value=1)
```

## 向后兼容 (Migration)

对于已有的大量自动化测试脚本，SDK 提供了兼容层包装，将老的方法名映射到新的架构上。

只需修改导入路径：
```python
# 旧代码:
# from ecu_simulator.interface.ecuinterface import ECUInterface
# 新代码:
from automotive_sdk.compat.ecu_simulator import ECUInterface

# 后续调用保持一致
tester = ECUInterface(veh_type="mars1", bl_ver="v_3_0_0")
tester.Ecu_Sim_App.Ecu_start()
```

## 架构参考

*   **`core/`**: 存放所有核心抽象 `interfaces.py`、类型 `types.py`、异常定义 `errors.py`、事件总线 `events.py`。
*   **`hal/`**: 硬件抽象层。添加新硬件只需继承 `BaseHardwareAdapter` 并放到 `adapters/` 目录下。
*   **`transport/`**: CAN / LIN / FlexRay / Ethernet 报文级收发管理。
*   **`protocol/`**: UDS / DoIP / SOMEIP 等标准协议实现。
*   **`services/`**: 将复杂的业务（刷写、总线过滤、诊断控制）封装成高层 API。
*   **`vehicle/` & `config/`**: 车型数据注册与解析。
