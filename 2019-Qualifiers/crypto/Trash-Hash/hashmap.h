#ifndef HASHMAP_H
#define HASHMAP_H

typedef struct {
    uint64_t hash;
    char* value;
} bucket;

typedef struct {
    uint64_t mask;
    bucket* buckets;
} hashmap;

hashmap map_create(void);
char* map_get(hashmap map, char* key);
int map_insert(hashmap map, char* key, char* value);

#endif
