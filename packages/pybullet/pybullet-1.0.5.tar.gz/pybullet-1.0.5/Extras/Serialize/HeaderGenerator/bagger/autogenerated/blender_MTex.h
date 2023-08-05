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
#ifndef __BLENDER_MTEX__H__
#define __BLENDER_MTEX__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class MTex
    {
    public:
        short texco;
        short mapto;
        short maptoneg;
        short blendtype;
        Object *object;
        Tex *tex;
        char uvname[64];
        char projx;
        char projy;
        char projz;
        char mapping;
        char brush_map_mode;
        char brush_angle_mode;
        char pad[2];
        vec3f ofs;
        vec3f size;
        float rot;
        float random_angle;
        short texflag;
        short colormodel;
        short pmapto;
        short pmaptoneg;
        short normapspace;
        short which_output;
        float r;
        float g;
        float b;
        float k;
        float def_var;
        float rt;
        float colfac;
        float varfac;
        float norfac;
        float dispfac;
        float warpfac;
        float colspecfac;
        float mirrfac;
        float alphafac;
        float difffac;
        float specfac;
        float emitfac;
        float hardfac;
        float raymirrfac;
        float translfac;
        float ambfac;
        float colemitfac;
        float colreflfac;
        float coltransfac;
        float densfac;
        float scatterfac;
        float reflfac;
        float timefac;
        float lengthfac;
        float clumpfac;
        float dampfac;
        float kinkfac;
        float kinkampfac;
        float roughfac;
        float padensfac;
        float gravityfac;
        float lifefac;
        float sizefac;
        float ivelfac;
        float fieldfac;
        int pad2;
        float shadowfac;
        float zenupfac;
        float zendownfac;
        float blendfac;
    };
}


#endif//__BLENDER_MTEX__H__
