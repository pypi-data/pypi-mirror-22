#include <stdlib.h>
#include <stdint.h>

typedef struct Tuple Tuple;
typedef struct TupleItem TupleItem;

struct Tuple {
    size_t num;
    TupleItem *items;
};

struct TupleItem {
    uint8_t type;
    unsigned char *buffer;
    union {
        Tuple tuple;
        char *chars;
        unsigned char *uchars;
        int8_t char_;
        uint8_t uchar;
        int16_t int16;
        uint16_t uint16;
        int32_t int32;
        uint32_t uint32;
        int64_t int64;
        uint64_t uint64;
    } typed;
};

int main(int argc, char *argv[])    {

}
