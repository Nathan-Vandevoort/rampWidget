kernel RampKernel: ImageComputationKernel<ePixelWise>
{
  Image<eRead, eAccessPoint, eEdgeClamped> src; // the input image
  Image<eWrite> dst; // the output image

  param:
    int key_order[50]; // The order of the keys
    int memory[50];
    int key_types[50];
    float key_positions[50];
    float key_values[50];
    float bezier_handle_positions[100];
    float bezier_handle_values[100];
    int key_index = 0;

  local:
    float3 coefficients;  // This local variable is not exposed to the user.
    int numberOfKeys;

  void define() {
  }

  // The init() function is run before any calls to process().
  // Local variables can be initialized here.
  void init() {

      // Get the number of keys
      for(int i = 0; i < 50; i++){
          if (key_order[i] == -1) {
              break;
          }
          numberOfKeys += 1;
      }
  }

  void process() {
    // Read the input image
    SampleType(src) input = src();

    int myIndex = 0;
    int nextIndex = 0;
    float position = 0;
    float value = 0;
    // 0 is linear 1 is bezier
    int key_type = 0;
    float handle01_position = 0;
    float handle01_value = 0;
    float handle02_position = 0;
    float handle02_value = 0;
    float solved_value = 0.0;
    float end_position = 0.0;
    float end_value = 0.0;

    float clampedInput = clamp(input.x, 0, 1);

    for(int i = 0; i < numberOfKeys; i++){
      if(key_positions[key_order[i]] > clampedInput){
        break;
      }
      myIndex = key_order[i];
      nextIndex = key_order[i+1];
    }

    position = key_positions[myIndex];
    value = key_values[myIndex];
    key_type = key_types[myIndex];
    handle01_position = bezier_handle_positions[myIndex * 2 + 1];
    handle01_value = bezier_handle_values[myIndex * 2 + 1];
    handle02_position = bezier_handle_positions[nextIndex * 2];
    handle02_value = bezier_handle_values[nextIndex * 2];
    end_position = key_positions[nextIndex];
    end_value = key_values[nextIndex];

    // bezier interpolation
    if (key_type == 0){
      float t = 0.0;
      float solved_t = 0.0;
      float x = 0.0;
      float y = 0.0;
      float x0 = 0.0;
      float y0 = 0.0;
      float x1 = 0.0;
      float y1 = 0.0;
      float x2 = 0.0;
      float y2 = 0.0;
      float x3 = 0.0;
      float y3 = 0.0;

      // solve for t
      float low = 0.0;
      float high = 1.0;
      float mid;
      x0 = position; y0 = 0.0;
      x1 = handle01_position;
      y1 = 0.0;
      x2 = handle02_position;
      y2 = 0.0;
      x3 = end_position;
      y3 = 0.0;

      for (int i = 0; i < 200; i++){
        mid = (low + high) / 2.0;
        float xMid;

        //evaluate
        t = mid;

        float one_minus_t = 1.0 - t;
        float t2 = t * t;
        float t3 = t2 * t;
        float one_minus_t2 = one_minus_t * one_minus_t;
        float one_minus_t3 = one_minus_t2 * one_minus_t;
        xMid = one_minus_t3 * x0 + 3 * one_minus_t2 * t * x1 + 3 * one_minus_t * t2 * x2 + t3 * x3;

        if (xMid < clampedInput){
          low = mid;
        } else {
          high = mid;
        }

      }

      solved_t = mid;

      //evaluate for Y
      low = 0.0;
      high = 1.0;
      t = solved_t;
      x0 = position;
      y0 = value;
      x1 = handle01_position;
      y1 = handle01_value;
      x2 = handle02_position;
      y2 = handle02_value;
      x3 = end_position;
      y3 = end_value;

      float one_minus_t = 1.0 - t;
      float t2 = t * t;
      float t3 = t2 * t;
      float one_minus_t2 = one_minus_t * one_minus_t;
      float one_minus_t3 = one_minus_t2 * one_minus_t;
      solved_value = one_minus_t3 * y0 + 3 * one_minus_t2 * t * y1 + 3 * one_minus_t * t2 * y2 + t3 * y3;
    }

    float4 srcPixel(solved_value, solved_value, solved_value, input.w);
    dst() = srcPixel;
  }
};