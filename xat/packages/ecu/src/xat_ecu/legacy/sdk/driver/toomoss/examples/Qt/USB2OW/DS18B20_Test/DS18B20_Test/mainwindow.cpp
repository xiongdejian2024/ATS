#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    int DevHandles[20];
    int DevNum = USB_ScanDevice(DevHandles);
    for(int i=0;i<DevNum;i++){
        ui->comboBoxDevHandle->addItem(QString("%1").arg(DevHandles[i],8,16,QChar('0')).toUpper());
        USB_OpenDevice(DevHandles[i]);
    }
    pAutoSaveFile = NULL;
    AutoSaveData = false;
}

MainWindow::~MainWindow()
{
    killTimer(GetDataTimer);
    if(pAutoSaveFile != NULL){
        pAutoSaveFile->close();
    }
    delete ui;
}


void MainWindow::on_pushButtonStart_clicked()
{
    QCheckBox *pChEn[]={ui->checkBoxEnable_0,ui->checkBoxEnable_1,ui->checkBoxEnable_2,ui->checkBoxEnable_3,
                       ui->checkBoxEnable_4,ui->checkBoxEnable_5,ui->checkBoxEnable_6,ui->checkBoxEnable_7,
                       ui->checkBoxEnable_8,ui->checkBoxEnable_9,ui->checkBoxEnable_10,ui->checkBoxEnable_11,
                       ui->checkBoxEnable_12,ui->checkBoxEnable_13,ui->checkBoxEnable_14,ui->checkBoxEnable_15};
    int DevHandle = ui->comboBoxDevHandle->currentText().toUInt(NULL,16);
    if(ui->pushButtonStart->text()=="开始"){
        for(int i=0;i<16;i++){
            ChEnFlag[i] = pChEn[i]->isChecked();
            if(ChEnFlag[i]){
                OW_Init(DevHandle,1<<i,500,1);
                uint8_t WriteDataBuffer[8];
                WriteDataBuffer[0] = 0xCC;
                WriteDataBuffer[1] = 0x44;
                OW_Reset(DevHandle,1<<i);
                int ret = OW_WriteBytes(DevHandle,1<<i,WriteDataBuffer,2);
                if(ret != OW_SUCCESS){
                    QMessageBox::warning(this,"警告",QString("通道%1初始化传感器失败！").arg(i),QMessageBox::Ok);
                    return;
                }
            }
        }
        ui->pushButtonStart->setText("停止");
        GetDataTimer = startTimer(ui->spinBoxTimeRead->value());
    }else{
        killTimer(GetDataTimer);
        ui->pushButtonStart->setText("开始");
    }
}

void MainWindow::timerEvent(QTimerEvent *event)
{
    QLCDNumber *pTemp[]={ui->lcdNumberTemp_0,ui->lcdNumberTemp_1,ui->lcdNumberTemp_2,ui->lcdNumberTemp_3,ui->lcdNumberTemp_4,
                        ui->lcdNumberTemp_5,ui->lcdNumberTemp_6,ui->lcdNumberTemp_7,ui->lcdNumberTemp_8,ui->lcdNumberTemp_9,
                        ui->lcdNumberTemp_10,ui->lcdNumberTemp_11,ui->lcdNumberTemp_12,ui->lcdNumberTemp_13,ui->lcdNumberTemp_14,
                        ui->lcdNumberTemp_15};

    if(event->timerId()==GetDataTimer){
        int DevHandle = ui->comboBoxDevHandle->currentText().toUInt(NULL,16);
        for(int i=0;i<16;i++){
            if(ChEnFlag[i]){
                uint8_t WriteDataBuffer[8];
                uint8_t ReadDataBuffer[8];
                WriteDataBuffer[0] = 0xCC;
                WriteDataBuffer[1] = 0x44;
                int ret = OW_Reset(DevHandle,1<<i);
                ret = OW_WriteBytes(DevHandle,1<<i,WriteDataBuffer,2);
                QThread::msleep(200);
                WriteDataBuffer[0] = 0xCC;
                WriteDataBuffer[1] = 0xBE;
                ret = OW_Reset(DevHandle,1<<i);
                ret = OW_WriteReadBytes(DevHandle,1<<i,WriteDataBuffer,2,ReadDataBuffer,2,100);
                int16_t tmp = (ReadDataBuffer[1]<<8)|ReadDataBuffer[0];
                float temperature = (float)tmp * 0.0625;
                if(ret != OW_SUCCESS){
                    on_pushButtonStart_clicked();
                    QMessageBox::warning(this,"警告",QString("通道%1读传感器数据失败！").arg(i),QMessageBox::Ok);
                    return;
                }
                pTemp[i]->display(QString().asprintf("%.2f",temperature));
                if(AutoSaveData&&(pAutoSaveFile!=NULL)){
                    pAutoSaveFile->write(QString().asprintf("%.2f,",temperature).toUtf8());
                }
            }
        }
        if(AutoSaveData&&(pAutoSaveFile!=NULL)){
            QDateTime curDateTime=QDateTime::currentDateTime();
            pAutoSaveFile->write(curDateTime.toString("yyyy-MM-dd hh:mm:ss\r\n").toUtf8());
        }
    }
}

void MainWindow::on_pushButtonSaveDataToFile_clicked()
{
    if(ui->pushButtonSaveDataToFile->text()=="自动保存"){
        QCheckBox *pChEn[]={ui->checkBoxEnable_0,ui->checkBoxEnable_1,ui->checkBoxEnable_2,ui->checkBoxEnable_3,
                           ui->checkBoxEnable_4,ui->checkBoxEnable_5,ui->checkBoxEnable_6,ui->checkBoxEnable_7,
                           ui->checkBoxEnable_8,ui->checkBoxEnable_9,ui->checkBoxEnable_10,ui->checkBoxEnable_11,
                           ui->checkBoxEnable_12,ui->checkBoxEnable_13,ui->checkBoxEnable_14,ui->checkBoxEnable_15};
        for(int i=0;i<12;i++){
            ChEnFlag[i] = pChEn[i]->isChecked();
        }
        QString fileName = QFileDialog::getSaveFileName(
                                this,
                                tr("Save File"),
                                "",
                                "Comma separated value(*.csv);;Text (*.txt)");
        if(fileName.isNull()){
            return;
        }

        pAutoSaveFile = new QFile(fileName);
        if(!pAutoSaveFile->open(QIODevice::WriteOnly)){
            QMessageBox::warning(this,"警告","打开文件失败！",QMessageBox::Ok);
            return;
        }
        ui->lineEditFileName->setText(fileName);
        uint8_t UTF8_BOM[3]={0xEF,0xBB,0xBF};
        pAutoSaveFile->write((char*)UTF8_BOM,3);
        for(int i=0;i<16;i++){
            if(ChEnFlag[i]){
                pAutoSaveFile->write(QString("通道%1温度(℃),").arg(i).toUtf8());
            }
        }
        pAutoSaveFile->write(QString("日期时间\r\n").toUtf8());
        AutoSaveData = true;
        ui->pushButtonSaveDataToFile->setText("停止保存");
    }else{
        AutoSaveData = false;
        pAutoSaveFile->close();
        pAutoSaveFile = NULL;
        ui->pushButtonSaveDataToFile->setText("自动保存");
    }
}
