#pragma once

#include <cstdint>

namespace turbodbc {
    int64_t timestamp_to_microseconds(char const * data_pointer);
    intptr_t date_to_days(char const * data_pointer);
}
