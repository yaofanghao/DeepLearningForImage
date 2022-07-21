TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt


SOURCES += \
    ./utils.cpp \
    ./tools.cpp 


HEADERS += \
    ./utils.h \


OTHER_FILES = Makefile

################################################################################
# OpenCV settings
################################################################################
OPENCV_TOP  = /opt/opencv-2.4.5
#OPENCV_TOP  = $$(OpenCV_DIR)

LIBS += -L$$OPENCV_TOP/lib \
        -lopencv_calib3d -lopencv_contrib -lopencv_core \
        -lopencv_features2d -lopencv_flann -lopencv_gpu \
        -lopencv_highgui -lopencv_imgproc -lopencv_legacy \
        -lopencv_ml -lopencv_nonfree -lopencv_objdetect \
        -lopencv_photo -lopencv_stitching -lopencv_ts \
        -lopencv_video -lopencv_videostab

INCLUDEPATH += $$OPENCV_TOP/include $$OPENCV_TOP/include/opencv \
                ./eigen3
