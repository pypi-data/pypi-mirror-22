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
#ifndef __BLENDER_VOXELDATA__H__
#define __BLENDER_VOXELDATA__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class VoxelData
    {
    public:
        int resol[3];
        int interp_type;
        short file_format;
        short flag;
        short extend;
        short smoked_type;
        short hair_type;
        short data_type;
        int _pad;
        Object *object;
        float int_multiplier;
        int still_frame;
        char source_path[1024];
        float *dataset;
        int cachedframe;
        int ok;
    };
}


#endif//__BLENDER_VOXELDATA__H__
