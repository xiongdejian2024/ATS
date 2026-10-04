#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "usb_device.h"
#include "usb2ow.h"
#include <QtDebug>
#include <QFile>
#include <QFileDialog>
#include <QMessageBox>
#include <QDateTime>
#include <QThread>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void timerEvent(QTimerEvent *event);

private slots:
    void on_pushButtonStart_clicked();

    void on_pushButtonSaveDataToFile_clicked();

private:
    Ui::MainWindow *ui;
    int GetDataTimer;
    bool ChEnFlag[16];
    bool AutoSaveData;
    QFile *pAutoSaveFile;
};
#endif // MAINWINDOW_H
