#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <assert.h>

void insertion_sort(int *a, int n) {
    int i, j, t;
    for (i = 1; i < n; i++) {
        t = a[i];
        for (j = i; j > 0 && t < a[j - 1]; j--) {
            a[j] = a[j - 1];
        };
        a[j] = t;
    };
};

void quick_sort(int *a, int n, int cutoff) {
    int i, j, p, t;
    if (n < 2) {
        return;
    }
    else if (n <= cutoff) {
        insertion_sort(a, n);
    }
    else {
        p = a[n / 2];
        for (i = 0, j = n - 1;; i++, j--) {
            while (a[i] < p)
                i++;
            while (p < a[j])
                j--;
            if (i >= j)
                break;
            t = a[i];
            a[i] = a[j];
            a[j] = t;
        };

        quick_sort(a, i, cutoff);
        quick_sort(a + i, n - i, cutoff);
    };
};
 
int main(int argc, char *argv[]) {
    int size   = 67108864;
    int cutoff = (int) strtol(argv[1], (char **)NULL, 10);

    int *a = (int *) malloc(sizeof(int) * size);

    srand(size);
    
    int i;
    for (i = 0; i < size; i++) {
        a[i] = rand();
    };

    quick_sort(a, size, cutoff);

    for (i = 0; i < size - 1; i++) {
        assert(a[i] <= a[i + 1]);
    };
    return 0;
};
