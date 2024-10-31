kernel RampKernel: ImageComputationKernel<ePixelWise>
{
  Image<eRead, eAccessPoint, eEdgeClamped> src; // the input image
  Image<eWrite> dst; // the output image

  param:
    int key_order[50]; // The order of the keys
    int available_memory[50];
    float key_positions[50];
    float key_values[50];
    float bezier_handle_positions[100];
    float bezier_handle_values[100];
    int key_index = 0;

  local:
    float3 coefficients;  // This local variable is not exposed to the user.

  // In define(), parameters can be given labels and default values.
  void define() {
  }

  // The init() function is run before any calls to process().
  // Local variables can be initialized here.
  void init() {
    // Initialise coefficients according to rec. 709 standard.
    coefficients.x = 0.2126f;
    coefficients.y = 0.7152f;
    coefficients.z = 0.0722f;
  }

  void process() {
    // Read the input image
    SampleType(src) input = src();

    // Isolate the RGB components
    float3 srcPixel(input.x, input.y, input.z);

    // Calculate luma
    float luma = srcPixel.x * coefficients.x
               + srcPixel.y * coefficients.y
               + srcPixel.z * coefficients.z;
    // Apply saturation

    // Write the result to the output image
  }
};
