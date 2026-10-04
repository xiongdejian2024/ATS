QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# The following define makes your compiler emit warnings if you use
# any Qt feature that has been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

win32{
    message($$QT_ARCH)
    contains(QT_ARCH, i386) {
        LIBS += -L$$PWD/libs/windows/x86 -lUSB2XXX
    } else {
        LIBS += -L$$PWD/libs/windows/x86_64 -lUSB2XXX
    }
}

unix:!macx{
    message($$QMAKE_HOST.arch)
    unix:contains(QMAKE_HOST.arch, x86_64){
        LIBS += -L$$PWD/libs/linux/x86_64 -lUSB2XXX
    }
    unix:contains(QMAKE_HOST.arch, x86){
        LIBS += -L$$PWD/libs/linux/x86 -lUSB2XXX
    }
    unix:contains(QMAKE_HOST.arch, aarch64){
        LIBS += -L$$PWD/libs/linux/aarch64 -lUSB2XXX
    }
    unix:contains(QMAKE_HOST.arch, armv7){
        LIBS += -L$$PWD/libs/linux/armv7 -lUSB2XXX
    }
    unix:contains(QMAKE_HOST.arch, mips64){
        LIBS += -L$$PWD/libs/linux/mips64 -lUSB2XXX
    }
}

SOURCES += \
    MS5803_01.cpp \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    MS5803_01.h \
    mainwindow.h \
    usb2iic.h \
    usb_device.h

FORMS += \
    mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
