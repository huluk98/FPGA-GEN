#include <array>
#include <cstdint>
#include <iostream>
#include <random>

extern "C" void vector_add_reference(const std::int32_t *, const std::int32_t *,
                                     std::int32_t *, int);
void vector_add(const std::int32_t *, const std::int32_t *, std::int32_t *, int);

namespace {

constexpr int kDepth = 16;
constexpr int kDirectedTests = 6;
constexpr int kRandomTests = 64;
constexpr std::uint32_t kSeed = 7;
constexpr std::int32_t kSentinel = 0x13579BDF;

using Values = std::array<std::int32_t, kDepth>;

bool check_case(int test_id, const Values &a, const Values &b, int n) {
  Values expected;
  Values actual;
  expected.fill(kSentinel);
  actual.fill(kSentinel);

  vector_add_reference(a.data(), b.data(), expected.data(), n);
  vector_add(a.data(), b.data(), actual.data(), n);

  for (int i = 0; i < kDepth; ++i) {
    if (expected[i] != actual[i]) {
      std::cerr << "mismatch test=" << test_id << " index=" << i
                << " expected=" << expected[i] << " actual=" << actual[i]
                << '\n';
      return false;
    }
  }
  return true;
}

} // namespace

int main() {
  int tested = 0;
  Values a{};
  Values b{};

  auto run = [&](int n) {
    const bool passed = check_case(tested, a, b, n);
    ++tested;
    return passed;
  };

  if (!run(kDepth)) {
    return 1;
  }

  a.fill(1);
  b.fill(-1);
  if (!run(kDepth)) {
    return 1;
  }

  for (int i = 0; i < kDepth; ++i) {
    a[i] = (i % 2 == 0) ? 1'000'000'000 : -1'000'000'000;
    b[i] = -a[i];
  }
  if (!run(kDepth)) {
    return 1;
  }

  for (int i = 0; i < kDepth; ++i) {
    a[i] = i * 17 - 100;
    b[i] = 200 - i * 13;
  }
  if (!run(7)) {
    return 1;
  }

  a.fill(1'000'000'000);
  b.fill(1'000'000'000);
  if (!run(kDepth)) {
    return 1;
  }

  a.fill(-1'000'000'000);
  b.fill(-1'000'000'000);
  if (!run(0)) {
    return 1;
  }

  std::mt19937 generator(kSeed);
  auto value = [&]() {
    return static_cast<std::int32_t>(generator() % 2'000'001U) - 1'000'000;
  };
  for (int test = 0; test < kRandomTests; ++test) {
    for (int i = 0; i < kDepth; ++i) {
      a[i] = value();
      b[i] = value();
    }
    if (!run(static_cast<int>(generator() % (kDepth + 1)))) {
      return 1;
    }
  }

  if (tested != kDirectedTests + kRandomTests) {
    std::cerr << "internal test-count error\n";
    return 2;
  }

  std::cout << "PASS host_tests=" << tested << " seed=" << kSeed << '\n';
  return 0;
}
