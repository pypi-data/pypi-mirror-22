#include <turbodbc/time_helpers.h>

#ifdef _WIN32
#include <windows.h>
#endif
#include <cstring>
#include <sql.h>

#include <boost/date_time/gregorian/gregorian_types.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>

namespace turbodbc {

    boost::posix_time::ptime const timestamp_epoch({1970, 1, 1}, {0, 0, 0, 0});

    int64_t timestamp_to_microseconds(char const * data_pointer)
    {
        auto & sql_ts = *reinterpret_cast<SQL_TIMESTAMP_STRUCT const *>(data_pointer);
        intptr_t const microseconds = sql_ts.fraction / 1000;
        boost::posix_time::ptime const ts({static_cast<unsigned short>(sql_ts.year), sql_ts.month, sql_ts.day},
                {sql_ts.hour, sql_ts.minute, sql_ts.second, microseconds});
        return (ts - timestamp_epoch).total_microseconds();
    }

    boost::gregorian::date const date_epoch(1970, 1, 1);

    intptr_t date_to_days(char const * data_pointer)
    {
        auto & sql_date = *reinterpret_cast<SQL_DATE_STRUCT const *>(data_pointer);
        boost::gregorian::date const date(sql_date.year, sql_date.month, sql_date.day);
        return (date - date_epoch).days();
    }

}
