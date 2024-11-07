class CubicBezier {
public:
    // Calculate the point on the Bézier curve for a given parameter t
    static void evaluate(double t, double x0, double y0, double x1, double y1, double x2, double y2, double x3, double y3, double& x, double& y) {
        double one_minus_t = 1.0 - t;
        double t2 = t * t;
        double t3 = t2 * t;
        double one_minus_t2 = one_minus_t * one_minus_t;
        double one_minus_t3 = one_minus_t2 * one_minus_t;

        // Calculate x(t) and y(t)
        x = one_minus_t3 * x0 + 3 * one_minus_t2 * t * x1 + 3 * one_minus_t * t2 * x2 + t3 * x3;
        y = one_minus_t3 * y0 + 3 * one_minus_t2 * t * y1 + 3 * one_minus_t * t2 * y2 + t3 * y3;
    }

    // Find t corresponding to a given x value using binary search
    static double findTForX(double targetX, double x0, double x1, double x2, double x3) {
        double low = 0.0, high = 1.0, mid;
        for (int i = 0; i < 100; ++i) {  // Iterations for accuracy
            mid = (low + high) / 2.0;
            double xMid;
            evaluate(mid, x0, 0.0, x1, 0.0, x2, 0.0, x3, 0.0, xMid, 0.0);

            if (xMid < targetX)
                low = mid;
            else
                high = mid;
        }
        return mid;
    }

    // Get the Y value for a given X value
    static double getYForX(double targetX, double x0, double y0, double x1, double y1, double x2, double y2, double x3, double y3) {
        double t = findTForX(targetX, x0, x1, x2, x3);
        double x, y;
        evaluate(t, x0, y0, x1, y1, x2, y2, x3, y3, x, y);
        return y;  // Return the Y value corresponding to the X
    }
};

int main() {
    // Example Bézier curve points
    double x0 = 0.0, y0 = 0.0;  // Start point
    double x1 = 1.0, y1 = 2.0;  // Control point 1
    double x2 = 2.0, y2 = 2.0;  // Control point 2
    double x3 = 3.0, y3 = 0.0;  // End point

    double targetX = 1.5;  // The X value where we want to sample Y

    double y = CubicBezier::getYForX(targetX, x0, y0, x1, y1, x2, y2, x3, y3);
    std::cout << "The Y value at X = " << targetX << " is Y = " << y << std::endl;

    return 0;
}