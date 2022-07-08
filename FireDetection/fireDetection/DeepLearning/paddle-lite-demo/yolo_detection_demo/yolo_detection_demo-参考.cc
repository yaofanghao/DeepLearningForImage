// Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Run in ~/code/Paddle-Lite-Demo/PaddleLite-armlinux-demo/yolo_detection_demo $
// with serial 115200
// average time 800ms

#include "paddle_api.h"
#include <arm_neon.h>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <stdio.h>
#include <sys/time.h>
#include <vector>
#include <iostream>
#include <iomanip>
#include <ctime>
#include <string>
#include <CppLinuxSerial/SerialPort.hpp>
#include "easylogging++.h"



extern "C"
{
#include "apriltag.h"
#include "tag36h11.h"
#include "tag25h9.h"
#include "tag16h5.h"
#include "tagCircle21h7.h"
#include "tagCircle49h12.h"
#include "tagCustom48h12.h"
#include "tagStandard41h12.h"
#include "tagStandard52h13.h"
#include "common/getopt.h"
#include "apriltag_pose.h"
}

INITIALIZE_EASYLOGGINGPP

using namespace std;
using namespace cv;

using namespace mn::CppLinuxSerial;


typedef std::uint16_t times16b;

/*
    Parameter Set
*/
int WARMUP_COUNT = 0;
int REPEAT_COUNT = 1;
int carImageWidth = 0;
int carImageHeight = 0;
const int CPU_THREAD_NUM = 4;
const paddle::lite_api::PowerMode CPU_POWER_MODE =
    paddle::lite_api::PowerMode::LITE_POWER_FULL;
const std::vector<int64_t> INPUT0_SHAPE = {1, 3, 320, 320};
const std::vector<int64_t> INPUT1_SHAPE = {1, 2};
const std::vector<float> mean = {0.485f, 0.456f, 0.406f};
const std::vector<float> scale = {0.229f, 0.224f, 0.225f};
const float SCORE_THRESHOLD = 0.5f;
char Predict_Result;
char Data_1_high, Data_0_low;
double distanceMeasureParameter = 61.0470795077, hoistCheckParameter, carDistanceConvertPara;

struct RESULT
{
    cv::Rect rec;
    int class_id;
    float prob;
};

/*
    Apriltag Detect and found function
*/
vector<float> apriltag_measurement(cv::Mat &frame, double tagSize)
{
    apriltag_family_t *tf = tag36h11_create();
    ;
    apriltag_detector_t *td = apriltag_detector_create();
    td->quad_decimate = 2.0;
    td->quad_sigma = 0.0;
    td->nthreads = 1;
    td->debug = 0;
    td->refine_edges = 1;
    apriltag_detector_add_family(td, tf);
    vector<float> apriltagResult(3, 10);
    Mat gray;
    int i = 1;
    while (i > 0)
    {
        cvtColor(frame, gray, COLOR_BGR2GRAY);

        // Make an image_u8_t header for the Mat data
        image_u8_t im = {.width = gray.cols,
                         .height = gray.rows,
                         .stride = gray.cols,
                         .buf = gray.data};

        zarray_t *detections = apriltag_detector_detect(td, &im);
        // Draw detection outlines
        for (int i = 0; i < zarray_size(detections); i++)
        {
            apriltag_detection_t *det;
            apriltag_detection_info_t info;
            double fx = (3.8 / 3.984) * gray.cols;
            double fy = (3.8 / 2.952) * gray.rows;
            double cx = gray.cols / 2;
            double cy = gray.rows / 2;
            double tagsize = tagSize;
            info.tagsize = tagsize;
            info.fx = fx;
            info.fy = fy;
            info.cx = cx;
            info.cy = cy;
            apriltag_pose_t pose;
            zarray_get(detections, i, &det);
            info.det = det;
            double err = estimate_tag_pose(&info, &pose);
            apriltagResult[0] = matd_get(pose.t, 0, 0);
            apriltagResult[1] = matd_get(pose.t, 0, 1);
            apriltagResult[2] = matd_get(pose.t, 0, 2);
            LOG(INFO) << "[XYZ] transcation is " << apriltagResult[0] << " " << apriltagResult[1] << " " << apriltagResult[2];
            line(frame, Point(det->p[0][0], det->p[0][1]),
                 Point(det->p[1][0], det->p[1][1]),
                 Scalar(0, 0xff, 0), 2);
            line(frame, Point(det->p[0][0], det->p[0][1]),
                 Point(det->p[3][0], det->p[3][1]),
                 Scalar(0, 0, 0xff), 2);
            line(frame, Point(det->p[1][0], det->p[1][1]),
                 Point(det->p[2][0], det->p[2][1]),
                 Scalar(0xff, 0, 0), 2);
            line(frame, Point(det->p[2][0], det->p[2][1]),
                 Point(det->p[3][0], det->p[3][1]),
                 Scalar(0xff, 0, 0), 2);

            stringstream ss;
            ss << det->id;
            String text = ss.str();
            int fontface = FONT_HERSHEY_SCRIPT_SIMPLEX;
            double fontscale = 1.0;
            int baseline;
            Size textsize = getTextSize(text, fontface, fontscale, 2,
                                        &baseline);
            putText(frame, text, Point(det->c[0] - textsize.width / 2, det->c[1] + textsize.height / 2),
                    fontface, fontscale, Scalar(0xff, 0x99, 0), 2);
        }
        apriltag_detections_destroy(detections);
        i--;
        imshow("Tag Detections", frame);
        if (waitKey(30) >= 0)
            break;
    }

    apriltag_detector_destroy(td);
    tag36h11_destroy(tf);
    return apriltagResult;
}

inline int64_t get_current_us()
{
    struct timeval time;
    gettimeofday(&time, NULL);
    return 1000000LL * (int64_t)time.tv_sec + (int64_t)time.tv_usec;
}

/*
    Load Labels from file
*/
std::vector<std::string> load_labels(const std::string &path)
{
    std::ifstream file;
    std::vector<std::string> labels;
    file.open(path);
    while (file)
    {
        std::string line;
        std::getline(file, line);
        labels.push_back(line);
    }
    file.clear();
    file.close();
    return labels;
}

/*
    Preprocess Function
*/

void preprocess(cv::Mat &img, int width,
                int height, float *input_data)
{
    cv::Mat rgb_img;
    cv::cvtColor(img, rgb_img, cv::COLOR_BGR2RGB);
    cv::resize(rgb_img, rgb_img, cv::Size(width, height), 0.f, 0.f, cv::INTER_CUBIC);
    cv::Mat imgf;
    rgb_img.convertTo(imgf, CV_32FC3, 1 / 255.f);
    std::vector<float> mean = {0.485f, 0.456f, 0.406f};
    std::vector<float> scale = {0.229f, 0.224f, 0.225f};
    const float *dimg = reinterpret_cast<const float *>(imgf.data);
    int image_size = height * width;
    // NHWC->NCHW
    float32x4_t vmean0 = vdupq_n_f32(mean[0]);
    float32x4_t vmean1 = vdupq_n_f32(mean[1]);
    float32x4_t vmean2 = vdupq_n_f32(mean[2]);
    float32x4_t vscale0 = vdupq_n_f32(1.0f / scale[0]);
    float32x4_t vscale1 = vdupq_n_f32(1.0f / scale[1]);
    float32x4_t vscale2 = vdupq_n_f32(1.0f / scale[2]);
    float *input_data_c0 = input_data;
    float *input_data_c1 = input_data + image_size;
    float *input_data_c2 = input_data + image_size * 2;
    int i = 0;
    for (; i < image_size - 3; i += 4)
    {
        float32x4x3_t vin3 = vld3q_f32(dimg);
        float32x4_t vsub0 = vsubq_f32(vin3.val[0], vmean0);
        float32x4_t vsub1 = vsubq_f32(vin3.val[1], vmean1);
        float32x4_t vsub2 = vsubq_f32(vin3.val[2], vmean2);
        float32x4_t vs0 = vmulq_f32(vsub0, vscale0);
        float32x4_t vs1 = vmulq_f32(vsub1, vscale1);
        float32x4_t vs2 = vmulq_f32(vsub2, vscale2);
        vst1q_f32(input_data_c0, vs0);
        vst1q_f32(input_data_c1, vs1);
        vst1q_f32(input_data_c2, vs2);
        dimg += 12;
        input_data_c0 += 4;
        input_data_c1 += 4;
        input_data_c2 += 4;
    }
    for (; i < image_size; i++)
    {
        *(input_data_c0++) = (*(dimg++) - mean[0]) / scale[0];
        *(input_data_c1++) = (*(dimg++) - mean[1]) / scale[1];
        *(input_data_c2++) = (*(dimg++) - mean[2]) / scale[2];
    }
}
/*
    Postprocess Function
*/
std::vector<RESULT> postprocess(const float *output_data,
                                int64_t output_size,
                                std::vector<std::string> &word_labels,
                                const float score_threshold,
                                cv::Mat &image)
{
    std::vector<int> palletIDPack;
    std::vector<int> carIDPack;
    if (output_data == nullptr)
    {
        std::cerr << "[ERROR] data can not be nullptr\n";
        exit(1);
    }
    std::vector<RESULT> rect_out;
    for (int iw = 0; iw < output_size; iw++)
    {
        int oriw = image.cols;
        int orih = image.rows;
        if (output_data[1] > score_threshold)
        {
            RESULT obj;

            int x = static_cast<int>(output_data[2]);
            int y = static_cast<int>(output_data[3]);
            int w = static_cast<int>(output_data[4] - output_data[2] + 1);
            int h = static_cast<int>(output_data[5] - output_data[3] + 1);
            cv::Rect rec_clip =
                cv::Rect(x, y, w, h) & cv::Rect(0, 0, image.cols, image.rows);
            obj.class_id = static_cast<int>(output_data[0]);
            obj.prob = output_data[1];
            obj.rec = rec_clip;

            if (obj.class_id != 2)
            {
                LOG(INFO) << "Pallet Find!"
                          << " Push Pallet ID In" << obj.class_id;
                palletIDPack.push_back(obj.class_id);
            }
            else
            {
                LOG(INFO) << "Car Find!"
                          << " Push Car ID In" << obj.class_id;
                ::carImageWidth = w;
                ::carImageHeight = h;
                carIDPack.push_back(obj.class_id);
            }

            if (w > 0 && h > 0 && obj.prob <= 1)
            {
                rect_out.push_back(obj);
                cv::rectangle(image, rec_clip, cv::Scalar(0, 0, 255), 1, cv::LINE_AA);
                std::string text = "Unknown";
                std::string str_prob = std::to_string(obj.prob);
                if (word_labels.size() > 0 && obj.class_id >= 0 &&
                    obj.class_id < word_labels.size())
                {
                    text = word_labels[obj.class_id] + ": " +
                           str_prob.substr(0, str_prob.find(".") + 4);
                }
                int font_face = cv::FONT_HERSHEY_COMPLEX_SMALL;
                double font_scale = 1.f;
                int thickness = 1;
                cv::Size text_size =
                    cv::getTextSize(text, font_face, font_scale, thickness, nullptr);
                float new_font_scale = w * 0.5 * font_scale / text_size.width;
                text_size = cv::getTextSize(
                    text, font_face, new_font_scale, thickness, nullptr);
                cv::Point origin;
                origin.x = x + 3;
                origin.y = y + text_size.height + 3;
                cv::putText(image,
                            text,
                            origin,
                            font_face,
                            new_font_scale,
                            cv::Scalar(0, 255, 255),
                            thickness,
                            cv::LINE_AA);
                LOG(INFO) << "Object Data->Name: " << text << "\n"
                          << "->Score: " << obj.prob << "\n"
                          << "->loacation[x,y,w,h]: " << x << " " << y << " " << w << " " << h << "\n";
            }
        }
        output_data += 6;
    }
    bool palletBool = palletIDPack.empty();
    bool carBool = carIDPack.empty();
    if (palletBool)
    {
        if (carBool)
        {
            ::Predict_Result = 0x06;
            ::carImageWidth = 0;
            ::carImageHeight = 0;
        }
        else
        {
            ::Predict_Result = 0x01;
        }
    }
    else
    {
        if (carBool)
        {
            ::Predict_Result = 0x02;
            ::carImageWidth = 0;
            ::carImageHeight = 0;
        }
        else
        {
            ::Predict_Result = 0x03;
        }
    }

    return rect_out;
}
/*
    Process Function
*/
cv::Mat process(cv::Mat &input_image,
                std::vector<std::string> &word_labels,
                std::shared_ptr<paddle::lite_api::PaddlePredictor> &predictor)
{
    // Preprocess image and fill the data of input tensor
    int input_width = INPUT0_SHAPE[2];
    int input_height = INPUT0_SHAPE[3];
    // Input 0
    std::unique_ptr<paddle::lite_api::Tensor> input_tensor0(std::move(predictor->GetInput(1)));
    input_tensor0->Resize({1, 3, input_width, input_width});
    auto *input_data0 = input_tensor0->mutable_data<float>();
    preprocess(input_image, input_width, input_height,
               input_data0);
    // Input 1
    std::unique_ptr<paddle::lite_api::Tensor> input_tensor1(std::move(predictor->GetInput(0)));
    input_tensor1->Resize({1, 2});
    auto *input_data1 = input_tensor1->mutable_data<float>();
    input_data1[0] = input_image.rows;
    input_data1[1] = input_image.cols;

    std::unique_ptr<paddle::lite_api::Tensor> input_tensor2(std::move(predictor->GetInput(2)));
    input_tensor2->Resize({1, 2});
    auto *data2 = input_tensor2->mutable_data<float>();
    data2[0] = 1;
    data2[1] = 1;
    predictor->Run();
    std::unique_ptr<const paddle::lite_api::Tensor> output_tensor(
        std::move(predictor->GetOutput(0)));
    const float *output_data = output_tensor->data<float>();
    int64_t output_size = 1;
    for (auto dim : output_tensor->shape())
    {
        output_size *= dim;
    }
    cv::Mat output_image = input_image.clone();
    auto rec_out = postprocess(
        output_data, static_cast<int>(output_size / 6), word_labels, SCORE_THRESHOLD, output_image);
    return output_image;
}
void runFunctionB0Predict()
{
    // run prediction
    ::Data_1_high = 0x00;
    ::Data_0_low = 0x00;
}
void runFunctionB1Distance(cv::Mat &frame,
                           std::vector<std::string> &word_labels,
                           std::shared_ptr<paddle::lite_api::PaddlePredictor> &predictor)
{
    // run apriltag distance measure
    double func2TagSize = 0.115;
    vector<float> apriltagResult = apriltag_measurement(frame, func2TagSize);
    bool noApriltag = (apriltagResult[0] == apriltagResult[1]) && (apriltagResult[0] == 10);
    if (noApriltag)
    {
        // if not fine apriltag, goto object detect and calculate image size
        cv::Mat output_image = process(frame, word_labels, predictor);
        if (::Predict_Result == 0x01 || ::Predict_Result == 0x03)
        {
            int imageSize = ::carImageWidth * ::carImageHeight;
            times16b imageRealDistance = imageSize * ::carDistanceConvertPara;
            ::Data_0_low = imageRealDistance;
            ::Data_1_high = imageRealDistance >> 8;
        }
        else
        {
            ::Data_0_low = 0xff;
            ::Data_1_high = 0xff;
            LOG(INFO) << "(B1-Function)Apriltag Didn't Find!, so does the prediction";
        }
    }
    else
    {
        times16b distanceResult = apriltagResult[2] * distanceMeasureParameter;
        ::Data_0_low = distanceResult;
        ::Data_1_high = distanceResult >> 8;
        LOG(INFO) << "(B1-Function)Apriltag Find!"
                  << " Parameter is "
                  << distanceMeasureParameter << "Distance Result is " << apriltagResult[2] * distanceMeasureParameter;
    }
}
void runFunctionB2Hoist(cv::Mat &frame)
{
    // run apriltag check Hoist
    double func1TagSize = 0.053;
    vector<float> apriltagResult = apriltag_measurement(frame, func1TagSize);
    bool noApriltag = (apriltagResult[0] == apriltagResult[1]) && (apriltagResult[0] == 10);
    float heightCheckResult = apriltagResult[1] - hoistCheckParameter;
    ::Data_1_high = 0x00;
    if (!noApriltag)
    {
        // find hoist, check hight
        if (-0.29 <= heightCheckResult <= 0.29)
        {
            ::Data_0_low = 0x01;
        }
        else
        {
            ::Data_0_low = 0x05;
        }
    }
    else
    {
        // no hoist find!
        ::Data_0_low = 0x06;
    }
    LOG(INFO) << "(B2-Function)Apriltag Find Result: " << !noApriltag << "Final Check Result is " << (int)Data_0_low;
}

int main(int argc, char **argv)
{
    time_t t = time(0);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&t), "%F %X");
    el::Configurations defaultConf;
    defaultConf.setToDefault();
    defaultConf.setGlobally(
        el::ConfigurationType::Filename, ss.str());
    el::Loggers::reconfigureLogger("default", defaultConf);
    el::Logger *defaultLogger = el::Loggers::getLogger("default");

    LOG(INFO) << "Programm Start";
    int fd;
    int count;
    unsigned int nextTime;
    cv::VideoCapture cap(-1);
    cap.set(CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);
    if (!cap.isOpened())
    {
        std::cout << "cam not opened!" << std::endl;
        return -1;
    }
    /*
    Serial INIT

    Create serial port object and open serial port at 57600 buad, 8 data bits, no parity bit, and one stop bit (8n1)
    Use SerialPort serialPort("/dev/ttyACM0", 13000); instead if you want to provide a custom baud rate
    */

    SerialPort serialPort("/dev/ttyS2", BaudRate::B_115200, NumDataBits::EIGHT, Parity::NONE, NumStopBits::ONE);
    serialPort.SetTimeout(-1); // Block when reading until any data is received
    serialPort.Open();
    vector<uint8_t> write_buffer = {0x88, 0x1D, 0x2D, 0x3D, 0x4D, 0x01, 0xCC, 0x10, 0x20, 0xDA, 0xDA, 0x01, 0x02};
    vector<uint8_t> read_buffer;
    serialPort.WriteBinary(write_buffer);

    /*
        Model INIT
    */
    string mode = argv[1];
    string parameterPath = "/home/pi/code/Paddle-Lite-Demo/PaddleLite-armlinux-demo/yolo_detection_demo/parameter.txt";
    vector<string> parameterTable = load_labels(parameterPath);
    string model_path = parameterTable[0];
    string label_path = parameterTable[1];
    std::vector<std::string> word_labels = load_labels(label_path);

    paddle::lite_api::MobileConfig config;
    config.set_model_from_file(model_path);
    config.set_threads(CPU_THREAD_NUM);
    config.set_power_mode(CPU_POWER_MODE);
    std::shared_ptr<paddle::lite_api::PaddlePredictor> predictor =
        paddle::lite_api::CreatePaddlePredictor<paddle::lite_api::MobileConfig>(config);
    LOG(INFO) << "Cam and Serial and Model Init Done";

    /*
        Debug Mode or Run Mode Set
    */
    LOG(INFO) << "MODE IS " << mode;
    if (mode == "debug")
    {
        // 重置为1 用于标定
        LOG(INFO) << "SWITCH TO PARAMETER SET MODE!";
        LOG(INFO) << "FUNCT2 FUNCT3 's parameter has been set to 1 and 0!";
        ::distanceMeasureParameter = 1;
        ::hoistCheckParameter = 0;
        // 进入调试模式， 当前功能2， 功能3的缩放参数重置为1， 请根据标定结果计算并修改./parameter.txt下的参数信息
    }
    else if (mode == "run")
    {
        ::distanceMeasureParameter = stod(parameterTable[2]);
        ::hoistCheckParameter = stod(parameterTable[3]);
    }
    else
    {
        LOG(ERROR) << "Missing right argument!";
        return -1;
    }

    LOG(INFO) << "Programm Start";
    while (1)
    {
        serialPort.ReadBinary(read_buffer);
        if (read_buffer.size() != 13)
        {
            LOG(INFO) << "buffer size is not 13";
        }
        times16b runtimes = (read_buffer[7] << 8) + read_buffer[8];
        switch (read_buffer[6])
        {
        case 0xb0:
            LOG(INFO) << "Receive Funct code B0, Go Predict";
            for (times16b i = 0; i < runtimes; i++)
            {
                cv::Mat input_image;
                cap >> input_image;
                cv::Mat output_image = process(input_image, word_labels, predictor);
                write_buffer[10] = Predict_Result;
                write_buffer[8] = (i + 1);
                write_buffer[7] = (i + 1) >> 8;
                LOG(INFO) << "(B0)Runtimes at " << (i + 1) << " Total Runtimes is " << runtimes;
                LOG(INFO) << "(B0)Prediction Result Code Judge is " << (int)Predict_Result;
                serialPort.WriteBinary(write_buffer);
                cv::imshow("Object Detection Demo", output_image);
                if (cv::waitKey(1) == char('q'))
                {
                    break;
                }
            }
            break;
        case 0xb1:
            LOG(INFO) << "Receive Funct code B1, Go Distance Measure";
            for (times16b i = 0; i < runtimes; i++)
            {
                cv::Mat input_image;
                cap >> input_image;
                runFunctionB1Distance(input_image, word_labels, predictor);
                write_buffer[7] = (i + 1) >> 8;
                write_buffer[8] = (i + 1);
                write_buffer[9] = Data_1_high;
                write_buffer[10] = Data_0_low;
                LOG(INFO) << "(B1)Runtimes at " << (i + 1) << "Total Runtimes is " << runtimes;
                serialPort.WriteBinary(write_buffer);
            }
            break;
        case 0xb2:
            LOG(INFO) << "Receive Funct code B2, Go Hoist Check";
            for (times16b i = 0; i < runtimes; i++)
            {
                cv::Mat input_image;
                cap >> input_image;
                runFunctionB2Hoist(input_image);
                write_buffer[7] = (i + 1) >> 8;
                write_buffer[8] = (i + 1);
                write_buffer[9] = Data_1_high;
                write_buffer[10] = Data_0_low;
                LOG(INFO) << "(B2)Runtimes at " << (i + 1) << "Total Runtimes is " << runtimes;
                serialPort.WriteBinary(write_buffer);
            }
            break;
        default:
            break;
        }
        fflush(stdout);
    }
    cap.release();
    cv::destroyAllWindows();
    return 0;
}
