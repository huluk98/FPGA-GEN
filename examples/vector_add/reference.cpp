#include <cstdint>

extern "C" void vector_add_reference(const std::int32_t *a,
                                     const std::int32_t *b,
                                     std::int32_t *out, int n) {
  for (int i = 0; i < n; ++i) {
    out[i] = a[i] + b[i];
  }
}
