import com.toomoss.USB2XXX.USB_Device;
import com.toomoss.USB2XXX.USB2LIN_EX;
import com.toomoss.USB2XXX.USB2LIN_EX.LIN_EX_MSG;

public class USB2XXX_LIN_EX_MasterSimpleWriteReadTest {
	  /** 
     * Launch the application. 
     */  
    public static void main(String[] args) {   
        int ret;
        int DevHandle = 0;
        int[] DevHandleArry = new int[20];
        boolean state;
        byte LINMasterIndex = 0;
        //扫描当前连接的设备
        ret = USB_Device.INSTANCE.USB_ScanDevice(DevHandleArry);
        if(ret > 0){
        	System.out.println("Device Num = "+ret);
        	DevHandle = DevHandleArry[0];
        }else{
        	System.out.println("No device");
        	return;
        }
        //打开当前连接的设备
        state = USB_Device.INSTANCE.USB_OpenDevice(DevHandle);
        if(!state){
        	System.out.println("open device error");
        	return;
        }
        //读取设备信息
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
        //初始化配置LIN
        ret = USB2LIN_EX.INSTANCE.LIN_EX_Init(DevHandle,LINMasterIndex,9600,USB2LIN_EX.LIN_EX_MASTER);
        if(ret != USB2LIN_EX.LIN_EX_SUCCESS){
        	System.out.println("Config LIN failed!");
            return;
        }else{
        	System.out.println("Config LIN Success!");
        }
        //主机模式发送数据，调用一次发送一帧,发送帧ID为0x05
        byte[] WriteData = new byte[] {0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08};
        ret = USB2LIN_EX.INSTANCE.LIN_EX_MasterWrite(DevHandle,LINMasterIndex,(byte)0x05,WriteData,(byte)WriteData.length,(byte)0x01);
        if(ret < USB2LIN_EX.LIN_EX_SUCCESS){
        	System.out.println("Write LIN failed!");
            return;
        }else {
        	System.out.println("Write LIN data success!");
        }
        //主机模式读数据，调用一次读一次，读数据帧ID为0x06
        byte[] ReadData = new byte[8];
        int ReadDataNum = USB2LIN_EX.INSTANCE.LIN_EX_MasterRead(DevHandle,LINMasterIndex,(byte)0x06,ReadData);
        if(ReadDataNum < USB2LIN_EX.LIN_EX_SUCCESS){
        	System.out.println("Read LIN failed!");
            return;
        }
        System.out.printf("Read PID[%02X] Data=",0x06);
        for(int j=0;j<ReadDataNum;j++){
        	System.out.printf("%02X ",ReadData[j]);
        }
        System.out.println("");
        System.out.println("USB2LIN test success!");
    }  
}
