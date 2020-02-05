#include <stdio.h>
#include <math.h>
#define EPS 1e-4
double a[MONOMIAL_COUNT] = ALPHAS;
char p[MONOMIAL_COUNT] = POWERS;
int main()
{
    double t = 0.0;
    double u = U0, f;
    FILE *fa = fopen("./out/ana.txt", "w");
    do
    {
        f = 0.0;
        int i;
        for (i = 0; i < MONOMIAL_COUNT; i++)
            f += a[i] * pow(u, p[i]);
        u += DT * f;
        t += DT;
        fprintf(fa, "%lf\t%lf\n", t, u);
    }
    while (u < 1.0 && u > EPS);
    fclose(fa);
}
