#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "recalcD.h"

#define NUM 3000
#define T0 0.0
#define OUT 0
#define LEV 3
#define TEND 4.0
#define TAU 0.0001
#define P1_INT_EQUIVALENT 32000
#define RECALC_U_BSTEP 0.5
#define EPS 1e-15
#define BARRIER TAU * NUM * P1_INT_EQUIVALENT
#define BARRIER1 TAU * (NUM - 1) * P1_INT_EQUIVALENT

double V0[MASS];
double V[MASS];
double Ub[MASS];

int part0_Count_p1[MASS];
int part0_Count_m1[MASS];
int part_Count_p1[MASS];
int part_Count_m1[MASS];

int sign(double x)
{
    if (x < EPS && x > -EPS)
        return 0;
    if (x > 0.0)
        return 1;
    if (x < 0.0)
        return -1;
}

inline int NeedReCalcUB(double x)
{
    return (x - trunc(x / RECALC_U_BSTEP) * RECALC_U_BSTEP > (RECALC_U_BSTEP - TAU)) ? 1 : 0;
}

void LoadParticleArrays(double u)
{
    recalcD(u, Ub);
    int NN, Numt;
    register int i;
    for (i = 0; i < MASS; i++)
    {
        part0_Count_p1[i] = 0;
        part0_Count_m1[i] = 0;
        NN = round(NUM * fabs(Ub[i]) / LEV);
        if (sign(Ub[i]) == 1)
        {
            part0_Count_p1[i] = NN;
            part_Count_p1[i] = NN;
        }
        else
            if (sign(Ub[i]) == -1)
            {
                part0_Count_m1[i] = NN;
                part_Count_m1[i] = NN;
            }
        Numt = part0_Count_p1[i] - part0_Count_m1[i];
        V0[i] = LEV * (double)Numt / NUM;
        V[i] = V0[i];
    }
}

inline void DiffSchemeOneStep()
{
    register int i;
    for (i = 0; i < MASS - 1; i++)
        V[i] = V0[i] + TAU * V0[i+1];
    V[i] = V0[i];
}

inline void MonteCarloOneStepInt()
{
    int n1, a1, b1, a2, b2;
    register int i;
    for (i = 0; i < MASS - 1; i++)
    {
        n1 = rand() % NUM;
        if ((part0_Count_p1[i + 1] + part0_Count_m1[i + 1]) <= n1)
            continue;

        a2 = rand() % P1_INT_EQUIVALENT;
	    b2 = BARRIER1;

        if (a2 <= b2 && (part0_Count_p1[i + 1] - n1) > 0)
            if (part0_Count_m1[i] > 0)
                part_Count_m1[i] = part0_Count_m1[i] - 1;
            else
                if (part0_Count_p1[i] < NUM)
                    part_Count_p1[i] = part0_Count_p1[i] + 1;

	    a1 = rand() % P1_INT_EQUIVALENT;
	    b1 = BARRIER;

        if (a1 <= b1 &&
            (n1 - part0_Count_p1[i + 1] + 1) *
            (part0_Count_p1[i + 1] + part0_Count_m1[i + 1] - n1) > 0)
        {
            if (part0_Count_p1[i] > 0)
                part_Count_p1[i] = part0_Count_p1[i] - 1;
            else
                if (part0_Count_m1[i] < NUM)
                    part_Count_m1[i] = part0_Count_m1[i] + 1;
        }
    }
}

inline void UpdateTimeLayers()
{
    register int i;
    for (i = 0; i < MASS; i++)
    {
        part0_Count_p1[i] = part_Count_p1[i];
        part0_Count_m1[i] = part_Count_m1[i];
        V0[i] = V[i];
    }
}

inline double AnalyticSolution(double t)
{
    return U0 / (U0 - exp(t) * (U0 - 1.0));
}

int main()
{
    srand(time(NULL));
    LoadParticleArrays(U0);
    int Numt, steps = (int)((TEND - T0) / TAU);
    double Time[steps], C[steps], y[steps], v[steps];
    double Conc, t = T0;
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC_RAW, &start);
    register unsigned int i = 0;
    while (t <= TEND)
    {
	    DiffSchemeOneStep();
	    MonteCarloOneStepInt();
        Numt = part0_Count_p1[OUT] - part0_Count_m1[OUT];
	    Conc = LEV * (double)Numt / NUM;
        if (NeedReCalcUB(t))//) && (t < 2 || t > 2))
        // if (t > 2.5 + TAU && t < 2.5 - TAU)
            LoadParticleArrays(Conc);
        Time[i] = t;
        C[i] = Conc;
        y[i] = AnalyticSolution(t);
        v[i++] = V0[OUT];
	    UpdateTimeLayers();
	    t += TAU;
	}
    clock_gettime(CLOCK_MONOTONIC_RAW, &end);
    printf("Main cycle time, s: %lf\n", end.tv_sec-start.tv_sec + 0.000000001*(end.tv_nsec-start.tv_nsec));

#ifndef NOOUT
    const char *mc = "./out/monteCarlo.txt";
    const char *num = "./out/diffScheme.txt";
    const char *ana = "./out/analyticSolution.txt";
    FILE *fMC = fopen(mc, "w");
    FILE *fNum = fopen(num, "w");
    FILE *fAna = fopen(ana, "w");
    if (fMC == NULL || fNum == NULL || fAna == NULL)
    {
        printf("File opening error!\n");
        fclose(fMC);
        fclose(fNum);
        fclose(fAna);
        exit(EXIT_FAILURE);
    }
    for (i = 0; i < steps; i++)
    {
        fprintf(fMC, "%lf\t%.10lf\n", Time[i], C[i]);
        fprintf(fNum, "%lf\t%.10lf\n", Time[i], v[i]);
        fprintf(fAna, "%lf\t%.10lf\n", Time[i], y[i]);
    }
    fclose(fMC);
    fclose(fNum);
    fclose(fAna);
#endif
    return 0;
}
