#include <stdio.h>
#include <stdlib.h>
#include <math.h>

char *INSTANCE = "instances/pla85900/pla85900.tsp";

int count_lines(char *filename) {
    FILE *file    = fopen(filename, "r");
    int character = 0;
    int lines     = 0;
    while(!feof(file)) {
      character = fgetc(file);
      if(character == '\n') {
        lines++;
      };
    };
    fclose(file);
    return lines;
};

void init_instance(char *filename, int **instance, int cities) {
    FILE *file = fopen(filename, "r");
    int i;
    for(i = 0; i < cities; i++) {
        fscanf(file, "%d %d %d", &instance[i][0],
               &instance[i][1], &instance[i][2]);
    };
    fclose(file);
};

void load_tour(char *filename, int *tour, int tour_size) {
    FILE *file = fopen(filename, "r");
    int i;
    for(i = 0; i < tour_size; i++) {
        fscanf(file, "%d", &tour[i]);
    };
    fclose(file);
};

unsigned long tour_cost(int **instance, int *tour, int tour_size) {
    int i;
    unsigned long cost = 0;
    unsigned long partial_cost;
    int city_a, a_x, a_y,
        city_b, b_x, b_y;

    for(i = 0; i < tour_size - 1; i++) {
        city_a        = tour[i] - 1;
        city_b        = tour[i + 1] - 1;

        a_x           = instance[city_a][1];
        a_y           = instance[city_a][2];

        b_x           = instance[city_b][1];
        b_y           = instance[city_b][2];

        partial_cost  = sqrt((double) (((b_x - a_x) * (b_x - a_x)) +
                                       ((b_y - a_y) * (b_y - a_y))));

        cost         += partial_cost;
    };
    return cost;
};

int main(int argc, char *argv[]) {
    int i;
    int tour_size = count_lines(INSTANCE) + 1;

    int *tour = (int *) malloc(sizeof(int) * tour_size);

    load_tour(argv[1], tour, tour_size);

    int **instance = (int **) malloc(sizeof(int *) * tour_size);
    for(i = 0; i < tour_size; i++) {
        instance[i] = (int *) malloc(3 * sizeof(int));
    };

    init_instance(INSTANCE, instance, tour_size - 1);

    printf("%lu\n", tour_cost(instance, tour, tour_size));
    return 0;
};
