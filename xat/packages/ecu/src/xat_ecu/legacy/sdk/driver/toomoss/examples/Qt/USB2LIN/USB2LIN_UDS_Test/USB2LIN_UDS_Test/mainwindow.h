#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMessageBox>
#include "usb2lin_ex.h"
#include "usb_device.h"
#include "lin_uds.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pushButtonInit_clicked();

    void on_pushButton_clicked();

private:
    Ui::MainWindow *ui;
    bool initFlag;
};
#endif // MAINWINDOW_H
