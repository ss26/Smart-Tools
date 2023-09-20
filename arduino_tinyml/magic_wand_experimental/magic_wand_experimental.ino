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
#include <avr/pgmspace.h>

#include "main_functions.h"

#include "test_data.h"

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
constexpr int kTensorArenaSize = 20 * 1024;
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

double a;
constexpr int label_count = 4;
const char* labels[label_count] = {"engrave", "cut", "route", "sand"};


// float f[] PROGMEM = {0.017452, 3.14159};

float normed_data;
float min_val;
float max_val;

int count;
float correct_guesses = 0;
float incorrect_guesses = 0;
float percent;
float label;

void loop() {
  
  // else{
  //   count = 0;
  // }

  // Attempt to read new data from the accelerometer.
  // bool got_data =
  //     ReadAccelerometer(error_reporter, model_input->data.f, input_length);
  // // If there was no new data, wait until next time.
  // if (!got_data) return;

    // TF_LITE_REPORT_ERROR(error_reporter, "ee %d", data);
  
  // for (int i = count*111; i < count*111 + 110; i++) {
  for (int i = 0; i < 110; i++)
  {
    //first row has 0.001 quantile, j is col
    min_val = pgm_read_float(&quant_arr[i]);
    //last row (5th) has 0.999 quantile, j is col
    max_val = pgm_read_float(&quant_arr[i] + 110*4);

    normed_data = (pgm_read_float(&data_arr[count*111 + i]) - min_val) / (max_val - min_val);

    Serial.print(normed_data,6);
    Serial.print(" ");

    model_input->data.f[i] = normed_data;

    }
    Serial.println(" ");

  // Run inference, and report any error.
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    TF_LITE_REPORT_ERROR(error_reporter, "Invoke failed on index: %d\n",
                         begin_index);
    return;
  }

  float max_score;
  int max_index;
  for (int i = 0; i < label_count; ++i) {
    float score = interpreter->output(0)->data.f[i];
    if ((i == 0) || (score > max_score)) {
      max_score = score;
      max_index = i;
    }
  }

  if (count < 25){

  Serial.println(count);
  label = pgm_read_float(&data_arr[110] + count*111);
  Serial.print(label, 6);
  Serial.print(" ");
  Serial.print(interpreter->output(0)->data.f[0], 6);
  Serial.print(" ");
  Serial.print(interpreter->output(0)->data.f[1], 6);
  Serial.print(" ");
  Serial.print(interpreter->output(0)->data.f[2], 6);
  Serial.print(" ");
  Serial.print(interpreter->output(0)->data.f[3], 6);
  Serial.print(" | ");
  Serial.print(max_score, 6);
  Serial.print(" ");
  Serial.println(max_index);

  if(label != max_index){
    incorrect_guesses++;
  }
  else{
    correct_guesses++;
  }

  Serial.print(correct_guesses);
  Serial.print(" ");
  Serial.print(incorrect_guesses);
  Serial.print(" ");
  percent = correct_guesses / (incorrect_guesses+correct_guesses);
  Serial.println(percent, 6);


  count++;
  }
  else
  {
    count=0;
    incorrect_guesses=0;
    correct_guesses=0;

  }


  // Analyze the results to obtain a prediction
  // int gesture_index = PredictGesture(interpreter->output(0)->data.f);

  // Produce an output
  // HandleOutput(error_reporter, gesture_index);
}
