/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include <TensorFlowLite.h>

#include "main_functions.h"

#include "accelerometer_handler.h"
#include "constants.h"
#include "gesture_predictor.h"
#include "magic_wand_model_data.h"
#include "output_handler.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace {
tflite::ErrorReporter* error_reporter = nullptr;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* model_input = nullptr;
int input_length;

// Create an area of memory to use for input, output, and intermediate arrays.
// The size of this will depend on the model you're using, and may need to be
// determined by experimentation.
constexpr int kTensorArenaSize = 200 * 1024;
uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

// The name of this function is important for Arduino compatibility.
void setup() {
  // Set up logging. Google style is to avoid globals or statics because of
  // lifetime uncertainty, but since this has a trivial destructor it's okay.
  static tflite::MicroErrorReporter micro_error_reporter;  // NOLINT
  error_reporter = &micro_error_reporter;

  // Map the model into a usable data structure. This doesn't involve any
  // copying or parsing, it's a very lightweight operation.
  model = tflite::GetModel(g_magic_wand_model_data);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    TF_LITE_REPORT_ERROR(error_reporter,
                         "Model provided is schema version %d not equal "
                         "to supported version %d.",
                         model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // Pull in only the operation implementations we need.
  // This relies on a complete list of all the ops needed by this graph.
  // An easier approach is to just use the AllOpsResolver, but this will
  // incur some penalty in code space for op implementations that are not
  // needed by this graph.
  // static tflite::MicroMutableOpResolver<5> micro_op_resolver;  // NOLINT
  // micro_op_resolver.AddConv2D();
  // micro_op_resolver.AddDepthwiseConv2D();
  // micro_op_resolver.AddFullyConnected();
  // micro_op_resolver.AddMaxPool2D();
  // micro_op_resolver.AddSoftmax();

  static tflite::AllOpsResolver resolver;

  // Build an interpreter to run the model with.
  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize, error_reporter);
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors.
  interpreter->AllocateTensors();

  // Obtain pointer to the model's input tensor.
  model_input = interpreter->input(0);
  // if ((model_input->dims->size != 4) || (model_input->dims->data[0] != 1) ||
  //     (model_input->dims->data[1] != 128) ||
  //     (model_input->dims->data[2] != kChannelNumber) ||
  //     (model_input->type != kTfLiteFloat32)) {
  //   TF_LITE_REPORT_ERROR(error_reporter,
  //                        "Bad input tensor parameters in model");
  //   return;
  // }

  // input_length = model_input->bytes / sizeof(float);

  // TfLiteStatus setup_status = SetupAccelerometer(error_reporter);
  // if (setup_status != kTfLiteOk) {
  //   TF_LITE_REPORT_ERROR(error_reporter, "Set up failed\n");
  // }
}

constexpr int label_count = 4;
const char* labels[label_count] = {"engrave", "cut", "route", "sand"};

float feature_buffer[110] = {9.80580370e-01, 9.95648267e-02, 9.12149037e-01, 3.16358783e-03, 
                                2.01203996e-02, 2.01203996e-02, 4.45788585e-04, 3.15653886e-01,
                                3.10521403e-02, 9.12149037e-01, 9.87149652e-01, 8.36772578e-02,
                                8.62832051e-01, 1.28903323e-02, 5.76937706e-03, 5.76937706e-03,
                                1.05818115e-04, 5.08647758e-01, 6.10697111e-03, 8.62832051e-01,
                                9.90974335e-01, 2.21812730e-02, 6.60626352e-01, 2.44961325e-03,
                                1.95529650e-02, 1.95529650e-02, 4.23623950e-04, 4.15288125e-01,
                                2.53718840e-02, 6.60626352e-01, 1.16735378e-01, 4.83901570e-04,
                                4.39536966e-04, 2.48039869e-02, 2.73325914e-04, 2.73325914e-04,
                                1.56500001e-07, 4.76488983e-01, 1.66694970e-04, 4.39536966e-04,
                                7.88196755e-32, 1.49018576e-33, 3.01862816e-33, 2.47231194e-02,
                                2.46610879e-34, 2.46610879e-34, 1.21388465e-67, 3.95472611e-01,
                                1.73300565e-34, 3.01862816e-33, 9.03147850e-01, 3.28390942e-02,
                                1.46899796e-01, 5.75652798e-02, 3.70167737e-02, 3.70167737e-02,
                                1.46099378e-03, 5.08397289e-01, 2.76867262e-02, 1.46899796e-01,
                                1.84001110e-01, 9.17207741e-02, 4.00768558e-01, 5.05028807e-02,
                                2.04835446e-01, 2.04835446e-01, 4.19741884e-02, 1.76589094e-01,
                                1.99773002e-01, 4.00768558e-01, 2.34100205e-03, 9.98957731e-04,
                                6.19903365e-04, 8.92526686e-02, 7.21029136e-04, 7.21029136e-04,
                                5.25391825e-07, 4.30017306e-01, 3.78371701e-04, 6.19903365e-04,
                                4.31120127e-07, 1.73401022e-08, 2.47726258e-08, 5.76758973e-02,
                                5.55625191e-09, 5.55625191e-09, 2.91185194e-17, 8.72918045e-01,
                                3.22401834e-09, 2.47726258e-08, 9.81176971e-01, 2.50765264e-02,
                                7.52940060e-01, 4.72668282e-02, 1.53380921e-02, 1.53380921e-02,
                                2.62794352e-04, 3.02159123e-01, 1.92956155e-02, 7.52940060e-01,
                                1.95290008e-02, 4.21546857e-01, 3.44167868e-01, 4.03191949e-03,
                                5.31554012e-01, 5.31554012e-01, 2.82550313e-01, 3.32329851e-01,
                                5.45095615e-01, 3.44167868e-01};

void loop() {
  // Attempt to read new data from the accelerometer.
  // bool got_data =
  //     ReadAccelerometer(error_reporter, model_input->data.f, input_length);
  // // If there was no new data, wait until next time.
  // if (!got_data) return;

  for (int i = 0; i < 110; ++i) {
      model_input->data.f[i] = feature_buffer[i];
    }

  // Run inference, and report any error.
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    TF_LITE_REPORT_ERROR(error_reporter, "Invoke failed on index: %d\n",
                         begin_index);
    return;
  }

  int8_t max_score;
    int max_index;
    for (int i = 0; i < label_count; ++i) {
      const int8_t score = interpreter->output(0)->data.f[i];
      if ((i == 0) || (score > max_score)) {
        max_score = score;
        max_index = i;
      }
    }
    TF_LITE_REPORT_ERROR(error_reporter, "Found %s (%d)", labels[max_index], max_score);
    if (labels[max_index] == "engrave" || labels[max_index] == "cut" || labels[max_index] == "sand" || labels[max_index] == "route"){
        digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(1000);                       // wait for a second
        digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
        delay(1000);
    }

  // Analyze the results to obtain a prediction
  // int gesture_index = PredictGesture(interpreter->output(0)->data.f);

  // Produce an output
  // HandleOutput(error_reporter, gesture_index);
}
