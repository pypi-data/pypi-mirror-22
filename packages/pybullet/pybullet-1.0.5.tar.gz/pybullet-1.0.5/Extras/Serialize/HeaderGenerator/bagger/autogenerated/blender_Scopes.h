/* Copyright (C) 2006 Charlie C
*
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of this software.
*
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
*
* 1. The origin of this software must not be misrepresented; you must not
*    claim that you wrote the original software. If you use this software
*    in a product, an acknowledgment in the product documentation would be
*    appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
*    misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*/
// Auto generated from makesdna dna.c
#ifndef __BLENDER_SCOPES__H__
#define __BLENDER_SCOPES__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_Histogram.h"

namespace Blender {


    // ---------------------------------------------- //
    class Scopes
    {
    public:
        int ok;
        int sample_full;
        int sample_lines;
        float accuracy;
        int wavefrm_mode;
        float wavefrm_alpha;
        float wavefrm_yfac;
        int wavefrm_height;
        float vecscope_alpha;
        int vecscope_height;
        float minmax[3][2];
        Histogram hist;
        float *waveform_1;
        float *waveform_2;
        float *waveform_3;
        float *vecscope;
        int waveform_tot;
        int pad;
    };
}


#endif//__BLENDER_SCOPES__H__
