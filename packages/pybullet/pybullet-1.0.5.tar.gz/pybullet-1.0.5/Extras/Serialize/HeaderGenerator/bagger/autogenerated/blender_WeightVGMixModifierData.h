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
#ifndef __BLENDER_WEIGHTVGMIXMODIFIERDATA__H__
#define __BLENDER_WEIGHTVGMIXMODIFIERDATA__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ModifierData.h"

namespace Blender {


    // ---------------------------------------------- //
    class WeightVGMixModifierData
    {
    public:
        ModifierData modifier;
        char defgrp_name_a[64];
        char defgrp_name_b[64];
        float default_weight_a;
        float default_weight_b;
        char mix_mode;
        char mix_set;
        char pad_c1[6];
        float mask_constant;
        char mask_defgrp_name[64];
        int mask_tex_use_channel;
        Tex *mask_texture;
        Object *mask_tex_map_obj;
        int mask_tex_mapping;
        char mask_tex_uvlayer_name[64];
        int pad_i1;
    };
}


#endif//__BLENDER_WEIGHTVGMIXMODIFIERDATA__H__
