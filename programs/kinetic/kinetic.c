#include "SFMT.h"

#include <math.h>
#include <stdio.h>
#include <time.h>

double a[MONOMIAL_COUNT] = ALPHAS;
char p[MONOMIAL_COUNT] = POWERS;

int main()
{
    unsigned int particleCount = N * U0;
    register unsigned int i;
    double pInteraction[MONOMIAL_COUNT];
    for (i = 0; i < MONOMIAL_COUNT; i++)
    {
        pInteraction[i] = fabs(a[i] * N * DT);
        // printf("p[%d] = %lf\n", i, pInteraction[i]);
    }
    sfmt_t sfmt;
    sfmt_init_gen_rand(&sfmt, time(NULL));
    double curPt = U0, t = 0.0;
    FILE *fp = fopen(OUTPUT, "w");
    // fprintf(fp, "%lf\t%lf\n", t, curPt);
    register double r, rs;
    register unsigned int j;
    char res;
    struct timespec start, end;
    // clock_gettime(CLOCK_MONOTONIC_RAW, &start);
    while (curPt > 0.0 && curPt < 1.0) //curPt > 0.0 && curPt < 1.0
    {
        for (i = 0; i < MONOMIAL_COUNT; i++)
        {
            res = 1;
            for (j = 0; j < p[i]; j++)
            {
                rs = sfmt_genrand_res53(&sfmt);
                if (curPt < rs)
                    res = 0;
            }
            r = sfmt_genrand_res53(&sfmt);
            if (r <= pInteraction[i] && res)
                particleCount += a[i] > 0 ? 1 : -1;
        }
        t += DT;
        curPt = particleCount / (double)N;
        // fprintf(fp, "%lf\t%lf\n", t, curPt);
    }
    // clock_gettime(CLOCK_MONOTONIC_RAW, &end);
    // printf("%lf\n", end.tv_sec-start.tv_sec + 0.000000001*(end.tv_nsec-start.tv_nsec));
    fclose(fp);
    return 0;
}
