using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;

namespace USB2XXX
{
    class HEX_DECODE
    {
        //LIN UDS地址定义
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
        public struct HEX_FILE_BLOCK
        {
            public UInt32 StartAddr;     //数据块起始地址
            public UInt32 DataNum;     //数据块字节数
            public IntPtr pData;       //数据块数据存储指针
        };

        //存储类型定义
        public const Int32 MEMTYPE_UINT8 = 1;  ///<1个地址单元存储1字节数据
        public const Int32 MEMTYPE_UINT16 = 2;  ///<1个地址单元存储2字节数据
        public const Int32 MEMTYPE_UINT32 = 4;  ///<1个地址单元存储4字节数据

        [DllImport("USB2XXX.dll")]
        public static extern Int32 hexfile_load_file(StringBuilder filename, Byte[] fileBuf);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 hexfile_convert_s19(Byte[] fileBuf, Int32 lenFileBuf, IntPtr pHexFileBlock, Int32 maxBlockNum, Byte memType);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 hexfile_convert_ihx(Byte[] fileBuf, Int32 lenFileBuf, IntPtr pHexFileBlock, Int32 maxBlockNum, Byte memType);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 hexfile_convert_txt(Byte[] fileBuf, Int32 lenFileBuf, IntPtr pHexFileBlock, Int32 maxBlockNum, Byte memType);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 hexfile_free_data(ref HEX_FILE_BLOCK pHexFileBlock, Int32 maxBlockNum);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 hexfile_save_image(StringBuilder filename, HEX_FILE_BLOCK[] pHexFileBlock, Int32 maxBlockNum, Byte memType, Byte fillBytes);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 hexfile_convert_image(Byte[] pOutData, HEX_FILE_BLOCK[] pHexFileBlock, Int32 maxBlockNum, Byte memType, Byte fillBytes);
    }
}
