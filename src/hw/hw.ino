/* Copyright 2022 The TensorFlow Authors. All Rights Reserved.

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

#include "constants.h"
#include "main_functions.h"
#include "model.h"
#include "output_handler.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace {
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
int inference_count = 0;

constexpr int kTensorArenaSize = 2000;
uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

// The name of this function is important for Arduino compatibility.
void setup() {
  tflite::InitializeTarget();

  // Map the model into a usable data structure. This doesn't involve any
  // copying or parsing, it's a very lightweight operation.
  model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    MicroPrintf(
        "Model provided is schema version %d not equal "
        "to supported version %d.",
        model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // This pulls in all the operation implementations we need.
  // NOLINTNEXTLINE(runtime-global-variables)
  static tflite::AllOpsResolver resolver;

  // Build an interpreter to run the model with.
  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors.
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    MicroPrintf("AllocateTensors() failed");
    return;
  }

  // Obtain pointers to the model's input and output tensors.
  input = interpreter->input(0);
  output = interpreter->output(0);

  // Keep track of how many inferences we have performed.
  inference_count = 0;
}

void load_data(const float* data, TfLiteTensor * input)
{
    //for (int i = 0; i < input->bytes; ++i)
    for (int i = 0; i < 110; ++i)
    {
      // quantize the input, then send to the model...
      int8_t x_quantized = data[i] / input->params.scale + input->params.zero_point;
      input->data.int8[i] = x_quantized;
    }
}

// The name of this function is important for Arduino compatibility.
void loop() {
  // Calculate an x value to feed into the model. We compare the current
  // inference_count to the number of inferences per cycle to determine
  // our position within the range of possible x values the model was
  // trained on, and use this to calculate a value.
  float x = 9.80580370e-01;
  // float x[110] = {9.80580370e-01, 9.95648267e-02, 9.12149037e-01, 3.16358783e-03, 
  //                         2.01203996e-02, 2.01203996e-02, 4.45788585e-04, 3.15653886e-01,
  //                         3.10521403e-02, 9.12149037e-01, 9.87149652e-01, 8.36772578e-02,
  //                         8.62832051e-01, 1.28903323e-02, 5.76937706e-03, 5.76937706e-03,
  //                         1.05818115e-04, 5.08647758e-01, 6.10697111e-03, 8.62832051e-01,
  //                         9.90974335e-01, 2.21812730e-02, 6.60626352e-01, 2.44961325e-03,
  //                         1.95529650e-02, 1.95529650e-02, 4.23623950e-04, 4.15288125e-01,
  //                         2.53718840e-02, 6.60626352e-01, 1.16735378e-01, 4.83901570e-04,
  //                         4.39536966e-04, 2.48039869e-02, 2.73325914e-04, 2.73325914e-04,
  //                         1.56500001e-07, 4.76488983e-01, 1.66694970e-04, 4.39536966e-04,
  //                         7.88196755e-32, 1.49018576e-33, 3.01862816e-33, 2.47231194e-02,
  //                         2.46610879e-34, 2.46610879e-34, 1.21388465e-67, 3.95472611e-01,
  //                         1.73300565e-34, 3.01862816e-33, 9.03147850e-01, 3.28390942e-02,
  //                         1.46899796e-01, 5.75652798e-02, 3.70167737e-02, 3.70167737e-02,
  //                         1.46099378e-03, 5.08397289e-01, 2.76867262e-02, 1.46899796e-01,
  //                         1.84001110e-01, 9.17207741e-02, 4.00768558e-01, 5.05028807e-02,
  //                         2.04835446e-01, 2.04835446e-01, 4.19741884e-02, 1.76589094e-01,
  //                         1.99773002e-01, 4.00768558e-01, 2.34100205e-03, 9.98957731e-04,
  //                         6.19903365e-04, 8.92526686e-02, 7.21029136e-04, 7.21029136e-04,
  //                         5.25391825e-07, 4.30017306e-01, 3.78371701e-04, 6.19903365e-04,
  //                         4.31120127e-07, 1.73401022e-08, 2.47726258e-08, 5.76758973e-02,
  //                         5.55625191e-09, 5.55625191e-09, 2.91185194e-17, 8.72918045e-01,
  //                         3.22401834e-09, 2.47726258e-08, 9.81176971e-01, 2.50765264e-02,
  //                         7.52940060e-01, 4.72668282e-02, 1.53380921e-02, 1.53380921e-02,
  //                         2.62794352e-04, 3.02159123e-01, 1.92956155e-02, 7.52940060e-01,
  //                         1.95290008e-02, 4.21546857e-01, 3.44167868e-01, 4.03191949e-03,
  //                         5.31554012e-01, 5.31554012e-01, 2.82550313e-01, 3.32329851e-01,
  //                         5.45095615e-01, 3.44167868e-01};
  // float position = static_cast<float>(inference_count) /
  //                  static_cast<float>(kInferencesPerCycle);
  // float x = position * kXrange;

  // Quantize the input from floating-point to integer
  // int8_t x_quantized = x / input->params.scale + input->params.zero_point;
  // // Place the quantized input in the model's input tensor
  // input->data.int8[0] = x_quantized;

  int8_t x_quantized = x / input->params.scale + input->params.zero_point;
  input->data.int8[0] = x_quantized;
  // load_data(x, input);

  // Run inference, and report any error
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    MicroPrintf("Invoke failed on x: %f\n", static_cast<double>(x));
    return;
  }

  // Obtain the quantized output from model's output tensor
  int8_t y_quantized = output->data.int8[0];
  // Dequantize the output from integer to floating-point
  float y = (y_quantized - output->params.zero_point) * output->params.scale;

  // Output the results. A custom HandleOutput function can be implemented
  // for each supported hardware target.
  // HandleOutput(x, y);
  MicroPrintf("Output y: %f\n", y);

  // Increment the inference_counter, and reset it if we have reached
  // the total number per cycle
  inference_count += 1;
  if (inference_count >= kInferencesPerCycle) inference_count = 0;
}
