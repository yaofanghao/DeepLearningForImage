#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <string>
#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "utils.h"

using namespace std;
using namespace cv;


////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

int convert_img2map(CParamArray *pa)
{
    Mat                 img;

    string              fname, fn_out;
    FILE                *fp = NULL;

    int                 i;
    uint32_t            w, h, n;

    uint8_t             *pb;
    int8_t              *pm;

    // get input/output filenames
    fname = "../figure/complex_maze_bin.png";
    pa->s("fn_in", fname);

    fn_out = "../figure/complex_maze.dat";
    pa->s("fn_out", fn_out);

    img = imread(fname, IMREAD_GRAYSCALE);

    w = img.cols;
    h = img.rows;
    n = w*h;

    printf("img w, h     = %d %d\n", w, h);
    printf("img channels = %d\n", img.channels());

    pb = img.data;

    pm = new int8_t[w*h];
    for(i=0; i<n; i++) {
        if( pb[i] > 128 )
            pm[i] = 0;
        else
            pm[i] = 1;
    }

    // begin output data
    fp = fopen(fn_out.c_str(), "wb");
    if( fp == NULL ) {
        printf("ERR: can not open output file: %s\n", fn_out.c_str());
        return -1;
    }

    fwrite(&w, sizeof(uint32_t), 1, fp);
    fwrite(&h, sizeof(uint32_t), 1, fp);
    fwrite(pm, sizeof(int8_t),   n, fp);

    fclose(fp);

    delete [] pm;

    return 0;
}


////////////////////////////////////////////////////////////////////////////////
/// main function
////////////////////////////////////////////////////////////////////////////////
struct RTK_TestFunctionArray g_fa[] =
{
    RTK_FUNC_TEST_DEF(convert_img2map,          "draw text"),

    {NULL,  "NULL",  "NULL"},
};


int main(int argc, char *argv[])
{
    CParamArray     pa;

    return rtk_test_main(argc, argv,
                         g_fa, pa);
}
