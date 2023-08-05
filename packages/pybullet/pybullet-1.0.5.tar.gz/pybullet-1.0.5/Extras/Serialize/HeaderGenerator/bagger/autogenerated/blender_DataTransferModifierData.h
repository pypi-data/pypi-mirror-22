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
#ifndef __BLENDER_DATATRANSFERMODIFIERDATA__H__
#define __BLENDER_DATATRANSFERMODIFIERDATA__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ModifierData.h"

namespace Blender {


    // ---------------------------------------------- //
    class DataTransferModifierData
    {
    public:
        ModifierData modifier;
        Object *ob_source;
        int data_types;
        int vmap_mode;
        int emap_mode;
        int lmap_mode;
        int pmap_mode;
        float map_max_distance;
        float map_ray_radius;
        float islands_precision;
        int pad_i1;
        int layers_select_src[4];
        int layers_select_dst[4];
        int mix_mode;
        float mix_factor;
        char defgrp_name[64];
        int flags;
    };
}


#endif//__BLENDER_DATATRANSFERMODIFIERDATA__H__
