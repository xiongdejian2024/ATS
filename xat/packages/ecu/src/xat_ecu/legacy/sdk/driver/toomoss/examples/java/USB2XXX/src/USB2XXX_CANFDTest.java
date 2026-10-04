import com.toomoss.USB2XXX.USB_Device;
import com.toomoss.USB2XXX.USB2CANFD;
public class USB2XXX_CANFDTest {
	  /** 
     * Launch the application. 
     */  
    public static void main(String[] args) {   
        int ret;
        int DevHandle = 0;
        int[] DevHandleArry = new int[20];
        byte SendCANIndex = 0;		//CAN1
        byte ReceiveCANIndex = 1;	//CAN2
        boolean state;
        //扫描设备
        ret = USB_Device.INSTANCE.USB_ScanDevice(DevHandleArry);
        if(ret > 0){
        	System.out.println("Device Num = "+ret);
        	DevHandle = DevHandleArry[0];
        }else{
        	System.out.println("No device");
        	return;
        }
        //打开设备
        state = USB_Device.INSTANCE.USB_OpenDevice(DevHandle);
        if(!state){
        	System.out.println("open device error");
        	return;
        }
        //获取设备信息
        USB_Device.DEVICE_INFO DevInfo = new USB_Device.DEVICE_INFO();
        byte[] funcStr = new byte[128];
        state = USB_Device.INSTANCE.DEV_GetDeviceInfo(DevHandle,DevInfo,funcStr);
        if(!state){
        	System.out.println("get device infomation error");
        	return;
        }else{
            try {
            	System.out.println("Firmware Info:");
            	System.out.println("--Name:" + new String(DevInfo.FirmwareName, "UTF-8"));
            	System.out.println("--Build Date:" + new String(DevInfo.BuildDate, "UTF-8"));
            	System.out.println(String.format("--Firmware Version:v%d.%d.%d", (DevInfo.FirmwareVersion >> 24) & 0xFF, (DevInfo.FirmwareVersion >> 16) & 0xFF, DevInfo.FirmwareVersion & 0xFFFF));
            	System.out.println(String.format("--Hardware Version:v%d.%d.%d", (DevInfo.HardwareVersion >> 24) & 0xFF, (DevInfo.HardwareVersion >> 16) & 0xFF, DevInfo.HardwareVersion & 0xFFFF));
            	System.out.println("--Functions:" + new String(funcStr, "UTF-8"));
            } catch (Exception ep) {
                ep.printStackTrace();
            }
        }
        //初始化配置CAN
        USB2CANFD.CANFD_INIT_CONFIG CANFDConfig = new USB2CANFD.CANFD_INIT_CONFIG();
        CANFDConfig.Mode = 0;        //0-正常模式，1-自发自收模式
        CANFDConfig.RetrySend = 1;   //使能自动重传
        CANFDConfig.ISOCRCEnable = 1;//使能ISOCRC
        CANFDConfig.ResEnable = 1;   //使能内部终端电阻（若总线上没有终端电阻，则必须使能终端电阻才能正常传输数据）
        //波特率参数可以用TCANLINPro软件里面的波特率计算工具计算
        //仲裁段波特率参数,波特率=40M/NBT_BRP*(1+NBT_SEG1+NBT_SEG2)
        CANFDConfig.NBT_BRP = 1;
        CANFDConfig.NBT_SEG1 = 63;
        CANFDConfig.NBT_SEG2 = 16;
        CANFDConfig.NBT_SJW = 16;
        //数据域波特率参数,波特率=40M/DBT_BRP*(1+DBT_SEG1+DBT_SEG2)
        CANFDConfig.DBT_BRP = 1;
        CANFDConfig.DBT_SEG1 = 15;
        CANFDConfig.DBT_SEG2 = 4;
        CANFDConfig.DBT_SJW = 4;
        ret = USB2CANFD.INSTANCE.CANFD_Init(DevHandle,SendCANIndex,CANFDConfig);//初始化发送通道
        if(ret != USB2CANFD.CANFD_SUCCESS){
        	System.out.println("CANFD Init Error!");
            return;
        }else{
        	System.out.println("CANFD Init Success!");
        }
        ret = USB2CANFD.INSTANCE.CANFD_Init(DevHandle,ReceiveCANIndex,CANFDConfig);//初始化接收通道
        if(ret != USB2CANFD.CANFD_SUCCESS){
        	System.out.println("CANFD Init Error!");
            return;
        }else{
        	System.out.println("CANFD Init Success!");
        }
      //启动CAN数据接收
        ret = USB2CANFD.INSTANCE.CANFD_StartGetMsg(DevHandle, ReceiveCANIndex);
        if (ret != USB2CANFD.CANFD_SUCCESS){
        	System.out.println("Start receive CANFD failed!");
            return;
        }else{
        	System.out.println("Start receive CANFD Success!");
        }
        //发送CAN数据
        USB2CANFD.CANFD_MSG[] CanMsg = (USB2CANFD.CANFD_MSG[])new USB2CANFD.CANFD_MSG().toArray(5);
        for (int i = 0; i < 5; i++){
            CanMsg[i].Flags = USB2CANFD.CANFD_MSG_FLAG_FDF;//bit[0]-BRS,bit[1]-ESI,bit[2]-FDF,bit[6..5]-Channel,bit[7]-RXD
            CanMsg[i].DLC = 16;
            CanMsg[i].ID = i|USB2CANFD.CANFD_MSG_FLAG_IDE;
            for (int j = 0; j < CanMsg[i].DLC; j++){
                CanMsg[i].Data[j] = (byte)j;
            }
        }
        int SendedMsgNum = USB2CANFD.INSTANCE.CANFD_SendMsg(DevHandle, SendCANIndex, CanMsg, 5);
        if (SendedMsgNum >= 0){
        	System.out.println(String.format("Success send frames:%d", SendedMsgNum));
        }else{
        	System.out.println("Send CAN data failed!");
            return;
        }
        //接收数据
        //延时
        try {
			Thread.sleep(10);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        //读取接收数据缓冲中的数据
        USB2CANFD.CANFD_MSG[] CanMsgBuffer = (USB2CANFD.CANFD_MSG[])new USB2CANFD.CANFD_MSG().toArray(1024);
        int GetMsgNum = USB2CANFD.INSTANCE.CANFD_GetMsg(DevHandle, ReceiveCANIndex, CanMsgBuffer, 1024);
        if (GetMsgNum > 0){
            for (int i = 0; i < GetMsgNum; i++){
            	System.out.println(String.format("CanMsg[%d].ID = 0x%08X", i, CanMsgBuffer[i].ID & USB2CANFD.CANFD_MSG_FLAG_ID_MASK));
            	System.out.println(String.format("CanMsg[%d].TimeStamp = %d", i, CanMsgBuffer[i].TimeStamp));
            	System.out.println(String.format("CanMsg[%d].DLC = %d", i, CanMsgBuffer[i].DLC));
            	System.out.print(String.format("CanMsg[%d].Data = ", i));
                for (int j = 0; j < CanMsgBuffer[i].DLC; j++)
                {
                	System.out.print(String.format("0x%02X ", CanMsgBuffer[i].Data[j]));
                }
                System.out.println("");
            }
        }else if (GetMsgNum < 0){
        	System.out.println("Get CAN data error!");
        }
        //停止接收数据
        ret = USB2CANFD.INSTANCE.CANFD_StopGetMsg(DevHandle, SendCANIndex);
        if (ret != USB2CANFD.CANFD_SUCCESS){
        	System.out.println("Stop receive CANFD failed!");
            return;
        }else{
        	System.out.println("Stop receive CANFD Success!");
        }
        System.out.println("CAN test success!");
    }
}
