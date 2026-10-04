#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    int DevHandle[20];
    int DevNum = USB_ScanDevice(DevHandle);
    for(int i=0;i<DevNum;i++){
        ui->comboBoxDevHandle->addItem(QString("%1").arg(DevHandle[i],8,16,QChar('0')).toUpper());
    }
    initFlag = false;
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButtonInit_clicked()
{
    unsigned int DevHandle = ui->comboBoxDevHandle->currentText().toUInt(NULL,16);
    if(USB_OpenDevice(DevHandle)){
        int ret = LIN_EX_Init(DevHandle,
                    ui->comboBoxChannel->currentIndex(),
                    ui->comboBoxBaudRate->currentText().toUInt(),
                    1);
        if(ret != LIN_EX_SUCCESS){
            QMessageBox::warning(this,tr("警告"),tr("初始化设备失败！"),QMessageBox::Ok);
        }else{
            initFlag = true;
        }
    }else{
        QMessageBox::warning(this,tr("警告"),tr("打开设备失败！"),QMessageBox::Ok);
    }
}

void MainWindow::on_pushButton_clicked()
{
    if(!initFlag){
        on_pushButtonInit_clicked();
        if(!initFlag){
            return;
        }
    }
    unsigned int DevHandle = ui->comboBoxDevHandle->currentText().toUInt(NULL,16);
    LIN_UDS_ADDR UDSAddr;
    UDSAddr.NAD = ui->spinBoxNAD->value();
    UDSAddr.ReqID = ui->spinBoxReqID->value();
    UDSAddr.ResID = ui->spinBoxRespID->value();
    UDSAddr.CheckType = 0;//一般都是标准校验
    UDSAddr.STmin = ui->spinBoxSTmin->value();
    uint8_t buffer[256];
    QStringList dataStrList = ui->lineEditReqData->text().split(" ");
    for(int i=0;i<dataStrList.length();i++){
        buffer[i] = dataStrList.at(i).toUInt(NULL,16);
    }
    int ret = LIN_UDS_Request(DevHandle,
                              ui->comboBoxChannel->currentIndex(),
                              &UDSAddr,
                              buffer,
                              dataStrList.length());
    if(ret == LIN_UDS_OK){
        ui->textBrowserLog->append("请求数据："+ui->lineEditReqData->text());
    }else{
        ui->textBrowserLog->append("请求数据失败！ret = "+QString("%1").arg(ret));
    }
    QApplication::processEvents();
    uint8_t outbuffer[256];
    ret = LIN_UDS_Response(DevHandle,
                           ui->comboBoxChannel->currentIndex(),
                           &UDSAddr,
                           outbuffer,
                           100);
    if(ret > 0){
        QString str;
        for(int i=0;i<ret;i++){
            str += QString("%1 ").arg(outbuffer[i],2,16,QChar('0')).toUpper();
        }
        ui->textBrowserLog->append("响应数据："+str);
    }else if(ret ==0 ){
        ui->textBrowserLog->append("无响应数据");
    }else{
        ui->textBrowserLog->append("响应数据失败！ret = "+QString("%1").arg(ret));
    }
}
