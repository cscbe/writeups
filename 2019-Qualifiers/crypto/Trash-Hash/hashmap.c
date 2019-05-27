#include <inttypes.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include "hashmap.h"

uint64_t h(char *key) {
    uint64_t state = 0x0123456789abcdef;
    char* cur = key;
    while (*cur != '\0') {
        state += *cur;
        state ^= 0xbadc0de;
        state = (state >> 30) | (state << 34);
        state -= *cur;
        state *= 3;
        cur++;
    }
    return state;
}

hashmap map_create(void) {
    size_t capacity = 0x1000000;
    bucket* buckets;
    if ((buckets = calloc(capacity, sizeof(bucket))) == NULL)
        exit(EXIT_FAILURE);

    return (hashmap) { .mask = capacity - 1, .buckets = buckets };
}

char* map_get(hashmap map, char* key) {
    uint64_t hash = h(key);
    int offset = hash & map.mask;
    if (map.buckets[offset].hash == hash)
        return map.buckets[offset].value;
    return NULL;
}

int map_insert(hashmap map, char* key, char* value) {
    uint64_t hash = h(key);
    int offset = hash & map.mask;
    if (map.buckets[offset].value)
        return -1;
    map.buckets[offset].hash = hash;
    map.buckets[offset].value = malloc(strlen(value) + 1);
    strcpy(map.buckets[offset].value, value);
    return 0;
}
