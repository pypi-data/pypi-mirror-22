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
#ifndef __BLENDER_CURVE__H__
#define __BLENDER_CURVE__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_CharInfo.h"
#include "blender_ID.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class Curve
    {
    public:
        ID id;
        AnimData *adt;
        BoundBox *bb;
        ListBase nurb;
        EditNurb *editnurb;
        Object *bevobj;
        Object *taperobj;
        Object *textoncurve;
        Ipo *ipo;
        Key *key;
        Material **mat;
        vec3f loc;
        vec3f size;
        vec3f rot;
        short type;
        short texflag;
        short drawflag;
        short twist_mode;
        float twist_smooth;
        float smallcaps_scale;
        int pathlen;
        short bevresol;
        short totcol;
        int flag;
        float width;
        float ext1;
        float ext2;
        short resolu;
        short resolv;
        short resolu_ren;
        short resolv_ren;
        int actnu;
        int actvert;
        char pad[4];
        short lines;
        char spacemode;
        char pad1;
        float spacing;
        float linedist;
        float shear;
        float fsize;
        float wordspace;
        float ulpos;
        float ulheight;
        float xof;
        float yof;
        float linewidth;
        int pos;
        int selstart;
        int selend;
        int len_wchar;
        int len;
        char *str;
        bInvalidHandle *editfont;
        char family[64];
        VFont *vfont;
        VFont *vfontb;
        VFont *vfonti;
        VFont *vfontbi;
        TextBox *tb;
        int totbox;
        int actbox;
        CharInfo *strinfo;
        CharInfo curinfo;
        float ctime;
        float bevfac1;
        float bevfac2;
        char bevfac1_mapping;
        char bevfac2_mapping;
        char pad2[2];
    };
}


#endif//__BLENDER_CURVE__H__
