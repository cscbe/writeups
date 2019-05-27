#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>

#include "hashmap.h"
#include "flag.h"

void help() {
    printf("Usage:\n");
    printf("set <key> <value>: insert a value into the hash map\n");
    printf("get <key>: get a value from the hash map\n");
}

int main() {
    hashmap map = map_create();
    map_insert(map, "flag", FLAG);

    unsigned long buflen = 0;
    int nread;
    char *buf = NULL, *cmd, *key, *value;

    printf("Very Stable Hash Map v0.0.1 command-line interface\n");
    while (1) {
        nread = getline(&buf, &buflen, stdin);
        if (nread <= 0)
            return 0;

        if ((cmd = strtok(buf, " \t\n")) == NULL)
            continue;

        if (strcasecmp(cmd, "set") == 0) {
            key = strtok(NULL, " \t\n");
            value = strtok(NULL, " \t\n");
            if (value == NULL) {
                help();
                continue;
            }
            if (map_insert(map, key, value) < 0)
                printf("could not insert value: bucket is full\n");
            else
                printf("succesfully inserted value\n");
        } else if (strcasecmp(cmd, "get") == 0) {
            key = strtok(NULL, " \t\n");
            if (key == NULL) {
                help();
                continue;
            }
            if (strcmp(key, "flag") == 0) {
                printf("this service doesn't leak private information.\n");
                continue;
            }
            if ((value = map_get(map, key)) == NULL)
                printf("key not found\n");
            else {
                printf("value = %s\n", value);
            }
        } else {
            printf("unknown command\n");
            help();
        }
    }
}
