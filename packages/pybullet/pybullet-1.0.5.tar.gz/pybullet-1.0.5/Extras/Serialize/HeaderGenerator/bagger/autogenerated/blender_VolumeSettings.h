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
#ifndef __BLENDER_VOLUMESETTINGS__H__
#define __BLENDER_VOLUMESETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class VolumeSettings
    {
    public:
        float density;
        float emission;
        float scattering;
        float reflection;
        vec3f emission_col;
        vec3f transmission_col;
        vec3f reflection_col;
        float density_scale;
        float depth_cutoff;
        float asymmetry;
        short stepsize_type;
        short shadeflag;
        short shade_type;
        short precache_resolution;
        float stepsize;
        float ms_diff;
        float ms_intensity;
        float ms_spread;
    };
}


#endif//__BLENDER_VOLUMESETTINGS__H__
