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
#ifndef __BLENDER_POINTDENSITY__H__
#define __BLENDER_POINTDENSITY__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class PointDensity
    {
    public:
        short flag;
        short falloff_type;
        float falloff_softness;
        float radius;
        short source;
        short color_source;
        int totpoints;
        int pdpad;
        Object *object;
        int psys;
        short psys_cache_space;
        short ob_cache_space;
        void *point_tree;
        float *point_data;
        float noise_size;
        short noise_depth;
        short noise_influence;
        short noise_basis;
        short pdpad3[3];
        float noise_fac;
        float speed_scale;
        float falloff_speed_scale;
        float pdpad2;
        ColorBand *coba;
        CurveMapping *falloff_curve;
    };
}


#endif//__BLENDER_POINTDENSITY__H__
