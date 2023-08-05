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
#ifndef __BLENDER_SCULPT__H__
#define __BLENDER_SCULPT__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_Paint.h"

namespace Blender {


    // ---------------------------------------------- //
    class Sculpt
    {
    public:
        Paint paint;
        int flags;
        int radial_symm[3];
        float detail_size;
        int symmetrize_direction;
        float gravity_factor;
        float constant_detail;
        float detail_percent;
        float pad;
        Object *gravity_object;
        void *pad2;
    };
}


#endif//__BLENDER_SCULPT__H__
