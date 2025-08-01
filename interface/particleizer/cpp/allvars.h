#ifndef ALLVARS_H
#define ALLVARS_H

#define X 0
#define Y 1

typedef struct
{
    int id;
    double pos[2];
    double vel[2];
    double accel[2];
    double mass;
    double rho;
    double h;
    double p;
    double c;
    double du;
    double u;
    int *nn;
    int nNeighbors;
    double *dx;
    double *dy;
    double *dz;
    double *r;
    double *W;
    double *dWx;
    double *dWy;
    double *dWz;
    int type;
} Particles;

// Puntero global al array de partículas y su tamaño
extern Particles *part;
extern int nPart;

#endif // ALLVARS_H
